<template>
    <div class="debating-container">
        <div class="title-container">
            <h1 class="debate-title">{{ formatCommitteeName(group) }} Debate</h1>
        </div>

        <!-- Comparison View -->
        <div v-if="isComparing" class="comparison-container">
            <div class="comparison-header">
                <h2>Amendment Comparison</h2>
                <div class="status-badge comparing" :class="{ 'editing': amendmentState.isEditingActive.value }">
                    {{ amendmentState.isEditingActive.value ? 'live editing' : 'debating amendments' }}
                </div>
            </div>

            <div class="clauses-grid">
                <!-- Original Clause -->
                <div class="clause-box">
                    <h3>Original Clause</h3>
                    <div class="clause-content"
                        v-html="amendmentState.isEditingActive.value ? amendmentState.originalContent : originalContent">
                    </div>
                </div>

                <!-- Amended Clause -->
                <div class="clause-box">
                    <h3>Proposed Changes</h3>
                    <div class="clause-content diff-view" v-html="amendedDiff"></div>
                </div>
            </div>
        </div>

        <!-- Normal View -->
        <div v-else-if="currentClause" class="clause-container">
            <div class="clause-header">
                <h2>Current Clause</h2>
                <div class="clause-info">
                    <span class="country-info">Submitted by: {{ currentClause.country }}</span>
                    <span class="status-badge" :class="{ 'is-active': isLiveEditing }">
                        {{ isLiveEditing ? 'Live Updating' : 'Debating' }}
                    </span>
                </div>
            </div>
            <div class="clause-content" v-html="currentClause.content"></div>
        </div>

        <div v-else class="no-clause">
            <div class="empty-state-container">
                <div class="empty-state-message">
                    <h3>No clause is currently being debated</h3>
                    <div class="no-clause-info">
                        <p>The chair has not yet opened a clause for debate in the {{ formatCommitteeName(group) }}
                            committee.</p>
                        <p>Please wait for the chair to select a clause or check with your committee chair for more
                            information.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { io } from 'socket.io-client';
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import { GlassMessage } from '../components/ui';
import { useRoute } from 'vue-router';
import { useAmendmentState } from '../composables/useAmendmentState';

export default {
    name: 'DebatingGroup',
    setup() {
        const BASE_URL = 'http://127.0.0.1:8000';

        // State
        const currentClause = ref(null);
        const group = ref('');
        const socket = io(BASE_URL);
        const isLiveEditing = ref(false);
        const route = useRoute();
        let liveEditingTimeout;

        // Amendment comparison state
        const isComparing = ref(false);
        const proposedContent = ref('');
        const currentAmendmentId = ref(null);
        const originalContent = ref('');

        // Access shared amendment state
        const amendmentState = useAmendmentState();

        // Watch for changes in the shared amendment state
        watch(() => amendmentState.isEditingActive.value, (isActive) => {
            if (isActive) {
                // When editing becomes active, show comparison view with the shared state data
                originalContent.value = amendmentState.originalContent.value;
                proposedContent.value = amendmentState.editingContent.value;
                currentAmendmentId.value = amendmentState.editingAmendmentId.value;
                isComparing.value = true;
            }
        });

        // Also watch for changes in editing content
        watch(() => amendmentState.editingContent.value, (newContent) => {
            if (amendmentState.isEditingActive.value) {
                proposedContent.value = newContent;
            }
        });

        // Simplified approach without diff-match-patch
        const amendedDiff = computed(() => {
            // Just display the proposed content directly without diffing
            return amendmentState.isEditingActive.value
                ? amendmentState.editingContent.value
                : proposedContent.value;
        });

        // Data fetching
        const fetchCurrentClause = async (committee) => {
            if (!committee) return;

            try {
                const response = await axios.get(`${BASE_URL}/committee/${committee.toLowerCase()}/current-clause`);
                if (response.data) {
                    currentClause.value = response.data;

                    // Reset comparison state
                    resetComparisonState();

                    // Only load comparison if there's an active amendment under debate
                    if (currentClause.value.active_amendment_id) {
                        try {
                            const amendmentResponse = await axios.get(
                                `${BASE_URL}/amendments/${currentClause.value.active_amendment_id}`
                            );

                            if (amendmentResponse.data && amendmentResponse.data.under_debate) {
                                originalContent.value = currentClause.value.content;
                                proposedContent.value = amendmentResponse.data.amended_clause;
                                currentAmendmentId.value = currentClause.value.active_amendment_id;
                                isComparing.value = true;
                            }
                        } catch (amendmentError) {
                            console.error('Error fetching active amendment:', amendmentError);
                            GlassMessage.error('Could not load active amendment');
                        }
                    }
                }
            } catch (error) {
                console.error('Error fetching current clause:', error);
                currentClause.value = null;
                isComparing.value = false;
                if (error.response?.status === 404) {
                    GlassMessage.info('No clause is currently under debate');
                } else {
                    GlassMessage.error('Error loading current clause');
                }
            }
        };

        // Socket handlers
        const setupSocket = () => {
            const socketEvents = {
                connect: () => {
                    console.log('Connected to websocket');
                },

                clause_published: (data) => {
                    if (isRelevantToCommittee(data)) {
                        currentClause.value = data;
                        resetComparisonState();

                        // Clear any ongoing amendment editing when a new clause is published
                        amendmentState.clearAmendmentEdit();

                        GlassMessage.success('New clause has been published');
                    }
                },

                clause_unpublished: (data) => {
                    if (isRelevantToCommittee(data)) {
                        // Clear the current clause since it's been unpublished
                        currentClause.value = null;
                        resetComparisonState();

                        // Clear any ongoing amendment editing
                        amendmentState.clearAmendmentEdit();

                        GlassMessage.info('The clause has been unpublished');
                    }
                },

                clause_rejected: (data) => {
                    if (isRelevantToCommittee(data)) {
                        // Clear the current clause since it's been rejected
                        currentClause.value = null;
                        resetComparisonState();

                        // Clear any ongoing amendment editing
                        amendmentState.clearAmendmentEdit();

                        GlassMessage.warning('The clause has been rejected');
                    }
                },

                debate_content_update: (data) => {
                    if (isRelevantToCommittee(data)) {
                        if (data.type === 'amendment_approved') {
                            handleAmendmentApproved(data);
                        } else {
                            handleContentUpdate(data);
                        }
                    }
                },

                clause_comparison: (data) => {
                    if (isRelevantToCommittee(data)) {
                        // Only proceed if we're not actively editing an amendment
                        if (!amendmentState.isEditingActive.value) {
                            // Store original content in currentClause
                            if (currentClause.value) {
                                currentClause.value = {
                                    ...currentClause.value,
                                    content: data.original_content
                                };
                            } else {
                                currentClause.value = { content: data.original_content };
                            }

                            // Store new content in proposedContent
                            originalContent.value = data.original_content;
                            proposedContent.value = data.new_content;
                            currentAmendmentId.value = data.amendment_id;
                            isComparing.value = true;
                            GlassMessage.info('Comparing amendment changes');
                        }
                    }
                },

                amendment_status_changed: (data) => {
                    if (isRelevantToCommittee(data) && data.is_published) {
                        if (currentAmendmentId.value === data.id) {
                            if (currentClause.value) {
                                currentClause.value = {
                                    ...currentClause.value,
                                    content: proposedContent.value
                                };
                            }
                            resetComparisonState();

                            // Clear any ongoing amendment editing
                            amendmentState.clearAmendmentEdit();

                            GlassMessage.success('Amendment has been applied');
                        }
                    }
                },

                amendment_rejected: (data) => {
                    if (isRelevantToCommittee(data)) {
                        // If the rejected amendment was being compared
                        if (currentAmendmentId.value === data.amendment_id) {
                            resetComparisonState();

                            // Clear any ongoing amendment editing
                            amendmentState.clearAmendmentEdit();
                        }

                        // If the rejected amendment was associated with the current clause
                        if (currentClause.value?.id === data.debate_clause_id) {
                            currentClause.value = {
                                ...currentClause.value,
                                active_amendment_id: null
                            };
                            isComparing.value = false;
                        }

                        GlassMessage.warning('Amendment has been rejected and comparison closed');
                    }
                },

                amendment_unpublished: (data) => {
                    if (isRelevantToCommittee(data)) {
                        resetComparisonState();

                        // Clear any ongoing amendment editing
                        amendmentState.clearAmendmentEdit();

                        // Update current clause content if needed
                        if (currentClause.value?.id === data.clause_id) {
                            currentClause.value = {
                                ...currentClause.value,
                                content: data.original_content,
                                active_amendment_id: null
                            };
                        }

                        GlassMessage.info('Amendment unpublished and changes reverted');
                    }
                },

                amendment_under_debate: (data) => {
                    if (isRelevantToCommittee(data)) {
                        // Only proceed if we're not actively editing an amendment
                        if (!amendmentState.isEditingActive.value) {
                            if (currentClause.value) {
                                currentClause.value = {
                                    ...currentClause.value,
                                    content: data.original_content,
                                    is_amended: true
                                };
                            } else {
                                currentClause.value = {
                                    content: data.original_content,
                                    is_amended: true
                                };
                            }

                            originalContent.value = data.original_content;
                            proposedContent.value = data.amended_content;
                            currentAmendmentId.value = data.amendment_id;
                            isComparing.value = true;
                            GlassMessage.info('Amendment is now under debate');
                        }
                    }
                }
            };

            // Register all event listeners
            Object.entries(socketEvents).forEach(([event, handler]) => {
                socket.on(event, handler);
            });
        };

        // Helper functions
        const isRelevantToCommittee = (data) => {
            return data.committee && data.committee.toLowerCase() === group.value.toLowerCase();
        };

        const resetComparisonState = () => {
            isComparing.value = false;
            proposedContent.value = '';
            currentAmendmentId.value = null;

            // If we're not in editor mode, also clear the shared state
            if (!amendmentState.isEditingActive.value) {
                amendmentState.clearAmendmentEdit();
            }
        };

        const handleAmendmentApproved = (data) => {
            // Update the current clause with the approved amendment content
            if (currentClause.value) {
                currentClause.value = {
                    ...currentClause.value,
                    content: data.content,
                    country: data.country
                };
            } else {
                currentClause.value = {
                    content: data.content,
                    country: data.country
                };
            }

            // Reset comparison view if this was the current amendment being compared
            if (currentAmendmentId.value === data.amendment_id) {
                resetComparisonState();
            }

            GlassMessage.success('Amendment has been approved and applied');
        };

        const handleContentUpdate = (data) => {
            // Handle other types of content updates
            if (currentClause.value && currentClause.value.id === data.clause_id) {
                currentClause.value = {
                    ...currentClause.value,
                    content: data.content
                };

                isLiveEditing.value = true;

                if (liveEditingTimeout) {
                    clearTimeout(liveEditingTimeout);
                }

                liveEditingTimeout = setTimeout(() => {
                    isLiveEditing.value = false;
                }, 2000);
            }
        };

        const formatCommitteeName = (name) => {
            if (!name) return '';
            
            // Committee name mapping
            const committeeNameMap = {
                'junior': 'Junior',
                'senior': 'Senior',
                'security-council': 'Security Council'
            };
            
            // Use the mapping if available
            if (committeeNameMap[name]) {
                return committeeNameMap[name];
            }
            
            // Otherwise format properly: replace hyphens with spaces and capitalize first letter of each word
            return name.replace(/-/g, ' ')
                .split(' ')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                .join(' ');
        };

        // Lifecycle hooks
        onMounted(() => {
            group.value = route.params.group;

            if (group.value) {
                fetchCurrentClause(group.value);
                setupSocket();
            } else {
                console.error('No committee specified in route');
                GlassMessage.error('Invalid committee');
            }
        });

        onUnmounted(() => {
            if (liveEditingTimeout) {
                clearTimeout(liveEditingTimeout);
            }
            socket.disconnect();
        });

        return {
            currentClause,
            group,
            formatCommitteeName,
            isLiveEditing,
            isComparing,
            proposedContent,
            originalContent,
            amendedDiff,
            amendmentState
        };
    }
};
</script>

<style scoped>
/* Import Apatos font if not already imported globally */
@import url('https://fonts.googleapis.com/css2?family=Apatos:wght@400;500;600;700&display=swap');

.debating-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    /* Prevent inheritance from glass-bg parent */
    color: #333333;
    all: initial;
    font-family: inherit;
    /* Restore the container styling after resetting inheritance */
    display: block;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

/* Title container to ensure proper positioning */
.title-container {
    width: 100%;
    text-align: center;
    margin-bottom: 30px;
    position: relative;
    z-index: 10;
}

/* Debate title with !important to override any other styles */
.debate-title {
    color: #FFFFFF !important;
    font-size: 2rem !important;
    font-weight: bold !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    margin: 0 !important;
    padding: 0 !important;
    display: inline-block !important;
    text-align: center !important;
    font-family: 'Apatos', sans-serif !important;
}

/* Re-style all elements to ensure they're not inheriting from parent */
.debating-container * {
    all: revert;
}

/* Exclude the title from the revert */
.debating-container .title-container,
.debating-container .debate-title {
    all: initial;
    display: block;
}

.debating-container .title-container {
    width: 100%;
    text-align: center;
    margin-bottom: 30px;
}

.debating-container .debate-title {
    color: #FFFFFF;
    font-size: 2rem;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    font-family: 'Apatos', sans-serif;
}

h1 {
    color: #FFFFFF;
    margin-bottom: 30px;
    text-align: center;
    width: 100%;
    display: block;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

p {
    color: #000000;
}

.clause-container {
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 20px;
    transition: all 0.3s ease;
}

.clause-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(235, 238, 245, 0.5);
}

.clause-header h2 {
    margin: 0;
    color: #303133;
}

.clause-info {
    display: flex;
    align-items: center;
    gap: 15px;
}

.country-info {
    color: #606266;
    font-size: 0.9em;
}

.status-badge {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8em;
    background-color: rgba(103, 194, 58, 0.8);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    color: white;
    box-shadow: 0 2px 6px rgba(103, 194, 58, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.status-badge.is-active {
    background-color: rgba(64, 158, 255, 0.8);
    animation: pulse 2s infinite;
    box-shadow: 0 2px 6px rgba(64, 158, 255, 0.2);
}

.clause-content {
    padding: 20px;
    background-color: rgba(248, 249, 250, 0.5);
    border-radius: 12px;
    min-height: 200px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
}

.no-clause {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 400px;
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Safari-friendly empty state styling */
.empty-state-container {
    width: 100%;
    text-align: center;
    padding: 40px 20px;
}

.empty-state-message {
    background-color: rgba(255, 255, 255, 0.95);
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    display: inline-block;
    max-width: 500px;
}

.empty-state-message h3 {
    font-size: 1.3rem;
    color: #303133;
    margin-top: 0;
    margin-bottom: 20px;
    font-weight: 600;
}

.no-clause-info {
    margin-top: 20px;
    text-align: center;
    max-width: 500px;
    color: #606266;
    font-family: 'Apatos', sans-serif;
}

.no-clause-info p {
    margin-bottom: 10px;
    line-height: 1.5;
    font-size: 1rem;
    color: #606266;
}

@keyframes pulse {
    0% {
        opacity: 1;
    }

    50% {
        opacity: 0.6;
    }

    100% {
        opacity: 1;
    }
}

.comparison-container {
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 20px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.comparison-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(235, 238, 245, 0.5);
}

.clauses-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    align-items: start;
}

.clause-box {
    background-color: rgba(248, 249, 250, 0.6);
    border-radius: 12px;
    padding: 15px;
    height: 80vh;
    overflow-y: auto;
    border: 1px solid rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
}

.clause-box h3 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #303133;
}

.status-badge.comparing {
    background-color: rgba(230, 162, 60, 0.8);
    animation: pulse 2s infinite;
    box-shadow: 0 2px 6px rgba(230, 162, 60, 0.2);
}

.status-badge.comparing.editing {
    background-color: rgba(64, 158, 255, 0.8);
    box-shadow: 0 2px 6px rgba(64, 158, 255, 0.2);
}

/* Update deletion style */
:deep(.diff-view) del {
    background-color: rgba(255, 230, 230, 0.7);
    text-decoration: line-through;
    color: #ff4444;
    opacity: 0.7;
}

/* Update insertion style */
:deep(.diff-view) ins {
    background-color: rgba(230, 255, 230, 0.7);
    text-decoration: none;
    border-bottom: 2px solid #4CAF50;
}

/* Safari-specific fixes */
@media not all and (min-resolution:.001dpcm) { 
    @supports (-webkit-appearance:none) {
        .no-clause {
            background-color: rgba(255, 255, 255, 0.95);
        }
        
        .empty-state-message {
            background-color: #ffffff;
        }
    }
}
</style>
