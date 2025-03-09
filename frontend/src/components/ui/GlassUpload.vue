<template>
    <div class="glass-upload">
        <div class="glass-upload__input" :class="{ 'glass-upload--drag': isDragging }"
            @dragover.prevent="handleDragOver" @dragleave.prevent="handleDragLeave" @drop.prevent="handleDrop"
            @click="triggerFileInput">
            <input ref="fileInput" type="file" :accept="accept" :multiple="multiple" class="glass-upload__file-input"
                @change="handleFileChange" />
            <div class="glass-upload__content">
                <div class="glass-upload__icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="17 8 12 3 7 8"></polyline>
                        <line x1="12" y1="3" x2="12" y2="15"></line>
                    </svg>
                </div>
                <div class="glass-upload__text">
                    <slot>
                        <p>Drop file here or <span class="glass-upload__browse">click to browse</span></p>
                    </slot>
                </div>
            </div>
        </div>

        <div class="glass-upload__actions">
            <slot name="actions">
                <GlassButton v-if="internalFileList.length > 0 && !autoUpload" type="primary" @click="submitUpload">
                    Upload
                </GlassButton>
            </slot>
        </div>
    </div>
</template>

<script>
import GlassButton from './GlassButton.vue';
import axios from 'axios';

export default {
    name: 'GlassUpload',
    components: {
        GlassButton
    },
    props: {
        action: {
            type: String,
            required: true
        },
        accept: {
            type: String,
            default: ''
        },
        multiple: {
            type: Boolean,
            default: false
        },
        autoUpload: {
            type: Boolean,
            default: false
        },
        headers: {
            type: Object,
            default: () => ({})
        },
        data: {
            type: Object,
            default: () => ({})
        },
        withCredentials: {
            type: Boolean,
            default: false
        },
        limit: {
            type: Number,
            default: 0
        },
        fileList: {
            type: Array,
            default: () => []
        }
    },
    emits: ['on-success', 'on-error', 'on-progress', 'on-exceed', 'on-remove', 'on-change', 'upload-requested'],
    data() {
        return {
            isDragging: false,
            internalFileList: [],
            uploadingFiles: {}
        };
    },
    watch: {
        fileList: {
            handler(newFileList) {
                // Update internal file list when the prop changes
                this.internalFileList = [...newFileList];
                console.log('GlassUpload fileList prop changed:', this.internalFileList);
            },
            immediate: true,
            deep: true
        }
    },
    methods: {
        handleDragOver() {
            this.isDragging = true;
        },
        handleDragLeave() {
            this.isDragging = false;
        },
        handleDrop(e) {
            this.isDragging = false;
            const files = e.dataTransfer.files;
            if (!files) return;

            // Only handle dropped files if none are already selected
            if (this.internalFileList.length === 0) {
                this.handleFiles(files);
            }
        },
        triggerFileInput() {
            // Only allow triggering file input if no files are selected
            if (this.internalFileList.length === 0) {
                this.$refs.fileInput.click();
            }
        },
        handleFileChange(e) {
            const files = e.target.files;
            if (!files) return;

            // Only handle files if none are already selected
            if (this.internalFileList.length === 0) {
                this.handleFiles(files);
            }

            // Reset the input so the same file can be uploaded again
            this.$refs.fileInput.value = null;
        },
        handleFiles(files) {
            const uploadFiles = Array.from(files);

            if (this.limit && this.internalFileList.length + uploadFiles.length > this.limit) {
                this.$emit('on-exceed', uploadFiles, this.internalFileList);
                return;
            }

            uploadFiles.forEach(file => {
                this.internalFileList.push(file);
            });

            this.$emit('on-change', this.internalFileList[0], this.internalFileList);

            if (this.autoUpload) {
                this.submitUpload();
            }
        },
        submitUpload() {
            // Emit an event instead of handling uploads directly
            // This allows parent components to handle the upload if desired
            this.$emit('upload-requested', this.internalFileList);

            // Skip internal upload handling if a listener exists for upload-requested event
            // This check needs to be adapted based on the Vue version (2 or 3)
            const hasUploadListener =
                // Vue 2 style
                (this.$listeners && this.$listeners['upload-requested']) ||
                // Vue 3 style (check if any listeners exist for this event)
                this._events && this._events['upload-requested'] && this._events['upload-requested'].length > 0;

            if (hasUploadListener) {
                console.log('Parent component is handling the upload, skipping internal upload');
                return;
            }

            // Only perform uploads directly if no parent is handling it
            console.log('No parent handler found, using internal upload mechanism');
            this.internalFileList.forEach((file, index) => {
                if (this.uploadingFiles[index]) return;
                this.uploadFile(file, index);
            });
        },
        uploadFile(file, index) {
            const formData = new FormData();
            formData.append('file', file);

            // Add additional data if provided
            if (this.data) {
                Object.keys(this.data).forEach(key => {
                    formData.append(key, this.data[key]);
                });
            }

            const config = {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    ...this.headers
                },
                withCredentials: this.withCredentials,
                onUploadProgress: progressEvent => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    this.$emit('on-progress', { file, percent: percentCompleted });
                }
            };

            this.uploadingFiles[index] = true;

            axios.post(this.action, formData, config)
                .then(response => {
                    this.$emit('on-success', response, file, this.internalFileList);
                    this.uploadingFiles[index] = false;
                })
                .catch(error => {
                    this.$emit('on-error', error, file, this.internalFileList);
                    this.uploadingFiles[index] = false;
                });
        },
        removeFile(index) {
            const file = this.internalFileList[index];
            this.internalFileList.splice(index, 1);
            this.$emit('on-remove', file, this.internalFileList);
            this.$emit('on-change', file, this.internalFileList);
        },
        clearFiles() {
            this.internalFileList = [];
            this.$emit('on-change', null, this.internalFileList);
        },
        formatSize(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }
    }
};
</script>

<style scoped>
.glass-upload {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.glass-upload__input {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 2px dashed rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    padding: 30px;
    text-align: center;
    cursor: pointer;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: all 0.3s;
}

.glass-upload__input:hover {
    border-color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.15);
}

.glass-upload--drag {
    border-color: rgba(64, 158, 255, 0.5);
    background: rgba(64, 158, 255, 0.1);
}

.glass-upload__file-input {
    display: none;
}

.glass-upload__content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}

.glass-upload__icon {
    color: rgba(255, 255, 255, 0.7);
}

.glass-upload__text {
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
}

.glass-upload__browse {
    color: var(--primary-color, #409eff);
    text-decoration: underline;
}

.glass-upload__file-list {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.glass-upload__file-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
}

.glass-upload__file-info {
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.glass-upload__file-name {
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.glass-upload__file-size {
    color: rgba(255, 255, 255, 0.5);
    font-size: 12px;
}

.glass-upload__remove-btn {
    border: none;
    background: transparent;
    cursor: pointer;
    color: rgba(255, 255, 255, 0.5);
    padding: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s;
}

.glass-upload__remove-btn:hover {
    color: rgba(255, 255, 255, 0.9);
    background: rgba(255, 255, 255, 0.1);
}

.glass-upload__actions {
    margin-top: 15px;
    display: flex;
    justify-content: flex-end;
}
</style>