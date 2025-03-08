<template>
    <div class="glass-checkbox" :class="{
        'is-checked': isChecked,
        'is-disabled': disabled
    }" @click="toggleChecked">
        <span class="glass-checkbox__input">
            <span class="glass-checkbox__inner"></span>
            <input type="checkbox" class="glass-checkbox__original" :value="label" :checked="isChecked"
                :disabled="disabled" @change="handleChange">
        </span>
        <span class="glass-checkbox__label">
            <slot>{{ label }}</slot>
        </span>
    </div>
</template>

<script>
export default {
    name: 'GlassCheckbox',
    props: {
        modelValue: {
            type: [Boolean, Array],
            default: false
        },
        label: {
            type: [String, Number, Boolean],
            default: ''
        },
        checked: {
            type: Boolean,
            default: false
        },
        disabled: {
            type: Boolean,
            default: false
        }
    },
    emits: ['update:modelValue', 'change'],
    computed: {
        isChecked() {
            if (Array.isArray(this.modelValue)) {
                return this.modelValue.includes(this.label);
            } else if (this.modelValue !== undefined) {
                return this.modelValue;
            } else {
                return this.checked;
            }
        }
    },
    methods: {
        toggleChecked() {
            if (this.disabled) return;

            const newValue = !this.isChecked;

            if (Array.isArray(this.modelValue)) {
                const newArray = [...this.modelValue];

                if (newValue) {
                    if (!newArray.includes(this.label)) {
                        newArray.push(this.label);
                    }
                } else {
                    const index = newArray.indexOf(this.label);
                    if (index !== -1) {
                        newArray.splice(index, 1);
                    }
                }

                this.$emit('update:modelValue', newArray);
                this.$emit('change', newArray);
            } else {
                this.$emit('update:modelValue', newValue);
                this.$emit('change', newValue);
            }
        },
        handleChange(event) {
            // This is needed to handle native checkbox behavior
            event.stopPropagation();
        }
    }
};
</script>

<style scoped>
.glass-checkbox {
    display: inline-flex;
    align-items: center;
    position: relative;
    cursor: pointer;
    font-size: 14px;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    margin-right: 30px;
    user-select: none;
}

.glass-checkbox__input {
    white-space: nowrap;
    cursor: pointer;
    outline: none;
    display: inline-flex;
    position: relative;
    vertical-align: middle;
}

.glass-checkbox__inner {
    display: inline-block;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 2px;
    box-sizing: border-box;
    width: 16px;
    height: 16px;
    background-color: rgba(255, 255, 255, 0.1);
    transition: border-color 0.25s, background-color 0.25s;
}

.glass-checkbox__inner::after {
    box-sizing: content-box;
    content: "";
    border: 1px solid #fff;
    border-left: 0;
    border-top: 0;
    height: 7px;
    left: 4px;
    position: absolute;
    top: 1px;
    transform: rotate(45deg) scaleY(0);
    width: 3px;
    transition: transform 0.15s ease-in 0.05s;
    transform-origin: center;
}

.glass-checkbox__original {
    opacity: 0;
    outline: none;
    position: absolute;
    margin: 0;
    width: 0;
    height: 0;
    z-index: -1;
}

.glass-checkbox__label {
    padding-left: 8px;
    transition: color 0.25s;
}

/* Checked state */
.glass-checkbox.is-checked .glass-checkbox__inner {
    background-color: var(--primary-color, #409eff);
    border-color: var(--primary-color, #409eff);
}

.glass-checkbox.is-checked .glass-checkbox__inner::after {
    transform: rotate(45deg) scaleY(1);
}

.glass-checkbox.is-checked .glass-checkbox__label {
    color: var(--primary-color, #409eff);
}

/* Disabled state */
.glass-checkbox.is-disabled {
    cursor: not-allowed;
}

.glass-checkbox.is-disabled .glass-checkbox__inner {
    background-color: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.15);
}

.glass-checkbox.is-disabled .glass-checkbox__label {
    color: rgba(255, 255, 255, 0.4);
}

.glass-checkbox.is-disabled.is-checked .glass-checkbox__inner {
    background-color: rgba(64, 158, 255, 0.4);
    border-color: rgba(64, 158, 255, 0.4);
}
</style>