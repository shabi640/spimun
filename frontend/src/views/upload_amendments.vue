<template>
    <div class="amendment-upload-container">
        <h1>Submit Amendment</h1>

        <!-- Published Clause Section -->
        <div v-if="currentClause" class="published-clause-section">
            <div class="glass-collapse">
                <div class="glass-collapse-header" @click="toggleClause">
                    <div class="clause-header">
                        <span>Current Published Clause</span>
                        <span class="country-info">Submitted by: {{ currentClause.country }}</span>
                    </div>
                    <span class="collapse-icon">{{ isClauseExpanded ? '▼' : '►' }}</span>
                </div>
                <div v-if="isClauseExpanded" class="glass-collapse-content">
                    <div v-html="sanitizedClauseContent"></div>
                </div>
            </div>
        </div>

        <div v-else class="no-clause-warning">
            <GlassAlert title="No clause is currently under debate" type="warning"
                description="Please wait for a clause to be published before submitting amendments." :closable="false"
                :show-icon="true">
            </GlassAlert>
        </div>

        <!-- Amendment Editor Section -->
        <div class="amendment-editor-section">
            <h2>Your Amendment</h2>
            <ckeditor-component v-model="amendmentContent" :disabled="!currentClause" />
        </div>

        <!-- Submit Button -->
        <div class="submit-section">
            <GlassButton type="primary" @click="submitAmendment" :disabled="!currentClause || !amendmentContent">
                Submit Amendment
            </GlassButton>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { io } from 'socket.io-client';
import { GlassAlert, GlassButton, GlassMessage } from '../components/ui';
import CkeditorComponent from '../components/ckeditor.vue';
import DOMPurify from 'dompurify';

export default {
    name: 'UploadAmendments',
    components: {
        CkeditorComponent,
        GlassAlert,
        GlassButton
    },
    setup() {
        const route = useRoute();
        const router = useRouter();
        const currentClause = ref(null);
        const amendmentContent = ref('');
        console.log('[AMENDMENTS] Creating socket connection in setup');
        const socket = io('http://127.0.0.1:8000');
        socket.on('connect', () => {
            console.log('[AMENDMENTS] Socket connected with ID:', socket.id);
        });
        const committee = ref('');
        const isClauseExpanded = ref(false);
        const isSubmitting = ref(false);

        const toggleClause = () => {
            isClauseExpanded.value = !isClauseExpanded.value;
        };

        const fetchCurrentClause = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/committee/${committee.value}/current-clause`);
                currentClause.value = response.data;
                if (!currentClause.value) {
                    GlassMessage.info('No clause is currently under debate');
                }
            } catch (error) {
                console.error('Error fetching current clause:', error);
                if (error.response && error.response.status === 404) {
                    GlassMessage.info('No clause is currently under debate');
                } else {
                    GlassMessage.error('Connection error. Please try again later.');
                }
            }
        };

        const submitAmendment = async () => {
            console.log('Submit function called');

            if (isSubmitting.value) {
                console.log('Preventing duplicate submission');
                return;
            }

            if (!currentClause.value) {
                GlassMessage.warning('No clause is currently under debate');
                return;
            }

            const delegate = JSON.parse(localStorage.getItem('delegate'));
            if (!delegate) {
                GlassMessage.error('Please sign in to submit amendments');
                return;
            }

            try {
                isSubmitting.value = true;
                console.log('Sending amendment submission request');

                await axios.post('http://127.0.0.1:8000/amendments/add', {
                    amendment: amendmentContent.value,
                    country: delegate.country,
                    committee: committee.value,
                    clause_id: currentClause.value.id
                });

                GlassMessage.success('Amendment submitted successfully');
                amendmentContent.value = '';
            } catch (error) {
                console.error('Error submitting amendment:', error);
                GlassMessage.error('Failed to submit amendment');
            } finally {
                setTimeout(() => {
                    isSubmitting.value = false;
                    console.log('Submission flag reset');
                }, 500);
            }
        };

        // Socket event handlers
        const setupSocket = () => {
            socket.on('clause_published', (data) => {
                console.log('[AMENDMENTS] Received clause_published event:', data);
                if (data.committee.toLowerCase() === committee.value.toLowerCase()) {
                    console.log('[AMENDMENTS] Committee matches, updating currentClause');
                    currentClause.value = data;
                    // Only show a message if the silent flag is not set
                    if (!data.silent) {
                        console.log('[AMENDMENTS] silent=false, showing info message');
                        GlassMessage.info('New clause has been published');
                    } else {
                        console.log('[AMENDMENTS] silent=true, not showing info message');
                    }
                } else {
                    console.log('[AMENDMENTS] Committee does not match, ignoring event');
                }
            });

            socket.on('clause_rejected', (data) => {
                console.log('[AMENDMENTS] Received clause_rejected event:', data);
                if (data.committee.toLowerCase() === committee.value.toLowerCase() &&
                    currentClause.value &&
                    currentClause.value.id === data.clauseId) {
                    console.log('[AMENDMENTS] Committee and clause ID match, updating currentClause to null');
                    currentClause.value = null;
                    // Only show a message if the silent flag is not set
                    if (!data.silent) {
                        console.log('[AMENDMENTS] silent=false, showing warning message');
                        GlassMessage.warning('The current clause has been rejected');
                    } else {
                        console.log('[AMENDMENTS] silent=true, not showing warning message');
                    }
                } else {
                    console.log('[AMENDMENTS] Committee or clause ID does not match, ignoring event');
                }
            });

            socket.on('clause_unpublished', (data) => {
                console.log('[AMENDMENTS] Received clause_unpublished event:', data);
                if (data.committee.toLowerCase() === committee.value.toLowerCase() &&
                    currentClause.value &&
                    currentClause.value.id === data.clauseId) {
                    console.log('[AMENDMENTS] Committee and clause ID match, updating currentClause to null');
                    currentClause.value = null;
                    // Only show a message if the silent flag is not set
                    if (!data.silent) {
                        console.log('[AMENDMENTS] silent=false, showing info message');
                        GlassMessage.info('The current clause has been unpublished');
                    } else {
                        console.log('[AMENDMENTS] silent=true, not showing info message');
                    }
                } else {
                    console.log('[AMENDMENTS] Committee or clause ID does not match, ignoring event');
                }
            });
        };

        // Sanitize HTML content to prevent XSS attacks
        const sanitizeHtml = (html) => {
            return DOMPurify.sanitize(html);
        };

        // Computed property for sanitized clause content
        const sanitizedClauseContent = computed(() => {
            if (currentClause.value) {
                return sanitizeHtml(currentClause.value.content);
            }
            return '';
        });

        onMounted(() => {
            const delegate = JSON.parse(localStorage.getItem('delegate') || 'null');
            if (!delegate) {
                GlassMessage.error('Please login first');
                router.push('/');
                return;
            }

            committee.value = route.params.committee;
            if (!committee.value) {
                committee.value = delegate.committee;
            }

            if (committee.value) {
                console.log('Initializing with committee:', committee.value);
                fetchCurrentClause();
                setupSocket();
            } else {
                GlassMessage.error('Committee not found');
                router.push('/');
            }
        });

        onUnmounted(() => {
            socket.disconnect();
        });

        return {
            currentClause,
            amendmentContent,
            submitAmendment,
            isClauseExpanded,
            toggleClause,
            isSubmitting,
            sanitizedClauseContent
        };
    }
};
</script>

<style scoped>
.amendment-upload-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    text-align: center;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    margin-bottom: 30px;
}

.published-clause-section {
    margin-bottom: 30px;
}

.glass-collapse {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.glass-collapse-header {
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    font-weight: bold;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    transition: background-color 0.3s;
}

.glass-collapse-header:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.collapse-icon {
    font-size: 14px;
    color: var(--text-color, rgba(255, 255, 255, 0.7));
}

.glass-collapse-content {
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.1);
    color: var(--text-color, rgba(255, 255, 255, 0.9));
}

.clause-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.country-info {
    font-size: 0.9em;
    color: var(--text-color, rgba(255, 255, 255, 0.7));
}

.amendment-editor-section {
    margin-top: 30px;
}

.amendment-editor-section h2 {
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    margin-bottom: 20px;
}

.submit-section {
    margin-top: 20px;
    text-align: right;
}

.no-clause-warning {
    margin: 20px 0;
}
</style>
