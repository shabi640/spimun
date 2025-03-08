<template>
    <div class="glass-form-item">
        <label v-if="label" class="glass-form-item__label" :style="labelStyle">
            {{ label }}
            <span v-if="required" class="glass-form-item__required">*</span>
        </label>
        <div class="glass-form-item__content">
            <slot></slot>
            <div v-if="error" class="glass-form-item__error">
                {{ error }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'GlassFormItem',
    props: {
        label: {
            type: String,
            default: ''
        },
        prop: {
            type: String,
            default: ''
        },
        required: {
            type: Boolean,
            default: false
        },
        rules: {
            type: [Object, Array],
            default: () => ({})
        },
        error: {
            type: String,
            default: ''
        },
        labelWidth: {
            type: String,
            default: ''
        }
    },
    inject: {
        glassForm: {
            default: null
        }
    },
    computed: {
        labelStyle() {
            if (this.labelWidth) {
                return { width: this.labelWidth };
            }
            if (this.glassForm && this.glassForm.labelWidth !== 'auto') {
                return { width: this.glassForm.labelWidth };
            }
            return {};
        },
        fieldValue() {
            if (!this.glassForm || !this.prop) return undefined;
            const { model } = this.glassForm;
            if (!model) return undefined;

            const props = this.prop.split('.');
            let value = model;
            props.forEach(key => {
                if (value) value = value[key];
            });
            return value;
        }
    },
    data() {
        return {
            validateState: '',
            validateMessage: ''
        };
    },
    methods: {
        validateField() {
            // Basic implementation - In a real app, you'd implement proper validation
            if (!this.prop || !this.rules) return null;

            const fieldRules = this.rules;
            const value = this.fieldValue;

            // Simple required validation as an example
            if (Array.isArray(fieldRules)) {
                for (const rule of fieldRules) {
                    if (rule.required && !value) {
                        this.validateState = 'error';
                        this.validateMessage = rule.message || `${this.label || this.prop} is required`;
                        return this.validateMessage;
                    }
                }
            } else if (fieldRules.required && !value) {
                this.validateState = 'error';
                this.validateMessage = fieldRules.message || `${this.label || this.prop} is required`;
                return this.validateMessage;
            }

            this.validateState = 'success';
            this.validateMessage = '';
            return null;
        },
        resetField() {
            this.validateState = '';
            this.validateMessage = '';

            // Reset the field value if possible
            if (!this.glassForm || !this.prop) return;
            const { model } = this.glassForm;
            if (!model) return;

            const props = this.prop.split('.');
            const len = props.length;

            if (len === 1) {
                model[this.prop] = '';
            } else {
                let value = model;
                for (let i = 0; i < len - 1; i++) {
                    value = value[props[i]];
                }
                value[props[len - 1]] = '';
            }
        }
    }
}
</script>

<style scoped>
.glass-form-item {
    margin-bottom: 18px;
}

.glass-form-item__label {
    display: block;
    font-size: 14px;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    line-height: 1.5;
    margin-bottom: 8px;
    font-weight: 500;
}

.glass-form-item__required {
    color: #f56c6c;
    margin-left: 4px;
}

.glass-form-item__content {
    position: relative;
}

.glass-form-item__error {
    color: #f56c6c;
    font-size: 12px;
    margin-top: 4px;
    position: absolute;
    top: 100%;
    left: 0;
}
</style>