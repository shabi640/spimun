<template>
    <li class="glass-option" :class="{
        'is-disabled': disabled,
        'is-selected': selected
    }" @click="handleClick">
        <slot>
            <span>{{ label || value }}</span>
        </slot>
    </li>
</template>

<script>
export default {
    name: 'GlassOption',
    props: {
        value: {
            type: [String, Number, Boolean, Object],
            required: true
        },
        label: {
            type: [String, Number]
        },
        disabled: {
            type: Boolean,
            default: false
        }
    },
    inject: {
        select: {
            default: null
        }
    },
    computed: {
        selected() {
            if (!this.select) return false;

            const { modelValue } = this.select;
            if (Array.isArray(modelValue)) {
                return modelValue.some(item => this.isEqual(item, this.value));
            } else {
                return this.isEqual(modelValue, this.value);
            }
        }
    },
    methods: {
        handleClick() {
            if (this.disabled) return;

            if (this.select) {
                this.select.handleOptionClick(this);
            }
        },
        isEqual(a, b) {
            if (a === b) return true;
            if (typeof a === 'object' && typeof b === 'object') {
                try {
                    return JSON.stringify(a) === JSON.stringify(b);
                } catch (e) {
                    return false;
                }
            }
            return false;
        }
    }
};
</script>

<style scoped>
.glass-option {
    display: flex;
    align-items: center;
    font-size: 14px;
    padding: 0 20px;
    position: relative;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: rgba(255, 255, 255, 0.8);
    height: 34px;
    line-height: 34px;
    box-sizing: border-box;
    cursor: pointer;
    transition: background-color 0.2s, color 0.2s;
}

.glass-option:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.is-selected {
    background-color: rgba(64, 158, 255, 0.3);
    font-weight: 500;
    color: white;
}

.is-disabled {
    color: rgba(255, 255, 255, 0.4);
    cursor: not-allowed;
}
</style>