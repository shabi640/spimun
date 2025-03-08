<template>
    <div class="amendments-container">
        <!-- Main Content -->
        <div class="main-content">
            <!-- Alert when no clause is published -->
            <div v-if="noPublishedClause" class="no-clause-warning">
                <GlassAlert title="No Published Clause" type="warning" :closable="false">
                    <p>There is currently no clause under debate in this committee.</p>
                    <p>Please publish a clause first to view and manage amendments.</p>
                </GlassAlert>
            </div>

            <!-- Main content when there is a published clause -->
            <div v-if="!noPublishedClause" class="main-content-wrapper">
                <h2>Amendments for Current Clause</h2>
                <div class="amendments-list">
                    <GlassEmpty v-if="currentClauseAmendments.length === 0"
                        description="No amendments for current clause" />

                    <div v-else class="amendments-list">
                        <div v-for="amendment in currentClauseAmendments" :key="amendment.id" class="amendment-item"
                            :class="{ 'published': amendment.is_published }">
                            <div class="amendment-header" @click="handleAmendmentClick(amendment.id)">
                                <span class="country">{{ amendment.country }}</span>
                                <GlassTag v-if="amendment.is_published" type="success" size="small"
                                    class="published-tag">Published</GlassTag>
                                <span class="timestamp">{{ formatTimestamp(amendment.timestamp) }}</span>
                                <GlassIcon class="toggle-icon" name="arrow-down" color="primary" size="small"
                                    :class="{ 'is-active': activeAmendment === amendment.id }">
                                </GlassIcon>
                            </div>
                            <div v-show="activeAmendment === amendment.id" class="amendment-content">
                                <div v-html="amendment.amendment_text"></div>
                                <div class="amendment-actions">
                                    <GlassButton @click="openAmendmentEditor(amendment)" type="primary" size="small"
                                        class="edit-button">
                                        Edit Amendment
                                    </GlassButton>
                                    <GlassButton @click="deleteAmendment(amendment)" type="danger" size="small"
                                        class="action-button">
                                        Delete
                                    </GlassButton>
                                    <template v-if="amendment.is_published">
                                        <GlassButton @click="unpublishAmendment(amendment)" type="warning" size="small"
                                            class="action-button">
                                            Unpublish
                                        </GlassButton>
                                        <GlassButton @click="rejectAmendment(amendment)" type="danger" size="small"
                                            class="action-button">
                                            Reject
                                        </GlassButton>
                                        <GlassButton @click="approveAmendment(amendment)" type="success" size="small"
                                            class="action-button">
                                            Approve
                                        </GlassButton>
                                    </template>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Approved Amendments for This Clause -->
            <GlassCollapse v-model="activePanel" v-if="currentClause && approvedForClause.length > 0">
                <GlassCollapseItem name="approved">
                    <template #title>
                        <h2>Approved Amendments for This Clause</h2>
                    </template>
                    <div class="amendments-list">
                        <div v-for="amendment in approvedForClause" :key="amendment.id" class="amendment-item approved">
                            <div class="amendment-header" @click="showApprovedAmendmentDialog(amendment)">
                                <span class="country">{{ amendment.country }}</span>
                                <div class="amendment-preview" v-html="amendment.amendment_text"></div>
                                <GlassTag type="success" size="small">Approved</GlassTag>
                                <span class="timestamp">{{ formatTimestamp(amendment.timestamp) }}</span>
                                <GlassIcon class="toggle-icon" name="document" color="primary" size="small"></GlassIcon>
                            </div>
                        </div>
                    </div>
                </GlassCollapseItem>
            </GlassCollapse>

            <!-- Other Amendments Section -->
            <div class="other-amendments-section">
                <GlassCollapse>
                    <GlassCollapseItem name="other">
                        <template #title>
                            <h2>Other Amendments</h2>
                        </template>

                        <GlassEmpty v-if="otherAmendments.length === 0" description="No other amendments" />

                        <div v-else class="amendments-list">
                            <div v-for="amendment in otherAmendments" :key="amendment.id" class="amendment-item"
                                :class="{ 'published': amendment.is_published }">
                                <div class="amendment-header" @click="handleAmendmentClick(amendment.id)">
                                    <span class="country">{{ amendment.country }}</span>
                                    <GlassTag size="small">Clause {{ amendment.clause_id }}</GlassTag>
                                    <GlassTag v-if="amendment.is_published" type="success" size="small"
                                        class="published-tag">
                                        Published</GlassTag>
                                    <span class="timestamp">{{ formatTimestamp(amendment.timestamp) }}</span>
                                    <GlassIcon class="toggle-icon" name="arrow-down" color="primary" size="small"
                                        :class="{ 'is-active': activeAmendment === amendment.id }">
                                    </GlassIcon>
                                </div>
                                <div v-show="activeAmendment === amendment.id" class="amendment-content">
                                    <div v-html="amendment.amendment_text"></div>
                                    <div class="amendment-actions">
                                        <GlassButton @click="openAmendmentEditor(amendment)" type="primary" size="small"
                                            class="edit-button">
                                            Edit Amendment
                                        </GlassButton>
                                        <GlassButton @click="deleteAmendment(amendment)" type="danger" size="small"
                                            class="action-button">
                                            Delete
                                        </GlassButton>
                                        <template v-if="amendment.is_published">
                                            <GlassButton @click="unpublishAmendment(amendment)" type="warning"
                                                size="small" class="action-button">
                                                Unpublish
                                            </GlassButton>
                                            <GlassButton @click="rejectAmendment(amendment)" type="danger" size="small"
                                                class="action-button">
                                                Reject
                                            </GlassButton>
                                            <GlassButton @click="approveAmendment(amendment)" type="success"
                                                size="small" class="action-button">
                                                Approve
                                            </GlassButton>
                                        </template>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </GlassCollapseItem>
                </GlassCollapse>
            </div>
        </div>

        <!-- Floating Current Clause Button -->
        <div v-if="currentClause" class="floating-clause-button"
            :style="{ top: buttonPosition.y + 'px', left: buttonPosition.x + 'px' }" @mousedown="startDrag"
            @click="showCurrentClauseDialog">
            <GlassIcon name="document" color="success" size="large"></GlassIcon>
            <span class="clause-number">{{ currentClause.clause_id }}</span>
        </div>

        <!-- Amendment Editor Dialog -->
        <GlassDialog v-model="isEditorVisible" title="Amendment View" width="90%" :close-on-click-modal="false"
            class="amendment-editor-dialog">
            <div class="editor-layout">
                <!-- Left: Main Editor Section -->
                <div class="editor-main">
                    <h3>Current Clause with Amendment</h3>
                    <ckeditor-component v-model="editingContent" @update:modelValue="handleEditorChange" />
                </div>

                <!-- Right: Reference Section -->
                <div class="reference-section">
                    <h3>Amendment Reference</h3>
                    <div class="amendment-info">
                        <span class="country">From: {{ selectedAmendment?.country }}</span>
                        <span class="timestamp">{{ selectedAmendment ? formatTimestamp(selectedAmendment.timestamp) : ''
                            }}</span>
                    </div>
                    <div class="amendment-reference-content" v-if="selectedAmendment"
                        v-html="selectedAmendment.amendment_text">
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="dialog-footer">
                    <GlassButton @click="closeEditor">Cancel</GlassButton>
                    <GlassButton type="primary" @click="saveChanges">Publish</GlassButton>
                </div>
            </template>
        </GlassDialog>

        <!-- Amendment View Dialog for Approved Amendments -->
        <GlassDialog v-model="isApprovedAmendmentVisible" title="Approved Amendment" width="60%"
            custom-class="glass-dialog fixed-position-dialog">
            <div v-if="selectedApprovedAmendment" class="approved-amendment-content">
                <div class="amendment-info glass-panel">
                    <span class="country">From: {{ selectedApprovedAmendment.country }}</span>
                    <span class="timestamp">{{ formatTimestamp(selectedApprovedAmendment.timestamp) }}</span>
                </div>
                <div class="amendment-view-content glass-panel" v-html="selectedApprovedAmendment.amendment_text"></div>
            </div>
            <template #footer>
                <div class="dialog-footer">
                    <GlassButton @click="closeApprovedAmendmentDialog">Close</GlassButton>
                </div>
            </template>
        </GlassDialog>

        <!-- Current Clause Dialog -->
        <GlassDialog v-model="isCurrentClauseVisible" :title="`Current Clause ${currentClause?.clause_id || ''}`"
            width="60%" custom-class="glass-dialog fixed-position-dialog">
            <div v-if="currentClause" class="current-clause-content">
                <div class="clause-meta glass-panel">
                    <div class="clause-header">
                        <span class="clause-country">{{ currentClause.country }}</span>
                        <GlassTag type="success" size="small">Published</GlassTag>
                    </div>
                    <div class="clause-stats">
                        <div class="stat-item">
                            <span class="stat-label">Clause Number:</span>
                            <span class="stat-value">{{ currentClause.clause_id }}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Total Amendments:</span>
                            <span class="stat-value">{{ totalAmendmentsCount }}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Pending Amendments:</span>
                            <span class="stat-value">{{ pendingAmendmentsCount }}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Publish Time:</span>
                            <span class="stat-value">{{ formatTimestamp(currentClause.timestamp) }}</span>
                        </div>
                    </div>
                </div>
                <div class="clause-content glass-panel" v-html="currentClause.content"></div>
            </div>
            <template #footer>
                <div class="dialog-footer">
                    <GlassButton @click="closeCurrentClauseDialog">Close</GlassButton>
                </div>
            </template>
        </GlassDialog>
    </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import axios from 'axios';
import { io } from 'socket.io-client';
import CKEditor from '../components/ckeditor.vue';
import { GlassMessage, GlassIcon, GlassAlert, GlassButton, GlassEmpty, GlassTag, GlassDialog } from '../components/ui';
import { useAmendmentState } from '../composables/useAmendmentState';

export default {
    name: 'AmendmentsView',
    components: {
        'ckeditor-component': CKEditor,
        GlassIcon,
        GlassAlert,
        GlassButton,
        GlassEmpty,
        GlassTag,
        GlassDialog
    },
    props: {
        committee: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const BASE_URL = 'http://127.0.0.1:8000';

        // State
        const currentClause = ref(null);
        const amendments = ref([]);
        const socket = io(BASE_URL);
        const isEditorVisible = ref(false);
        const selectedAmendment = ref(null);
        const editingContent = ref('');
        const activePanel = ref(['amendment']);
        const activeAmendment = ref(null);
        const noPublishedClause = ref(false);
        const isApprovedAmendmentVisible = ref(false);
        const selectedApprovedAmendment = ref(null);
        const isCurrentClauseVisible = ref(false);

        // Floating button position
        const buttonPosition = ref({ x: window.innerWidth - 80, y: window.innerHeight - 80 });
        const isDragging = ref(false);
        const dragOffset = ref({ x: 0, y: 0 });

        // Import shared amendment state
        const amendmentState = useAmendmentState();

        // Computed properties
        const currentClauseAmendments = computed(() => {
            if (!currentClause.value) return [];
            return filterAndSortAmendments(amendments.value, currentClause.value.id);
        });

        const otherAmendments = computed(() => {
            if (!currentClause.value) return amendments.value.filter(a => !a.is_passed);
            return filterAndSortAmendments(
                amendments.value.filter(a => a.clause_id !== currentClause.value.id)
            );
        });

        const approvedForClause = computed(() => {
            if (!currentClause.value) return [];
            return amendments.value.filter(a =>
                a.is_passed &&
                a.clause_id === currentClause.value?.id &&
                a.committee.toLowerCase() === props.committee.toLowerCase()
            );
        });

        const publishedAmendmentsCount = computed(() =>
            currentClauseAmendments.value.filter(a => a.is_published).length
        );

        // 新增计算属性
        const totalAmendmentsCount = computed(() => {
            if (!currentClause.value) return 0;
            return amendments.value.filter(a =>
                a.clause_id === currentClause.value.id &&
                a.committee.toLowerCase() === props.committee.toLowerCase()
            ).length;
        });

        const pendingAmendmentsCount = computed(() => {
            if (!currentClause.value) return 0;
            return amendments.value.filter(a =>
                a.clause_id === currentClause.value.id &&
                a.committee.toLowerCase() === props.committee.toLowerCase() &&
                !a.is_passed && !a.is_published
            ).length;
        });

        const hasPublishedAmendment = computed(() => publishedAmendmentsCount.value > 0);

        // Helper functions
        const filterAndSortAmendments = (amendmentsList, clauseId = null) => {
            let filteredList = amendmentsList;

            // Filter by clause if provided
            if (clauseId) {
                filteredList = filteredList.filter(a =>
                    a.clause_id === clauseId &&
                    a.committee.toLowerCase() === props.committee.toLowerCase() &&
                    !a.is_passed // Exclude approved amendments
                );
            } else {
                filteredList = filteredList.filter(a =>
                    a.committee.toLowerCase() === props.committee.toLowerCase() &&
                    !a.is_passed // Exclude approved amendments
                );
            }

            // Sort by published status then timestamp
            return filteredList.sort((a, b) => {
                if (a.is_published && !b.is_published) return -1;
                if (!a.is_published && b.is_published) return 1;
                return new Date(b.timestamp) - new Date(a.timestamp);
            });
        };

        const formatTimestamp = (timestamp) => {
            return new Date(timestamp).toLocaleString();
        };

        // Amendment actions
        const unpublishAmendment = async (amendment) => {
            try {
                const response = await axios.post(`${BASE_URL}/amendments/${amendment.id}/unpublish`);

                // Update local state
                amendments.value = amendments.value.map(a =>
                    a.id === amendment.id ? { ...a, is_published: false } : a
                );

                // Update current clause if provided in response
                if (currentClause.value && response.data.clause) {
                    currentClause.value.content = response.data.clause.content;
                }

                GlassMessage.success('Amendment unpublished and changes reverted');
            } catch (error) {
                console.error('Error unpublishing amendment:', error);
                GlassMessage.error('Failed to unpublish amendment');
            }
        };

        const rejectAmendment = async (amendment) => {
            try {
                const response = await axios.post(`${BASE_URL}/amendments/${amendment.id}/reject`);

                // Update local state
                amendments.value = amendments.value.filter(a => a.id !== amendment.id);

                // Update current clause
                if (response.data.clause) {
                    currentClause.value = response.data.clause;
                }

                GlassMessage.success('Amendment rejected and comparison closed');
            } catch (error) {
                console.error('Error rejecting amendment:', error);
                GlassMessage.error('Failed to reject amendment');
            }
        };

        const approveAmendment = async (amendment) => {
            try {
                const response = await axios.post(`${BASE_URL}/amendments/${amendment.id}/approve`);

                // Update local state
                const index = amendments.value.findIndex(a => a.id === amendment.id);
                if (index !== -1) {
                    amendments.value[index] = {
                        ...amendments.value[index],
                        is_published: false,
                        is_passed: true
                    };
                }

                // Update clause content if provided
                if (response.data.clause) {
                    currentClause.value = response.data.clause;
                }

                GlassMessage.success('Amendment approved');
            } catch (error) {
                console.error('Error approving amendment:', error);
                GlassMessage.error('Failed to approve amendment');
            }
        };

        const deleteAmendment = async (amendment) => {
            try {
                await axios.delete(`${BASE_URL}/amendments/delete/${amendment.id}`);
                amendments.value = amendments.value.filter(a => a.id !== amendment.id);
                GlassMessage.success('Amendment deleted successfully');
            } catch (error) {
                console.error('Error deleting amendment:', error);
                GlassMessage.error('Failed to delete amendment');
            }
        };

        // Data fetching
        const fetchCurrentClause = async () => {
            try {
                const response = await axios.get(`${BASE_URL}/committee/${props.committee.toLowerCase()}/current-clause`);
                if (response.data) {
                    currentClause.value = response.data;
                    noPublishedClause.value = false;
                } else {
                    currentClause.value = null;
                    noPublishedClause.value = true;
                }
            } catch (error) {
                console.error('Error fetching current clause:', error);
                if (error.response?.status === 404) {
                    noPublishedClause.value = true;
                } else {
                    GlassMessage.error('Error checking current clause status');
                }
                currentClause.value = null;
            }
        };

        const fetchAmendments = async () => {
            try {
                const response = await axios.get(`${BASE_URL}/amendments`, {
                    params: { committee: props.committee.toLowerCase() }
                });
                amendments.value = response.data;
            } catch (error) {
                console.error('Error fetching amendments:', error);
                GlassMessage.error(`Failed to fetch amendments: ${error.message}`);
            }
        };

        // Socket event handlers
        const setupSocketListeners = () => {
            // Define all socket events and their handlers
            const socketEvents = {
                new_amendment: (data) => {
                    if (isRelevantToCommittee(data)) {
                        amendments.value.unshift(data);
                        GlassMessage.info(`New amendment from ${data.country}`);
                    }
                },
                clause_published: (data) => {
                    if (isRelevantToCommittee(data)) {
                        currentClause.value = data;
                        noPublishedClause.value = false;
                        fetchAmendments();
                        GlassMessage.info('New clause has been published');
                    }
                },
                clause_rejected: (data) => {
                    if (isRelevantToCommittee(data) &&
                        currentClause.value &&
                        currentClause.value.id === data.clauseId) {
                        currentClause.value = null;
                        noPublishedClause.value = true;
                        GlassMessage.warning('The current clause has been rejected');
                    }
                },
                amendment_status_changed: (data) => {
                    if (isRelevantToCommittee(data)) {
                        updateAmendmentInState(data);

                        if (data.is_published) {
                            GlassMessage.success(`Amendment from ${data.country} has been published`);
                        } else {
                            GlassMessage.warning(`Amendment from ${data.country} has been unpublished`);
                        }
                    }
                },
                amendment_rejected: (data) => {
                    if (isRelevantToCommittee(data)) {
                        amendments.value = amendments.value.filter(a => a.id !== data.amendment_id);
                        GlassMessage.warning('An amendment was rejected and removed');
                    }
                },
                clause_unpublished: (data) => {
                    if (isRelevantToCommittee(data)) {
                        noPublishedClause.value = true;
                        currentClause.value = null;
                    }
                },
                amendment_deleted: (data) => {
                    if (isRelevantToCommittee(data)) {
                        amendments.value = amendments.value.filter(a => a.id !== data.id);
                        GlassMessage.warning('An amendment was deleted');
                    }
                },
                amendment_unpublished: (data) => {
                    if (isRelevantToCommittee(data)) {
                        if (data.clause) {
                            currentClause.value = data.clause;
                        }

                        updateAmendmentInState({ id: data.id, is_published: false });

                        GlassMessage.warning(`Amendment from ${data.country || 'a country'} has been unpublished`);
                    }
                }
            };

            // Register all event listeners
            Object.entries(socketEvents).forEach(([event, handler]) => {
                socket.on(event, handler);
            });
        };

        // Socket event helper functions
        const isRelevantToCommittee = (data) => {
            return data.committee && data.committee.toLowerCase() === props.committee.toLowerCase();
        };

        const updateAmendmentInState = (data) => {
            const index = amendments.value.findIndex(a => a.id === data.id);
            if (index !== -1) {
                amendments.value[index] = {
                    ...amendments.value[index],
                    ...data
                };
            }
        };

        // Amendment editor methods
        const openAmendmentEditor = async (amendment) => {
            try {
                const response = await axios.get(`${BASE_URL}/amendments/${amendment.id}`);
                selectedAmendment.value = response.data;
                const content = response.data.amended_clause ||
                    (currentClause.value ? currentClause.value.content : '');
                editingContent.value = content;

                // Update shared state when opening the editor
                if (currentClause.value) {
                    amendmentState.updateAmendmentEdit(
                        content,
                        response.data.id,
                        currentClause.value.content
                    );
                }

                isEditorVisible.value = true;
            } catch (error) {
                console.error('Error fetching amendment data:', error);
                GlassMessage.error('Failed to load amendment data');
            }
        };

        const handleEditorChange = async (newContent) => {
            editingContent.value = newContent;

            // Update the shared state with new content
            if (selectedAmendment.value) {
                amendmentState.updateAmendmentEdit(
                    newContent,
                    selectedAmendment.value.id,
                    currentClause.value ? currentClause.value.content : ''
                );
            }

            if (selectedAmendment.value && isEditorVisible.value) {
                try {
                    await axios.post(`${BASE_URL}/amendments/${selectedAmendment.value.id}/update-amended-clause`, {
                        amended_clause: newContent
                    });
                } catch (error) {
                    console.error('Error updating amended clause:', error);
                }
            }
        };

        const closeEditor = () => {
            if (selectedAmendment.value && editingContent.value) {
                handleEditorChange(editingContent.value);
            }
            isEditorVisible.value = false;
            selectedAmendment.value = null;
            editingContent.value = '';

            // Clear shared state when closing the editor
            amendmentState.clearAmendmentEdit();
        };

        // Fixed saveChanges function to handle the null reference issue
        const saveChanges = async () => {
            // Double-check both values are present to avoid null reference
            if (!currentClause.value) {
                GlassMessage.error('No current clause available');
                return;
            }

            if (!selectedAmendment.value) {
                GlassMessage.error('No amendment selected');
                return;
            }

            // 检查是否已经有一个amendment正在debate
            if (hasPublishedAmendment.value) {
                GlassMessage.error('There is already an amendment under debate. Please unpublish it first before publishing another one.');
                return;
            }

            try {
                const amendmentId = selectedAmendment.value.id;
                if (!amendmentId) {
                    GlassMessage.error('Invalid amendment ID');
                    return;
                }

                const response = await axios.put(`${BASE_URL}/committee/${props.committee}/current-clause`, {
                    content: editingContent.value,
                    amendment_id: amendmentId,
                    amendment_text: editingContent.value,
                });

                // Update local state
                currentClause.value = {
                    ...currentClause.value,
                    content: editingContent.value,
                    is_amended: true
                };

                updateAmendmentInState({
                    id: amendmentId,
                    under_debate: true,
                    is_published: true
                });

                // Clear shared state after saving
                amendmentState.clearAmendmentEdit();

                GlassMessage.success('Amendment is now under debate');
                closeEditor();
            } catch (error) {
                console.error('Error saving changes:', error);
                if (error.response?.status === 409) {
                    GlassMessage.error(error.response.data.error);
                } else {
                    GlassMessage.error('Failed to start debate');
                }
            }
        };

        // UI interaction methods
        const handleAmendmentClick = (amendmentId) => {
            activeAmendment.value = activeAmendment.value === amendmentId ? null : amendmentId;
        };

        // Approved amendment methods
        const showApprovedAmendmentDialog = (amendment) => {
            selectedApprovedAmendment.value = amendment;
            isApprovedAmendmentVisible.value = true;
        };

        const closeApprovedAmendmentDialog = () => {
            isApprovedAmendmentVisible.value = false;
            selectedApprovedAmendment.value = null;
        };

        // Text truncation
        const truncateText = (text, maxLength) => {
            if (text.length > maxLength) {
                return text.slice(0, maxLength) + '...';
            }
            return text;
        };

        // New methods for Current Clause Dialog
        const showCurrentClauseDialog = () => {
            isCurrentClauseVisible.value = true;
        };

        const closeCurrentClauseDialog = () => {
            isCurrentClauseVisible.value = false;
        };

        // Draggable functionality
        const startDrag = (event) => {
            // Prevent dialog from opening when starting drag
            event.stopPropagation();

            isDragging.value = true;
            dragOffset.value = {
                x: event.clientX - buttonPosition.value.x,
                y: event.clientY - buttonPosition.value.y
            };

            document.addEventListener('mousemove', onDrag);
            document.addEventListener('mouseup', stopDrag);
        };

        const onDrag = (event) => {
            if (isDragging.value) {
                buttonPosition.value = {
                    x: event.clientX - dragOffset.value.x,
                    y: event.clientY - dragOffset.value.y
                };

                // Keep button within viewport bounds
                const button = document.querySelector('.floating-clause-button');
                if (button) {
                    const buttonWidth = button.offsetWidth;
                    const buttonHeight = button.offsetHeight;

                    if (buttonPosition.value.x < 0) buttonPosition.value.x = 0;
                    if (buttonPosition.value.y < 0) buttonPosition.value.y = 0;
                    if (buttonPosition.value.x > window.innerWidth - buttonWidth) {
                        buttonPosition.value.x = window.innerWidth - buttonWidth;
                    }
                    if (buttonPosition.value.y > window.innerHeight - buttonHeight) {
                        buttonPosition.value.y = window.innerHeight - buttonHeight;
                    }
                }
            }
        };

        const stopDrag = () => {
            isDragging.value = false;
            document.removeEventListener('mousemove', onDrag);
            document.removeEventListener('mouseup', stopDrag);
        };

        // Clean up event listeners when component is unmounted
        onUnmounted(() => {
            socket.disconnect();
            document.removeEventListener('mousemove', onDrag);
            document.removeEventListener('mouseup', stopDrag);
        });

        // Lifecycle hooks
        onMounted(() => {
            if (props.committee) {
                fetchCurrentClause();
                fetchAmendments();
                setupSocketListeners();
            }
        });

        // Watch for committee changes
        watch(() => props.committee, (newCommittee) => {
            if (newCommittee) {
                fetchCurrentClause();
                fetchAmendments();
            }
        });

        return {
            currentClause,
            currentClauseAmendments,
            otherAmendments,
            formatTimestamp,
            isEditorVisible,
            selectedAmendment,
            editingContent,
            activePanel,
            openAmendmentEditor,
            handleEditorChange,
            closeEditor,
            saveChanges,
            activeAmendment,
            handleAmendmentClick,
            noPublishedClause,
            unpublishAmendment,
            rejectAmendment,
            approveAmendment,
            deleteAmendment,
            approvedForClause,
            publishedAmendmentsCount,
            isApprovedAmendmentVisible,
            selectedApprovedAmendment,
            showApprovedAmendmentDialog,
            closeApprovedAmendmentDialog,
            truncateText,
            isCurrentClauseVisible,
            showCurrentClauseDialog,
            closeCurrentClauseDialog,
            buttonPosition,
            startDrag,
            totalAmendmentsCount,
            pendingAmendmentsCount,
            hasPublishedAmendment
        };
    }
};
</script>

<style scoped>
.amendments-container {
    position: relative;
    height: 100vh;
    overflow: hidden;
}

.main-content {
    height: 100%;
    overflow-y: auto;
    padding: 20px;
}

.current-clause-content {
    padding: 20px;
    color: white;
}

.clause-meta {
    margin-bottom: 20px;
    padding: 15px;
}

.clause-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
}

.clause-country {
    font-weight: bold;
    color: white;
}

.clause-stats {
    margin-top: 15px;
}

.stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item:last-child {
    border-bottom: none;
}

.stat-label {
    color: rgba(255, 255, 255, 0.8);
}

.stat-value {
    color: white;
    font-weight: bold;
}

.clause-content {
    padding: 20px;
    margin-top: 15px;
    min-height: 200px;
}

.amendment-item {
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    margin-bottom: 10px;
    overflow: hidden;
}

.amendment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 15px;
    background-color: #f5f7fa;
    cursor: pointer;
    transition: background-color 0.3s;
}

.amendment-header:hover {
    background-color: #e6e8eb;
}

.amendment-content {
    padding: 15px;
    background-color: #fff;
    border-top: 1px solid #dcdfe6;
}

.toggle-icon {
    transition: transform 0.3s;
}

.toggle-icon.is-active {
    transform: rotate(180deg);
}

.country {
    font-weight: bold;
    color: #67c23a;
    flex: 1;
}

.timestamp {
    color: #909399;
    font-size: 0.9em;
    margin: 0 15px;
}

.amendment-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
    flex-wrap: wrap;
}

.action-button {
    margin: 0;
}

.edit-button {
    margin-top: 10px;
}

.amendment-item.published {
    border: 1px solid var(--el-color-success-light-3);
    background-color: var(--el-color-success-light-9);
}

.amendment-item.published .amendment-header {
    background-color: var(--el-color-success-light-8);
}

.amendment-item.published .amendment-header:hover {
    background-color: var(--el-color-success-light-7);
}

.published-tag {
    margin: 0 8px;
}

.no-clause-warning {
    margin: 40px auto;
    max-width: 600px;
    text-align: center;
    padding: 20px;
    border-radius: 8px;
    background-color: #fffbe6;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    border: 1px solid #faecd8;
}

.no-clause-warning p {
    margin: 10px 0;
    line-height: 1.6;
    color: #606266;
}

.no-clause-warning :deep(.glass-alert) {
    background-color: transparent;
    border: none;
}

.no-clause-warning :deep(.glass-alert__title) {
    color: #e6a23c;
}

/* Editor Dialog */
.amendment-editor-dialog :deep(.el-dialog__body) {
    padding: 20px;
    min-height: 600px;
}

.editor-layout {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 20px;
    height: 100%;
    min-height: 600px;
}

.editor-main,
.reference-section {
    display: flex;
    flex-direction: column;
}

.editor-main h3,
.reference-section h3 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #303133;
    font-size: 16px;
}

.reference-section {
    border-left: 1px solid #dcdfe6;
    padding-left: 20px;
}

.amendment-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    padding: 8px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.amendment-reference-content {
    flex: 1;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 4px;
    overflow-y: auto;
    border: 1px solid #dcdfe6;
    color: #000000;
}

.amendment-reference-content * {
    color: #000000;
}

.dialog-footer {
    padding-top: 20px;
    text-align: right;
}

:deep(.el-dialog) {
    margin: 5vh auto !important;
    max-height: 80vh !important;
    height: auto !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    position: relative !important;
    top: 0 !important;
    transform: none !important;
}

:deep(.el-dialog__body) {
    flex: 1;
    overflow: auto;
    max-height: calc(80vh - 120px) !important;
    /* 减去头部和底部的高度 */
}

:deep(.glass-dialog) {
    background-color: rgba(255, 255, 255, 0.2) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
}

:deep(.el-overlay) {
    overflow: auto !important;
    display: flex !important;
    align-items: flex-start !important;
    justify-content: center !important;
    padding: 5vh 0 !important;
}

:deep(.el-overlay-dialog) {
    position: relative !important;
    display: flex !important;
    align-items: flex-start !important;
    justify-content: center !important;
    width: 100% !important;
    height: auto !important;
    max-height: 90vh !important;
    overflow: visible !important;
}

:deep(.el-dialog__header) {
    padding: 20px;
    margin-right: 0;
    border-bottom: 1px solid #dcdfe6;
}

:deep(.el-dialog__footer) {
    border-top: 1px solid #dcdfe6;
    padding: 20px;
}

.editor-main :deep(.ck-editor) {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.editor-main :deep(.ck-editor__editable_inline) {
    flex: 1;
    min-height: 400px;
}

.amendment-item.approved {
    border: 2px solid var(--el-color-success);
    background-color: var(--el-color-success-light-9);
}

.amendment-item.approved .amendment-header {
    background-color: var(--el-color-success-light-8);
}

.amendment-item.approved .amendment-header:hover {
    background-color: var(--el-color-success-light-7);
}

.amendment-preview {
    color: white;
    font-size: 0.9em;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin: 0 10px;
    max-height: 2.5em;
    line-height: 1.2;
    position: relative;
}

.amendment-preview::after {
    content: "...";
    position: absolute;
    right: 0;
    bottom: 0;
    background-color: var(--el-color-success-light-8);
    padding-left: 4px;
    color: white;
}

.amendment-preview :deep(*) {
    display: inline;
    white-space: nowrap;
    color: white !important;
}

.approved-amendment-content {
    padding: 20px;
    color: white;
}

.amendment-view-content {
    margin-top: 15px;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Glass Dialog Styling */
:deep(.glass-dialog .el-dialog__header) {
    background-color: rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

:deep(.glass-dialog .el-dialog__title) {
    color: #ffffff;
    font-weight: 600;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

:deep(.glass-dialog .el-dialog__headerbtn .el-dialog__close) {
    color: #ffffff;
}

:deep(.glass-dialog .el-dialog__body) {
    background-color: transparent;
    color: #ffffff;
}

:deep(.glass-dialog .el-dialog__footer) {
    background-color: rgba(255, 255, 255, 0.1);
    border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.glass-panel {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    color: white;
}

.glass-panel * {
    color: white !important;
}

.approved-amendment-content {
    padding: 20px;
    color: white;
}

.approved-amendment-content .amendment-info {
    margin-bottom: 15px;
}

.approved-amendment-content .country,
.approved-amendment-content .timestamp {
    color: white;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.floating-clause-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background-color: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s;
}

.floating-clause-button:hover {
    background-color: rgba(236, 245, 255, 0.9);
}

.floating-clause-button .el-icon {
    font-size: 24px;
    color: #67c23a;
}

.clause-number {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.2em;
    font-weight: bold;
    color: #67c23a;
}

/* 固定位置对话框样式 */
:deep(.fixed-position-dialog) {
    position: fixed !important;
    top: 10vh !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    margin: 0 !important;
}

:deep(.fixed-position-dialog .el-dialog__wrapper) {
    position: static !important;
}

:deep(.fixed-position-dialog .el-dialog__body) {
    max-height: 65vh !important;
    overflow-y: auto !important;
}

:deep(.fixed-position-dialog .el-dialog__header) {
    padding-top: 20px !important;
    padding-bottom: 20px !important;
}
</style>
