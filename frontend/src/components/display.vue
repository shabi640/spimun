<template>
    <div class="editor-container">
        <!-- Left Panel with Editor -->
        <div class="editor-panel">
            <div class="editor-header">
                <h2>Clause Editor</h2>
                <div class="save-status">
                    <GlassTag size="small" :type="saveStatusType" effect="light">
                        {{ saveStatusText }}
                    </GlassTag>
                </div>
            </div>
            <div class="editor-content">
                <div v-if="isPublished" class="editor-disabled-notice">
                    <GlassAlert type="info" title="Editor Locked"
                        description="This clause is published and cannot be edited. Unpublish the clause to make changes."
                        :closable="false" :show-icon="true">
                    </GlassAlert>
                </div>
                <ckeditor v-model="editorData" @input="onEditorChange" :disabled="isPublished" />
            </div>
        </div>

        <!-- Right Panel with Actions -->
        <div class="action-panel">
            <div class="action-buttons">
                <div class="button-group">
                    <GlassButton type="primary" size="large" :disabled="isPublished" @click="publishClause">
                        {{ isPublished ? 'Published' : 'Publish' }}
                    </GlassButton>
                    <GlassButton v-if="isPublished" type="warning" size="large" @click="unpublishClause">
                        Unpublish
                    </GlassButton>
                    <GlassButton type="success" size="large" :disabled="!isPublished" @click="addToResolution">
                        Add to Resolution
                    </GlassButton>
                    <GlassButton type="danger" size="large" :disabled="!isPublished" @click="showRejectDialog = true">
                        Reject Clause
                    </GlassButton>
                    <GlassButton type="success" size="large" @click="formatWithDeepseek" :loading="isFormatting">
                        Format with DeepSeek
                    </GlassButton>
                    <GlassButton type="info" size="large" @click="goBack">
                        Back to List
                    </GlassButton>
                </div>
            </div>
            <div v-if="isPublished" class="publish-info">
                <GlassAlert title="Clause Published" type="success"
                    description="This clause is now available for amendments" show-icon :closable="false">
                </GlassAlert>
            </div>
        </div>

        <!-- Formatting dialog -->
        <GlassDialog v-model="showFormattingDialog" title="DeepSeek Formatting" width="70%"
            :close-on-click-modal="false" :close-on-press-escape="false" :show-close="false">
            <div class="formatting-dialog-content">
                <p v-if="isFormatting">DeepSeek is reformatting your document... <span
                        v-if="activeEventSource">(formatting in progress, you can cancel at any time)</span></p>
                <div v-if="formattedContent" class="formatted-preview" v-html="sanitizedFormattedContent"></div>
            </div>
            <template #footer>
                <span class="dialog-footer">
                    <GlassButton @click="cancelFormatting">Cancel</GlassButton>
                    <GlassButton type="primary" @click="applyFormatting" :disabled="isFormatting || !formattedContent">
                        Apply Formatting
                    </GlassButton>
                </span>
            </template>
        </GlassDialog>

        <!-- Rejection confirmation dialog -->
        <GlassDialog v-model="showRejectDialog" title="Warning" width="400px">
            <div style="text-align: center;">
                Are you sure you want to reject this clause? It will be removed from the published list.
            </div>
            <template #footer>
                <span class="dialog-footer">
                    <GlassButton @click="showRejectDialog = false">Cancel</GlassButton>
                    <GlassButton type="warning" @click="confirmReject">Yes, reject it</GlassButton>
                </span>
            </template>
        </GlassDialog>
    </div>
</template>

<script>
import Ckeditor from './ckeditor.vue'
import axios from 'axios';
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import { GlassMessage } from '../components/ui';
import { io } from 'socket.io-client';
import DOMPurify from 'dompurify';

export default {
    name: 'ClausesView',
    components: {
        Ckeditor
    },
    props: {
        initialHtmlData: {
            type: String,
            required: true
        },
        group: {
            type: String,
            required: true
        },
        clauseId: {
            type: Number,
            required: true
        }
    },
    setup(props, { emit }) {
        const isPublished = ref(false);
        const socket = io('http://127.0.0.1:8000');
        socket.on('connect', () => {
            // Socket connected
        });

        // Add a listener for the clause_published event
        socket.on('clause_published', (data) => {
            // Clause published event received
        });

        const isFormatting = ref(false);
        const showFormattingDialog = ref(false);
        const showRejectDialog = ref(false);
        const formattedContent = ref('');
        const saveStatus = ref('saved'); // Default is 'saved'
        const lastSavedContent = ref(''); // Start empty and will be properly initialized in onMounted
        const saveTimeout = ref(null);
        const isPublishing = ref(false); // Add this to track if a publish operation is in progress
        const isRejecting = ref(false); // Add this to track if a reject operation is in progress
        const isUnpublishing = ref(false); // Add this to track if an unpublish operation is in progress
        const activeEventSource = ref(null); // Add this to track the active EventSource for cancellation

        // Check if the clause is already published when component mounts
        const checkPublishStatus = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/clause/${props.clauseId}/status`);
                isPublished.value = response.data.is_published;
            } catch (error) {
                console.error('Error checking publish status:', error);
            }
        };

        // Computed property for sanitized formatted content
        const sanitizedFormattedContent = computed(() => {
            return DOMPurify.sanitize(formattedContent.value);
        });

        // Computed properties for save status
        const saveStatusText = computed(() => {
            switch (saveStatus.value) {
                case 'saving': return 'Saving...';
                case 'saved': return 'All changes saved';
                case 'error': return 'Save failed';
                case 'editing': return 'Editing';
                default: return 'All changes saved';
            }
        });

        const saveStatusType = computed(() => {
            switch (saveStatus.value) {
                case 'saving': return 'info';
                case 'saved': return 'success';
                case 'error': return 'danger';
                case 'editing': return ''; // Use default (gray) style for editing
                default: return 'success';
            }
        });

        onMounted(() => {
            checkPublishStatus();
            // Initialize lastSavedContent with initialHtmlData from props
            lastSavedContent.value = props.initialHtmlData;
        });

        onUnmounted(() => {
            socket.disconnect();
            if (saveTimeout.value) {
                clearTimeout(saveTimeout.value);
            }
            // Make sure to close any active EventSource when component unmounts
            if (activeEventSource.value) {
                activeEventSource.value.close();
                activeEventSource.value = null;
            }
        });

        return {
            isPublished,
            socket,
            isFormatting,
            showFormattingDialog,
            showRejectDialog,
            formattedContent,
            sanitizedFormattedContent,
            saveStatus,
            saveStatusText,
            saveStatusType,
            lastSavedContent,
            saveTimeout,
            isPublishing,
            isRejecting,
            isUnpublishing,
            activeEventSource
        };
    },
    data() {
        return {
            editorData: this.initialHtmlData
        }
    },
    watch: {
        editorData: {
            handler(newContent) {
                // Trigger debounced auto-save when content changes
                this.debouncedAutoSave();
            },
            deep: true,
            immediate: true // Add immediate: true to check on initialization
        }
    },
    methods: {
        onEditorChange() {
            // Set status to editing when user is typing, but only if the clause is not published
            if (!this.isPublished) {
                this.saveStatus = 'editing';
            }
        },
        debouncedAutoSave() {
            // Clear any existing timeout
            if (this.saveTimeout) {
                clearTimeout(this.saveTimeout);
            }

            // If the clause is published, don't trigger auto-save
            if (this.isPublished) {
                this.saveStatus = 'saved';
                return;
            }

            // If content hasn't changed since last save, don't trigger save
            if (this.editorData === this.lastSavedContent) {
                this.saveStatus = 'saved';
                return;
            }

            // Set status to editing while waiting to save
            this.saveStatus = 'editing';

            // Set a new timeout (1.5 seconds delay)
            this.saveTimeout = setTimeout(() => {
                this.autoSave();
            }, 1500);
        },
        async autoSave() {
            try {
                // Don't save if content hasn't changed since last save
                if (this.editorData === this.lastSavedContent) {
                    this.saveStatus = 'saved';
                    return;
                }

                // Don't save if the clause is published
                if (this.isPublished) {
                    this.saveStatus = 'saved';
                    return;
                }

                this.saveStatus = 'saving';

                // Call the backend endpoint to update the clause content
                await axios.post(`http://127.0.0.1:8000/clause/${this.clauseId}/update-content`, {
                    formatted_content: this.editorData
                });

                // Update last saved content
                this.lastSavedContent = this.editorData;
                this.saveStatus = 'saved';

                // No need to reset status after a delay anymore since 'saved' is the default state
            } catch (error) {
                console.error('Auto-save failed:', error);
                this.saveStatus = 'error';

                // Show an error message only if it's a significant error
                if (error.response && error.response.status !== 409) {
                    GlassMessage.error({
                        message: 'Failed to auto-save content. Please try again.',
                        duration: 3000
                    });
                }

                // Revert to 'editing' status after 3 seconds if there was an error
                setTimeout(() => {
                    if (this.saveStatus === 'error' && this.editorData !== this.lastSavedContent) {
                        this.saveStatus = 'editing';
                    }
                }, 3000);
            }
        },
        async confirmReject() {
            // Prevent multiple calls in quick succession
            if (this.isRejecting) {
                return;
            }

            try {
                this.isRejecting = true; // Set flag to indicate reject is in progress

                const response = await axios.post(`http://127.0.0.1:8000/clause/${this.clauseId}/reject`);

                if (response.data.success) {
                    this.isPublished = false;

                    // Emit socket event for real-time updates
                    this.socket.emit('clause_rejected', {
                        clauseId: this.clauseId,
                        committee: this.group,
                        silent: true // Add silent flag to prevent duplicate messages
                    });

                    // Close the dialog
                    this.showRejectDialog = false;

                    // Show success message
                    GlassMessage.success('Clause rejected successfully');

                    // Go back to the list view immediately
                    this.goBack();
                }
            } catch (error) {
                GlassMessage.error('Failed to reject clause');
                console.error('Error rejecting clause:', error);
                // Close the dialog even if there's an error
                this.showRejectDialog = false;
            } finally {
                // Reset the rejecting flag after a short delay to prevent accidental double-clicks
                setTimeout(() => {
                    this.isRejecting = false;
                }, 1000);
            }
        },
        async publishClause() {
            // Prevent multiple calls in quick succession
            if (this.isPublishing) {
                return;
            }

            try {
                this.isPublishing = true; // Set flag to indicate publish is in progress

                const response = await axios.post(`http://127.0.0.1:8000/clause/${this.clauseId}/publish`, {
                    committee: this.group,
                    content: this.editorData
                });

                if (response.data.success) {
                    this.isPublished = true;

                    // Show success message immediately after API call succeeds
                    GlassMessage.success('Clause published successfully');

                    // Emit socket event for real-time updates with silent flag
                    this.socket.emit('clause_published', {
                        clauseId: this.clauseId,
                        committee: this.group,
                        content: this.editorData,
                        silent: true // Explicitly set to true to prevent other components from showing messages
                    });
                }
            } catch (error) {
                if (error.response && error.response.status === 409) {
                    GlassMessage.warning('Another clause is already published for this committee');
                } else {
                    GlassMessage.error('Failed to publish clause');
                    console.error('Error publishing clause:', error);
                }
            } finally {
                // Reset the publishing flag after a short delay to prevent accidental double-clicks
                setTimeout(() => {
                    this.isPublishing = false;
                }, 1000);
            }
        },
        async unpublishClause() {
            // Add a reactive variable to track unpublish state
            if (this.isUnpublishing) {
                return;
            }

            try {
                this.isUnpublishing = true; // Set flag to indicate unpublish is in progress

                const response = await axios.post(`http://127.0.0.1:8000/clause/${this.clauseId}/unpublish`);

                if (response.data.success) {
                    this.isPublished = false;

                    // Show success message immediately after API call succeeds
                    GlassMessage.success('Clause unpublished successfully');

                    // Emit socket event for real-time updates with silent flag
                    this.socket.emit('clause_unpublished', {
                        clauseId: this.clauseId,
                        committee: this.group,
                        silent: true // Explicitly set to true to prevent other components from showing messages
                    });
                }
            } catch (error) {
                GlassMessage.error('Failed to unpublish clause');
                console.error('Error unpublishing clause:', error);
            } finally {
                // Reset the unpublishing flag after a short delay to prevent accidental double-clicks
                setTimeout(() => {
                    this.isUnpublishing = false;
                }, 1000);
            }
        },
        addToResolution() {
            axios.post(`http://127.0.0.1:8000/api/resolutions/${this.group}`, {
                data: this.editorData,
                clauseId: this.clauseId
            })
                .then(() => {
                    GlassMessage.success('Added to resolution successfully');
                    this.isPublished = false;
                    this.goBack();
                })
                .catch(error => {
                    GlassMessage.error('Failed to add to resolution');
                    console.error('Error adding to resolution:', error);
                });
        },
        async formatWithDeepseek() {
            try {
                this.isFormatting = true;
                this.showFormattingDialog = true;
                this.formattedContent = ''; // Clear previous content

                // Store the EventSource instance so we can close it when canceling
                this.activeEventSource = null;

                // Call the backend endpoint to start the formatting process
                await axios.post(`http://127.0.0.1:8000/clause/${this.clauseId}/format-with-deepseek`);

                // Use Server-Sent Events to handle streaming response
                const eventSource = new EventSource(`http://127.0.0.1:8000/clause/${this.clauseId}/stream-format`);
                this.activeEventSource = eventSource;

                // Initialize an empty string to build up the response
                let streamedContent = '';

                // Handle incoming data chunks
                eventSource.onmessage = (event) => {
                    const data = JSON.parse(event.data);

                    if (data.error) {
                        GlassMessage.error(`Error: ${data.error}`);
                        eventSource.close();
                        this.activeEventSource = null;
                        this.isFormatting = false;
                        return;
                    }

                    if (data.done) {
                        // Formatting is complete
                        // Apply post-processing to improve list formatting
                        if (streamedContent) {
                            streamedContent = this.improveListFormatting(streamedContent);
                            this.formattedContent = streamedContent;
                        }
                        eventSource.close();
                        this.activeEventSource = null;
                        this.isFormatting = false;
                        return;
                    }

                    if (data.chunk) {
                        // Add the new chunk to our content
                        streamedContent += data.chunk;

                        // Apply formatting in real-time to the accumulated content
                        const formattedStreamContent = this.improveListFormatting(streamedContent);
                        this.formattedContent = formattedStreamContent;
                    }

                    // If we receive the final content in one go
                    if (data.final_content) {
                        // Apply post-processing to improve list formatting
                        const processedContent = this.improveListFormatting(data.final_content);
                        this.formattedContent = processedContent;
                        eventSource.close();
                        this.activeEventSource = null;
                        this.isFormatting = false;
                    }
                };

                // Handle errors
                eventSource.onerror = (error) => {
                    console.error('EventSource error:', error);
                    eventSource.close();
                    this.activeEventSource = null;
                    GlassMessage.error('Error streaming formatted content');
                    this.isFormatting = false;
                };
            } catch (error) {
                GlassMessage.error('Failed to format document with DeepSeek.');
                console.error(error);
                this.isFormatting = false;
                if (this.activeEventSource) {
                    this.activeEventSource.close();
                    this.activeEventSource = null;
                }
            }
        },
        // Helper method to improve list formatting in HTML
        improveListFormatting(html) {
            // Create a temporary DOM element to manipulate the HTML
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;

            // Process all lists to ensure proper indentation and structure
            const processLists = (element) => {
                // Process all unordered lists
                const ulElements = element.querySelectorAll('ul');
                ulElements.forEach(ul => {
                    ul.style.paddingLeft = '2em';
                    ul.style.marginTop = '0.5em';
                    ul.style.marginBottom = '0.5em';

                    // Process list items within this list
                    const liElements = ul.querySelectorAll('li');
                    liElements.forEach(li => {
                        li.style.marginBottom = '0.5em';
                        li.style.lineHeight = '1.5';

                        // If this list item contains a paragraph, ensure proper spacing
                        const paragraphs = li.querySelectorAll('p');
                        paragraphs.forEach(p => {
                            p.style.marginTop = '0.25em';
                            p.style.marginBottom = '0.25em';
                        });
                    });
                });

                // Process all ordered lists
                const olElements = element.querySelectorAll('ol');
                olElements.forEach(ol => {
                    ol.style.paddingLeft = '2em';
                    ol.style.marginTop = '0.5em';
                    ol.style.marginBottom = '0.5em';

                    // Process list items within this list
                    const liElements = ol.querySelectorAll('li');
                    liElements.forEach(li => {
                        li.style.marginBottom = '0.5em';
                        li.style.lineHeight = '1.5';

                        // If this list item contains a paragraph, ensure proper spacing
                        const paragraphs = li.querySelectorAll('p');
                        paragraphs.forEach(p => {
                            p.style.marginTop = '0.25em';
                            p.style.marginBottom = '0.25em';
                        });
                    });
                });
            };

            // Apply the processing
            processLists(tempDiv);

            // Return the improved HTML
            return tempDiv.innerHTML;
        },
        async applyFormatting() {
            try {
                this.isFormatting = true;

                // Ensure the formatted content has proper list formatting before applying
                const finalFormattedContent = this.improveListFormatting(this.formattedContent);

                // Call the backend endpoint to update the clause content
                await axios.post(`http://127.0.0.1:8000/clause/${this.clauseId}/update-content`, {
                    formatted_content: finalFormattedContent
                });

                // Update the local content
                this.editorData = finalFormattedContent;

                // Close the dialog
                this.showFormattingDialog = false;
                this.isFormatting = false;

                GlassMessage.success('Document formatted successfully');
            } catch (error) {
                GlassMessage.error('Failed to apply formatting.');
                console.error(error);
                this.isFormatting = false;
            }
        },
        cancelFormatting() {
            // Stop the generation by closing the EventSource connection
            if (this.activeEventSource) {
                this.activeEventSource.close();
                this.activeEventSource = null;

                // Also notify the backend to stop generation if needed
                axios.post(`http://127.0.0.1:8000/clause/${this.clauseId}/cancel-format`)
                    .catch(error => {
                        console.error('Error while canceling format:', error);
                    });
            }

            this.formattedContent = '';
            this.showFormattingDialog = false;
            this.isFormatting = false;
        },
        goBack() {
            this.$emit('go-back');
        }
    }
}
</script>

<style scoped>
.editor-container {
    display: flex;
    height: 100vh;
    width: 100%;
    background-color: #f5f7fa;
}

.editor-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 20px;
    background-color: white;
    border-right: 1px solid #dcdfe6;
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.editor-header {
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #ebeef5;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.editor-header h2 {
    color: #303133;
    margin: 0;
}

.save-status {
    display: flex;
    align-items: center;
}

.save-status .el-tag {
    padding: 0 10px;
    height: 24px;
    line-height: 24px;
    border-radius: 12px;
    transition: all 0.3s ease;
}

.editor-content {
    flex: 1;
    overflow-y: auto;
}

.action-panel {
    width: 300px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.action-buttons {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.button-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
}

.button-group .el-button {
    width: 100%;
    margin-left: 0 !important;
    height: 50px;
    font-size: 16px;
}

.publish-info {
    margin-top: 20px;
}

.formatting-dialog-content {
    min-height: 300px;
    max-height: 60vh;
    overflow-y: auto;
}

.formatted-preview {
    border: none;
    border-radius: 4px;
    padding: 15px;
    background-color: transparent;
    margin-top: 10px;
    color: white;
}

/* Ensure consistent font color for all elements in formatted preview */
.formatted-preview *,
.formatted-preview p,
.formatted-preview h1,
.formatted-preview h2,
.formatted-preview h3,
.formatted-preview h4,
.formatted-preview h5,
.formatted-preview h6,
.formatted-preview li,
.formatted-preview span,
.formatted-preview div,
.formatted-preview a,
.formatted-preview table,
.formatted-preview td,
.formatted-preview th,
.formatted-preview blockquote,
.formatted-preview pre,
.formatted-preview code {
    color: white !important;
}

/* Fix list indentation in formatted preview */
.formatted-preview ol,
.formatted-preview ul {
    padding-left: 2em;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}

.formatted-preview ol ol,
.formatted-preview ul ul,
.formatted-preview ol ul,
.formatted-preview ul ol {
    padding-left: 2em;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}

.formatted-preview li {
    margin-bottom: 0.5em;
    line-height: 1.5;
    position: relative;
}

/* Improve nested list indentation with visual indicators */
.formatted-preview ul>li {
    list-style-type: disc;
    padding-left: 0.5em;
}

.formatted-preview ul>li>ul>li {
    list-style-type: circle;
}

.formatted-preview ul>li>ul>li>ul>li {
    list-style-type: square;
}

/* Improve spacing between list items */
.formatted-preview li+li {
    margin-top: 0.5em;
}

/* Ensure proper alignment of multi-line list items */
.formatted-preview li>p {
    margin-top: 0.25em;
    margin-bottom: 0.25em;
}

/* Handle different list styles */
.formatted-preview ol[type="1"],
.formatted-preview ol[style*="list-style-type:decimal"] {
    list-style-type: decimal;
}

.formatted-preview ol[type="a"],
.formatted-preview ol[style*="list-style-type:lower-alpha"],
.formatted-preview ol[style*="list-style-type:lower-latin"] {
    list-style-type: lower-alpha;
}

.formatted-preview ol[type="A"],
.formatted-preview ol[style*="list-style-type:upper-alpha"],
.formatted-preview ol[style*="list-style-type:upper-latin"] {
    list-style-type: upper-alpha;
}

.formatted-preview ol[type="i"],
.formatted-preview ol[style*="list-style-type:lower-roman"] {
    list-style-type: lower-roman;
}

.formatted-preview ol[type="I"],
.formatted-preview ol[style*="list-style-type:upper-roman"] {
    list-style-type: upper-roman;
}

.editor-disabled-notice {
    margin-bottom: 15px;
}

/* Transitions */
.el-button {
    transition: all 0.3s ease;
}

.el-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-button:active {
    transform: translateY(0);
}
</style>
