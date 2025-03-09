<template>
    <div class="upload-container">
        <!-- Committee Selection -->
        <div class="committee-selector">
            <h3>Select Committee:</h3>
            <div class="slider-selector">
                <div class="slider-track">
                    <div class="slider-indicator" :style="{ left: indicatorPosition }"></div>
                    <div class="slider-option" :class="{ active: selectedGroup === 'junior' }"
                        @click="selectCommittee('junior')">
                        Junior
                    </div>
                    <div class="slider-option" :class="{ active: selectedGroup === 'senior' }"
                        @click="selectCommittee('senior')">
                        Senior
                    </div>
                    <div class="slider-option security-council"
                        :class="{ active: selectedGroup === 'security council' }"
                        @click="selectCommittee('security council')">
                        Security Council
                    </div>
                </div>
            </div>
            <div class="selected-committee">
                Current Committee: <span class="selected-value">{{ capitalize(selectedGroup) }}</span>
            </div>
        </div>

        <!-- Upload Section -->
        <div class="upload-section">
            <h3>Upload Clause Document:</h3>
            <GlassUpload ref="uploadRef" class="upload-demo" :action="uploadUrl" :auto-upload="false" accept=".docx"
                :on-change="handleChange" :file-list="fileList" :headers="uploadHeaders" :on-success="onUploadSuccess"
                :on-error="onUploadError" :before-upload="beforeUpload" :on-progress="onUploadProgress"
                :on-remove="handleRemove" @upload-requested="handleUploadRequested" drag>
                <template #default>
                    <div class="upload-area-container">
                        <!-- File Selection Area (shown only when no file is selected) -->
                        <div v-if="fileList.length === 0" class="upload-drag-area" @click.stop>
                            <!-- 隐藏的文件输入框 -->
                            <input type="file" ref="manualFileInput" accept=".docx" style="display: none;"
                                @change="manualFileChange" />

                            <!-- 简洁的上传区域 -->
                            <div class="upload-content" @click.stop="selectFile">
                                <GlassIcon name="edit" size="large" color="primary" />
                                <div class="upload-text">Drop document here or click to select</div>
                            </div>
                        </div>

                        <!-- Selected File Display (shown only when a file is selected) -->
                        <div v-else class="selected-file-display">
                            <div class="selected-file-info">
                                <GlassIcon name="edit" size="medium" color="primary" style="margin-right: 10px;" />
                                <div>
                                    <div class="selected-file-name">{{ fileList[0]?.name }}</div>
                                    <div class="selected-file-type">Word Document (.docx)</div>
                                </div>
                            </div>
                            <GlassButton type="default" size="small" @click="handleRemove(fileList[0])"
                                class="remove-btn-inline">
                                <GlassIcon name="close" size="small" color="danger" />
                                Clear
                            </GlassButton>
                        </div>
                    </div>
                </template>

                <!-- 使用actions插槽来定制上传按钮 -->
                <template #actions>
                    <div class="upload-actions">
                        <GlassButton class="custom-upload-button" type="primary" @click="submitUpload"
                            :loading="uploading" :disabled="fileList.length === 0"
                            style="background: linear-gradient(135deg, rgba(79, 236, 184, 0.8), rgba(79, 236, 184, 0.6)); border: none; padding: 10px 20px; box-shadow: 0 4px 15px rgba(79, 236, 184, 0.3);">
                            <GlassIcon name="edit" size="small" color="primary" style="margin-right: 10px;" />
                            {{ uploading ? 'Uploading...' : 'Upload Document' }}
                        </GlassButton>
                    </div>
                </template>
            </GlassUpload>

            <!-- Upload Progress and Status -->
            <div v-if="uploading" class="progress-container"
                style="margin-top: 15px; padding: 10px; background: rgba(255, 255, 255, 0.1); border-radius: 6px;">
                <div style="font-size: 14px; margin-bottom: 5px;">Uploading: {{ uploadProgress }}%</div>
                <div style="height: 10px; background: rgba(0, 0, 0, 0.2); border-radius: 5px; overflow: hidden;">
                    <div style="height: 100%; background: rgba(79, 236, 184, 0.5); transition: width 0.3s ease;"
                        :style="{ width: `${uploadProgress}%` }"></div>
                </div>
            </div>

            <div v-if="uploadSuccess" class="success-container"
                style="margin-top: 15px; padding: 10px; background: rgba(79, 236, 184, 0.1); border-radius: 6px; display: flex; align-items: center;">
                <GlassIcon name="check" size="small" color="success" style="margin-right: 10px;" />
                <span>Document uploaded successfully!</span>
            </div>
        </div>

        <!-- Uploaded Files Table -->
        <div class="uploaded-files">
            <h3>Uploaded Files for {{ capitalize(selectedGroup) }}:</h3>
            <div v-if="uploadedFiles.length === 0" class="no-files">
                <GlassEmpty description="No files uploaded yet" />
            </div>
            <div v-else class="files-list">
                <table class="custom-table">
                    <thead>
                        <tr>
                            <th>Filename</th>
                            <th>Country</th>
                            <th>Upload Time</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="file in uploadedFiles" :key="file.id">
                            <td>
                                <div class="filename-cell">
                                    <GlassIcon name="edit" size="small" color="info" style="margin-right: 10px;" />
                                    <span>{{ file.filename }}</span>
                                </div>
                            </td>
                            <td>{{ file.country }}</td>
                            <td>{{ formatDate(file.timestamp) }}</td>
                            <td>
                                <div class="action-buttons">
                                    <router-link :to="getDocumentViewerUrl(file)">
                                        <GlassButton type="primary" size="small">View</GlassButton>
                                    </router-link>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
import {
    GlassMessage,
    GlassSelect,
    GlassOption,
    GlassUpload,
    GlassButton,
    GlassEmpty,
    GlassIcon
} from '../components/ui'
import axios from 'axios'
import { io } from 'socket.io-client'
// Replace Element Plus types with more generic types
// We can define our own UploadInstance and UploadFile types if needed
type UploadInstance = any;
type UploadFile = any;

const GROUP_KEY = 'selectedGroup'
const defaultGroup = 'junior'

// Retrieve the logged-in delegate's info from localStorage
const delegate = JSON.parse(localStorage.getItem('delegate') || 'null')
const selectedGroup = ref(delegate?.committee || localStorage.getItem(GROUP_KEY) || defaultGroup)
const uploadRef = ref<UploadInstance>()
const fileList = ref<UploadFile[]>([])
const uploadedFiles = ref<any[]>([])
const uploadUrl = ref(`http://127.0.0.1:8000/upload/${selectedGroup.value}`)
const socket = io('http://127.0.0.1:8000')
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadSuccess = ref(false)
let isUploadInProgress = false; // Flag to prevent multiple simultaneous uploads

// 计算滑动指示器的位置
const indicatorPosition = computed(() => {
    if (selectedGroup.value === 'junior') {
        return '0%';
    } else if (selectedGroup.value === 'senior') {
        return '33.33%';
    } else if (selectedGroup.value === 'security council') {
        return '66.66%';
    }
    return '0%';
})

// 选择委员会的函数
const selectCommittee = (committee: string) => {
    selectedGroup.value = committee
    fetchUploadedFiles()
}

// Headers for the upload request
const uploadHeaders = {
    'X-Country': delegate?.country || 'Unknown'
}

const fetchUploadedFiles = async () => {
    try {
        console.log(`Fetching files for committee: ${selectedGroup.value}`)
        const response = await axios.get(`http://127.0.0.1:8000/files/${selectedGroup.value}`)
        uploadedFiles.value = response.data
        console.log(`Received ${uploadedFiles.value.length} files`, uploadedFiles.value)
    } catch (error) {
        console.error('Failed to fetch files:', error)
        GlassMessage.error('Failed to fetch uploaded files')
    }
}

const handleChange = (file: UploadFile, files: UploadFile[]) => {
    console.log('handleChange called', file, files);
    if (files && files.length) {
        fileList.value = files;
    } else if (file) {
        fileList.value = [file];
    }
    // 确保文件列表更新后，按钮状态也会更新
    setTimeout(() => {
        console.log('fileList updated', fileList.value);
    }, 0);
}

const handleRemove = (file: UploadFile) => {
    fileList.value = fileList.value.filter(f => f !== file)
}

const beforeUpload = (file: UploadFile) => {
    const isDocx = file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    if (!isDocx) {
        GlassMessage.error('Only DOCX files are allowed!')
        return false
    }
    return true
}

const onUploadProgress = (event: any, file: UploadFile) => {
    uploading.value = true
    uploadProgress.value = Math.floor(event.percent)
}

const submitUpload = () => {
    // Prevent duplicate uploads
    if (isUploadInProgress) {
        console.log('Upload already in progress, ignoring duplicate request');
        return;
    }

    if (fileList.value.length === 0) {
        GlassMessage({
            message: 'Please select a file before uploading!',
            type: 'warning',
        })
        return;
    }

    uploading.value = true;
    isUploadInProgress = true; // Set flag to prevent duplicate uploads
    const selectedFile = fileList.value[0];

    // 创建FormData对象
    const formData = new FormData();
    formData.append('file', selectedFile);

    // 设置上传请求配置
    const config = {
        headers: {
            'Content-Type': 'multipart/form-data',
            ...uploadHeaders
        },
        onUploadProgress: (progressEvent: any) => {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            uploadProgress.value = percentCompleted;
        }
    };

    // 使用axios直接上传，确保只上传一次
    axios.post(uploadUrl.value, formData, config)
        .then(response => {
            onUploadSuccess(response, selectedFile);
            isUploadInProgress = false; // Reset flag after successful upload
        })
        .catch(error => {
            onUploadError(error);
            isUploadInProgress = false; // Reset flag after failed upload
        });
}

const onUploadSuccess = (response: any, file: UploadFile) => {
    uploading.value = false
    uploadProgress.value = 0
    uploadSuccess.value = true
    GlassMessage.success('File uploaded successfully!')

    // Clear the file list after successful upload
    fileList.value = []

    // 手动调用清理文件方法，确保上传列表被清除
    setTimeout(() => {
        if (uploadRef.value) {
            // 尝试多种可能的清除方法
            if (typeof uploadRef.value.clearFiles === 'function') {
                uploadRef.value.clearFiles()
            } else if (typeof uploadRef.value.abort === 'function') {
                uploadRef.value.abort()
            }
        }
    }, 100)

    // Refresh the uploaded files list
    fetchUploadedFiles()

    // 自动清除成功消息
    setTimeout(() => {
        uploadSuccess.value = false
    }, 5000)
}

const onUploadError = (error: any) => {
    uploading.value = false
    uploadProgress.value = 0
    GlassMessage.error(`Upload failed: ${error.message || 'Unknown error'}`)
}

const getDocumentViewerUrl = (row: any) => {
    return `/clauses_upload/view/${row.id}`;
}

const formatDate = (timestamp: string) => {
    return new Date(timestamp).toLocaleString()
}

// Socket.io event handlers
const setupSocketListeners = () => {
    socket.on('new_clause', (data) => {
        if (data.committee === selectedGroup.value) {
            // Check if file already exists in the list to avoid duplicates
            const exists = uploadedFiles.value.some(file => file.id === data.id)
            if (!exists) {
                uploadedFiles.value.unshift(data)
            }
        }
    })
}

// Watch for changes in selectedGroup
watch(selectedGroup, (newGroup) => {
    uploadUrl.value = `http://127.0.0.1:8000/upload/${newGroup}`
    localStorage.setItem(GROUP_KEY, newGroup)
    fetchUploadedFiles()
})

onMounted(() => {
    fetchUploadedFiles()
    setupSocketListeners()

    // Apply the directive to the upload area to prevent drag/drop when a file is selected
    if (uploadRef.value && uploadRef.value.$el) {
        const uploadInput = uploadRef.value.$el.querySelector('.glass-upload__input');
        if (uploadInput) {
            preventDropWhenFileSelected(uploadInput);
        }
    }

    // Override the GlassUpload's submitUpload method to prevent duplicate uploads
    if (uploadRef.value) {
        const originalSubmitUpload = uploadRef.value.submitUpload;
        uploadRef.value.submitUpload = function () {
            console.log('Using custom upload implementation instead of GlassUpload internal one');
            // Just call our own implementation
            submitUpload();
        };
    }
})

onUnmounted(() => {
    socket.disconnect()
})

// 自定义capitalize函数代替lodash的依赖
const capitalize = (str: string): string => {
    if (!str) return ''
    return str.charAt(0).toUpperCase() + str.slice(1)
}

// 直接保存在Vue组件中的文件引用
const manualFileInput = ref<HTMLInputElement | null>(null);

// 手动触发文件选择对话框
const selectFile = (event) => {
    // 阻止事件继续传播，避免多次触发
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }

    // 如果已经有文件被选中，不允许选择新文件
    if (fileList.value.length > 0) {
        console.log('A file is already selected. Please remove it first.');
        return;
    }

    // 确保只触发一次文件选择框
    if (manualFileInput.value && !uploading.value) {
        console.log('Triggering file selection');
        manualFileInput.value.click();
    }
};

// Modify the GlassUpload component's drop handler through a directive
const preventDropWhenFileSelected = (el) => {
    const originalDragOver = el.__dragover__;
    const originalDrop = el.__drop__;

    // Override the dragover event
    el.addEventListener('dragover', (e) => {
        if (fileList.value.length > 0) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
        if (originalDragOver) originalDragOver(e);
    });

    // Override the drop event
    el.addEventListener('drop', (e) => {
        if (fileList.value.length > 0) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
        if (originalDrop) originalDrop(e);
    });
};

// 处理手动选择的文件
const manualFileChange = (event: any) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
        // 先检查是否是docx文件
        const isDocx = selectedFile.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
        if (!isDocx) {
            GlassMessage.error('Only DOCX files are allowed!');
            return;
        }

        // 直接更新fileList
        fileList.value = [selectedFile];

        // 确保GlassUpload组件知道文件已经选择 - 修复按钮启用问题
        if (uploadRef.value) {
            if (typeof uploadRef.value.handleFiles === 'function') {
                // 确保使用正确的参数调用handleFiles
                uploadRef.value.handleFiles([selectedFile]);
            } else {
                // 如果handleFiles不可用，直接尝试通过props更新
                // 这将触发GlassUpload组件中的watch
                console.log('Using fileList prop update fallback');
            }

            // 确保与GlassUpload组件中的on-change事件签名相符
            uploadRef.value.$emit && uploadRef.value.$emit('on-change', selectedFile, [selectedFile]);
        }

        // 控制台记录以验证文件列表已更新
        console.log('Manual file selection complete, fileList:', fileList.value);

        // 重置input以便可以再次选择同一文件
        event.target.value = '';
    }
};

// Add a new function to handle the upload-requested event
const handleUploadRequested = (files) => {
    // This ensures we only use our implementation and not the component's internal one
    console.log('Upload requested from GlassUpload component, using our implementation');
    submitUpload();
};
</script>

<style>
.upload-container {
    padding: 20px;
    max-width: 950px;
    margin: 0 auto;
}

.committee-selector {
    margin-bottom: 20px;
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 10px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    position: relative;
    z-index: 10;
    /* Ensure dropdown appears above other elements */
}

.slider-selector {
    width: 100%;
    max-width: 600px;
    margin: 15px 0;
}

.slider-track {
    position: relative;
    display: flex;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    height: 50px;
    align-items: center;
    justify-content: space-between;
    padding: 4px;
    overflow: hidden;
}

.slider-indicator {
    position: absolute;
    height: calc(100% - 8px);
    width: 33.33%;
    background: rgba(79, 236, 184, 0.2);
    border: 1px solid rgba(79, 236, 184, 0.5);
    border-radius: 6px;
    transition: all 0.3s ease;
    z-index: 1;
}

.slider-option {
    flex: 1;
    text-align: center;
    padding: 10px 5px;
    cursor: pointer;
    transition: all 0.2s;
    border-radius: 6px;
    color: rgba(255, 255, 255, 0.7);
    font-weight: 500;
    position: relative;
    z-index: 2;
    user-select: none;
}

.slider-option.active {
    color: #4fecb8;
    font-weight: bold;
}

.slider-option:hover:not(.active) {
    color: white;
    background: rgba(255, 255, 255, 0.05);
}

.slider-option.security-council {
    font-size: 0.9em;
    /* 稍微减小字体大小以适应更多文本 */
}

.selected-committee {
    margin-top: 10px;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    font-size: 14px;
}

.selected-value {
    font-weight: bold;
    color: #4fecb8;
}

/* Make sure the dropdown appears above other elements */
:deep(.glass-select__dropdown) {
    z-index: 100 !important;
}

.upload-section {
    margin-bottom: 20px;
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 10px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    position: relative;
    z-index: 5;
}

.upload-demo {
    width: 100%;
    margin: 15px 0;
}

.upload-actions {
    margin-top: 15px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
}

/* 选中的文件显示样式 */
.selected-file {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.1);
    padding: 8px 12px;
    border-radius: 6px;
    max-width: 70%;
    overflow: hidden;
}

.selected-file span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-right: 10px;
}

.remove-btn {
    margin-left: auto;
    padding: 4px;
    opacity: 0.7;
}

.remove-btn:hover {
    opacity: 1;
}

.uploaded-files {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 10px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.files-list {
    margin-top: 15px;
    overflow-x: auto;
}

.custom-table {
    width: 100%;
    border-collapse: collapse;
    color: white;
}

.custom-table th,
.custom-table td {
    padding: 10px 15px;
    text-align: left;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.custom-table th {
    background-color: rgba(0, 0, 0, 0.2);
    font-weight: bold;
}

.custom-table tr:hover {
    background-color: rgba(255, 255, 255, 0.05);
}

.glass-upload__tip {
    font-size: 12px;
    color: #e6e6e6;
    margin-top: 7px;
}

.ml-3 {
    margin-left: 12px;
}

.upload-area-container {
    width: 100%;
    margin: 15px 0;
}

.upload-drag-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 120px;
    border: 2px dashed rgba(255, 255, 255, 0.3);
    border-radius: 8px;
    transition: all 0.3s;
    cursor: pointer;
    background: rgba(0, 0, 0, 0.05);
}

.upload-drag-area:hover {
    border-color: rgba(79, 236, 184, 0.5);
    background: rgba(79, 236, 184, 0.05);
}

.upload-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.upload-text {
    margin-top: 10px;
    color: #e6e6e6;
    font-size: 16px;
}

.selected-file-display {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    border-radius: 8px;
    background: rgba(79, 236, 184, 0.05);
    border: 1px solid rgba(79, 236, 184, 0.2);
    margin-bottom: 15px;
    transition: all 0.3s ease;
    width: 100%;
    box-sizing: border-box;
}

.selected-file-display:hover {
    background: rgba(79, 236, 184, 0.08);
    border-color: rgba(79, 236, 184, 0.3);
}

.selected-file-info {
    display: flex;
    align-items: center;
    flex: 1;
    min-width: 0;
    margin-right: 15px;
}

.selected-file-name {
    font-weight: bold;
    color: white;
    word-break: break-all;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
}

.selected-file-type {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.85em;
    margin-top: 3px;
}

.remove-btn-inline {
    border: none;
    background: rgba(255, 255, 255, 0.1);
    padding: 4px 10px;
    display: flex;
    align-items: center;
    gap: 5px;
    border-radius: 4px;
    color: #ff6b6b;
    font-size: 12px;
    transition: all 0.2s;
}

.remove-btn-inline:hover {
    background: rgba(255, 255, 255, 0.2);
    color: #ff4f4f;
}

.upload-progress-container {
    margin-top: 15px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.progress-wrapper {
    margin-bottom: 10px;
}

.progress-label {
    font-size: 14px;
    color: white;
    margin-bottom: 5px;
}

.progress-bar {
    height: 10px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    overflow: hidden;
}

.progress-bar-inner {
    height: 100%;
    background: rgba(79, 236, 184, 0.5);
    transition: width 0.3s ease;
}

.upload-success {
    margin-top: 10px;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    font-size: 14px;
    color: white;
    display: flex;
    align-items: center;
}

.custom-upload-button {
    background: linear-gradient(135deg, rgba(79, 236, 184, 0.8), rgba(79, 236, 184, 0.6));
    border: none;
    padding: 10px 20px;
    box-shadow: 0 4px 15px rgba(79, 236, 184, 0.3);
    margin-left: auto;
    /* Push to right */
    transition: all 0.3s ease;
}

.custom-upload-button:hover:not(:disabled) {
    background: linear-gradient(135deg, rgba(79, 236, 184, 0.9), rgba(79, 236, 184, 0.7));
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(79, 236, 184, 0.4);
}

.custom-upload-button:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: 0 2px 10px rgba(79, 236, 184, 0.2);
}

.custom-upload-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style>
