<template>
    <GlassDialog :model-value="visible" @update:model-value="updateVisible" title="Login" :modal="true"
        :append-to-body="true" class="login-dialog">
        <GlassForm @submit.prevent="handleLogin" label-width="120px" class="glass-form">
            <h2 class="glass-title login-title">Welcome to SPIMUN</h2>
            <div class="glass-divider"></div>

            <GlassFormItem label="Name">
                <input v-model="name" placeholder="Enter your name" required class="standard-input">
            </GlassFormItem>

            <GlassFormItem label="Country">
                <GlassSelect ref="countrySelect" v-model="country" placeholder="Select your country" required
                    :options="countryOptions" @change="handleCountryChange">
                </GlassSelect>
            </GlassFormItem>
            <GlassFormItem label="Committee">
                <GlassSelect ref="committeeSelect" v-model="committee" placeholder="Select your committee" required
                    :options="committeeOptions" @change="handleCommitteeChange">
                </GlassSelect>
            </GlassFormItem>
            <div v-if="errorMessage" class="error-message">
                <GlassAlert :title="errorMessage" type="error" :show-icon="true"></GlassAlert>
            </div>
            <GlassFormItem class="form-buttons">
                <GlassButton type="primary" native-type="submit" class="login-button">Login</GlassButton>
                <GlassButton @click="refuseLogin" class="cancel-button">Cancel</GlassButton>
            </GlassFormItem>
        </GlassForm>
    </GlassDialog>
</template>

<script>
import axios from 'axios';

export default {
    props: {
        visible: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            name: '',
            country: '',
            committee: 'junior',
            id: '',
            errorMessage: '',
            // Define country and committee options directly in the component
            countryOptions: [
                { label: 'United States', value: 'USA' },
                { label: 'United Kingdom', value: 'UK' },
                { label: 'France', value: 'France' },
                { label: 'Germany', value: 'Germany' },
                { label: 'China', value: 'China' },
                { label: 'Russia', value: 'Russia' },
                { label: 'Japan', value: 'Japan' },
                { label: 'India', value: 'India' },
                { label: 'Brazil', value: 'Brazil' },
                { label: 'South Africa', value: 'South Africa' },
                { label: 'Canada', value: 'Canada' },
                { label: 'Australia', value: 'Australia' },
                { label: 'Italy', value: 'Italy' },
                { label: 'Spain', value: 'Spain' },
                { label: 'Mexico', value: 'Mexico' }
            ],
            committeeOptions: [
                { label: 'Junior', value: 'junior' },
                { label: 'Senior', value: 'senior' },
                { label: 'Security Council', value: 'security council' }
            ]
        };
    },
    computed: {
        // Helper computed properties to get the selected label
        selectedCountryLabel() {
            const country = this.countryOptions.find(option => option.value === this.country);
            return country ? country.label : '';
        },
        selectedCommitteeLabel() {
            const committee = this.committeeOptions.find(option => option.value === this.committee);
            return committee ? committee.label : '';
        }
    },
    methods: {
        handleCountryChange() {
            // Try multiple approaches to close the dropdown
            if (this.$refs.countrySelect) {
                // Approach 1: Set isOpen property directly
                this.$refs.countrySelect.isOpen = false;

                // Approach 2: Try to find and manipulate the DOM element
                const selectElement = this.$refs.countrySelect.$el;
                if (selectElement) {
                    // Remove the open class
                    selectElement.classList.remove('glass-select--open');

                    // Find and hide the dropdown element
                    const dropdown = selectElement.querySelector('.glass-select__dropdown');
                    if (dropdown) {
                        dropdown.style.display = 'none';
                    }
                }

                // Approach 3: Force a click outside to close the dropdown
                setTimeout(() => {
                    document.body.click();
                }, 0);
            }
        },
        handleCommitteeChange() {
            // Try multiple approaches to close the dropdown
            if (this.$refs.committeeSelect) {
                // Approach 1: Set isOpen property directly
                this.$refs.committeeSelect.isOpen = false;

                // Approach 2: Try to find and manipulate the DOM element
                const selectElement = this.$refs.committeeSelect.$el;
                if (selectElement) {
                    // Remove the open class
                    selectElement.classList.remove('glass-select--open');

                    // Find and hide the dropdown element
                    const dropdown = selectElement.querySelector('.glass-select__dropdown');
                    if (dropdown) {
                        dropdown.style.display = 'none';
                    }
                }

                // Approach 3: Force a click outside to close the dropdown
                setTimeout(() => {
                    document.body.click();
                }, 0);
            }
        },
        handleLogin() {
            // Validate form
            if (!this.name || !this.country) {
                this.errorMessage = 'Please fill in all required fields';
                return;
            }

            // Create login request data
            const loginData = {
                name: this.name,
                country: this.country,
                committee: this.committee
            };

            // Make API call to login endpoint
            axios.post('http://127.0.0.1:8000/api/login', loginData)
                .then(response => {
                    if (response.data.success) {
                        // Use the ID returned from the backend
                        const delegateInfo = {
                            name: this.name,
                            country: this.country,
                            committee: response.data.committee || this.committee,
                            id: response.data.id
                        };

                        console.log('Login successful with delegate ID:', delegateInfo.id);
                        console.log('Login with:', delegateInfo);

                        // Emit the login event with the delegate info
                        this.$emit('login', delegateInfo);

                        // Reset form fields
                        this.name = '';
                        this.country = '';
                        this.committee = 'junior';
                        this.errorMessage = '';
                    } else {
                        this.errorMessage = 'Login failed. Please check your credentials.';
                    }
                })
                .catch(error => {
                    console.error('Login error:', error);
                    this.errorMessage = 'Login failed. ' + (error.response?.data?.error || 'Please try again.');
                });
        },
        refuseLogin() {
            this.$emit('refuse-login');
        },
        updateVisible(newValue) {
            this.$emit('update:visible', newValue);
        },
    },
};
</script>

<style scoped>
/* 登录对话框样式 */
.login-dialog {
    z-index: 2000 !important;
}

.login-title {
    text-align: center;
    margin-bottom: 1.5rem;
    font-size: 1.8rem;
    color: rgba(255, 255, 255, 0.9);
}

.glass-form {
    max-width: 100%;
}

.glass-divider {
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
    margin: 15px 0 25px;
    width: 100%;
}

/* Standard input styling to match glass design */
.standard-input {
    width: 100%;
    height: 40px;
    padding: 10px 15px;
    /* Increased padding to match GlassSelect height */
    font-size: 14px;
    background-color: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.9);
    outline: none;
    transition: all 0.3s;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-sizing: border-box;
    /* Ensure padding is included in height calculation */
    margin: 0;
    /* Reset any default margins */
}

/* Add a wrapper to ensure consistent height with GlassSelect */
:deep(.glass-form-item) {
    min-height: 84px;
    /* Force all form items to have the same minimum height */
}

.standard-input::placeholder {
    color: rgba(255, 255, 255, 0.5);
}

.standard-input:focus {
    border-color: rgba(64, 158, 255, 0.8);
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

/* 自定义下拉列表样式 - 降低透明度 */
:deep(.glass-select__dropdown) {
    background-color: rgba(30, 41, 59, 0.9) !important;
    /* 增加不透明度 */
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
}

:deep(.glass-option) {
    color: rgba(255, 255, 255, 0.9) !important;
    /* 增加文字不透明度 */
}

:deep(.glass-option:hover) {
    background-color: rgba(255, 255, 255, 0.2) !important;
    /* 增加悬停背景不透明度 */
}

:deep(.is-selected) {
    background-color: rgba(64, 158, 255, 0.5) !important;
    /* 增加选中项背景不透明度 */
    color: white !important;
    font-weight: 500 !important;
}

.form-buttons {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
}

.login-button {
    background: linear-gradient(45deg, var(--glass-accent), var(--glass-accent-secondary)) !important;
    border: none !important;
    margin-right: 10px;
    transition: all 0.3s ease;
}

.login-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(79, 236, 184, 0.3) !important;
}

.cancel-button {
    background: rgba(255, 255, 255, 0.15) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

.cancel-button:hover {
    background: rgba(255, 255, 255, 0.25) !important;
}

.error-message {
    margin-bottom: 20px;
}
</style>
