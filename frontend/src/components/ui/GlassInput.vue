<template>
    <div class="glass-input" :class="{
        'glass-input--disabled': disabled,
        'glass-input--focused': focused
    }">
        <label v-if="label" class="glass-input__label">{{ label }}</label>
        <div class="glass-input__wrapper">
            <input :type="type" :value="modelValue" :placeholder="placeholder" :disabled="disabled" :required="required"
                class="glass-input__inner" @input="updateValue" @focus="handleFocus" @blur="handleBlur" />
        </div>
    </div>
</template>

<script>
export default {
    name: 'GlassInput',
    props: {
        modelValue: {
            type: [String, Number],
            default: ''
        },
        type: {
            type: String,
            default: 'text'
        },
        placeholder: {
            type: String,
            default: ''
        },
        disabled: {
            type: Boolean,
            default: false
        },
        required: {
            type: Boolean,
            default: false
        },
        label: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            focused: false
        }
    },
    methods: {
        updateValue(event) {
            this.$emit('update:modelValue', event.target.value);
        },
        handleFocus() {
            this.focused = true;
            this.$emit('focus');
        },
        handleBlur() {
            this.focused = false;
            this.$emit('blur');
        }
    }
}
</script>

<style scoped>
.glass-input {
    position: relative;
    margin-bottom: 15px;
    width: 100%;
}

.glass-input__label {
    display: block;
    font-size: 14px;
    margin-bottom: 6px;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    font-weight: 500;
}

.glass-input__wrapper {
    position: relative;
    border-radius: 8px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    background-color: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s;
    overflow: hidden;
}

.glass-input__inner {
    width: 100%;
    height: 40px;
    padding: 0 15px;
    font-size: 14px;
    background: transparent;
    border: none;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    outline: none;
    box-sizing: border-box;
}

.glass-input__inner::placeholder {
    color: rgba(255, 255, 255, 0.5);
}

/* States */
.glass-input--focused .glass-input__wrapper {
    border-color: rgba(64, 158, 255, 0.8);
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.glass-input--disabled .glass-input__wrapper {
    background-color: rgba(255, 255, 255, 0.05);
    cursor: not-allowed;
}

.glass-input--disabled .glass-input__inner {
    cursor: not-allowed;
    color: rgba(255, 255, 255, 0.4);
}
</style>