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

        <div v-if="fileList.length > 0" class="glass-upload__file-list">
            <div v-for="(file, index) in fileList" :key="index" class="glass-upload__file-item">
                <div class="glass-upload__file-info">
                    <div class="glass-upload__file-name">{{ file.name }}</div>
                    <div class="glass-upload__file-size">{{ formatSize(file.size) }}</div>
                </div>
                <button class="glass-upload__remove-btn" @click.stop="removeFile(index)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </button>
            </div>
        </div>

        <div class="glass-upload__actions">
            <slot name="actions">
                <GlassButton v-if="fileList.length > 0 && !autoUpload" type="primary" @click="submitUpload">
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
        }
    },
    emits: ['on-success', 'on-error', 'on-progress', 'on-exceed', 'on-remove', 'on-change'],
    data() {
        return {
            isDragging: false,
            fileList: [],
            uploadingFiles: {}
        };
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
            this.handleFiles(files);
        },
        triggerFileInput() {
            this.$refs.fileInput.click();
        },
        handleFileChange(e) {
            const files = e.target.files;
            if (!files) return;
            this.handleFiles(files);
            // Reset the input so the same file can be uploaded again
            this.$refs.fileInput.value = null;
        },
        handleFiles(files) {
            const uploadFiles = Array.from(files);

            if (this.limit && this.fileList.length + uploadFiles.length > this.limit) {
                this.$emit('on-exceed', uploadFiles, this.fileList);
                return;
            }

            uploadFiles.forEach(file => {
                this.fileList.push(file);
            });

            this.$emit('on-change', this.fileList);

            if (this.autoUpload) {
                this.submitUpload();
            }
        },
        submitUpload() {
            this.fileList.forEach((file, index) => {
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
                    this.$emit('on-success', response, file, this.fileList);
                    this.uploadingFiles[index] = false;
                })
                .catch(error => {
                    this.$emit('on-error', error, file, this.fileList);
                    this.uploadingFiles[index] = false;
                });
        },
        removeFile(index) {
            const file = this.fileList[index];
            this.fileList.splice(index, 1);
            this.$emit('on-remove', file, this.fileList);
            this.$emit('on-change', this.fileList);
        },
        clearFiles() {
            this.fileList = [];
            this.$emit('on-change', this.fileList);
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