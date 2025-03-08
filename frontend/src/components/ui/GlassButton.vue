<template>
    <button class="glass-button" :class="[
        `glass-button--${type}`,
        `glass-button--${size}`,
        { 'glass-button--disabled': disabled },
        { 'glass-button--loading': loading },
        { 'glass-button--circle': circle }
    ]" :disabled="disabled || loading" @click="handleClick">
        <div v-if="loading" class="glass-button__loading">
            <svg class="loading-spinner" viewBox="0 0 50 50">
                <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
            </svg>
        </div>
        <slot v-else></slot>
    </button>
</template>

<script>
export default {
    name: 'GlassButton',
    props: {
        type: {
            type: String,
            default: 'default',
            validator: (value) => ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value)
        },
        size: {
            type: String,
            default: 'medium',
            validator: (value) => ['small', 'medium', 'large'].includes(value)
        },
        disabled: {
            type: Boolean,
            default: false
        },
        loading: {
            type: Boolean,
            default: false
        },
        circle: {
            type: Boolean,
            default: false
        }
    },
    methods: {
        handleClick(event) {
            if (this.disabled || this.loading) return;
            this.$emit('click', event);
        }
    }
}
</script>

<style scoped>
.glass-button {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    color: var(--text-color, #fff);
}

.glass-button:hover:not(.glass-button--disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.glass-button:active:not(.glass-button--disabled) {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Sizes */
.glass-button--small {
    padding: 6px 12px;
    font-size: 12px;
    height: 32px;
}

.glass-button--medium {
    padding: 8px 16px;
    font-size: 14px;
    height: 40px;
}

.glass-button--large {
    padding: 10px 20px;
    font-size: 16px;
    height: 48px;
}

/* Types */
.glass-button--default {
    background-color: rgba(255, 255, 255, 0.2);
    color: var(--text-color, #303133);
}

.glass-button--primary {
    background-color: rgba(64, 158, 255, 0.7);
    color: #fff;
}

.glass-button--success {
    background-color: rgba(103, 194, 58, 0.7);
    color: #fff;
}

.glass-button--warning {
    background-color: rgba(230, 162, 60, 0.7);
    color: #fff;
}

.glass-button--danger {
    background-color: rgba(245, 108, 108, 0.7);
    color: #fff;
}

.glass-button--info {
    background-color: rgba(144, 147, 153, 0.7);
    color: #fff;
}

/* States */
.glass-button--disabled {
    cursor: not-allowed;
    opacity: 0.6;
    pointer-events: none;
}

.glass-button--loading {
    cursor: wait;
}

.glass-button--circle {
    border-radius: 50%;
    padding: 0;
    width: 40px;
    height: 40px;
}

.glass-button--circle.glass-button--small {
    width: 32px;
    height: 32px;
}

.glass-button--circle.glass-button--large {
    width: 48px;
    height: 48px;
}

/* Loading spinner */
.glass-button__loading {
    display: inline-flex;
    justify-content: center;
    align-items: center;
}

.loading-spinner {
    animation: rotate 2s linear infinite;
    width: 20px;
    height: 20px;
}

.path {
    stroke: currentColor;
    stroke-linecap: round;
    animation: dash 1.5s ease-in-out infinite;
}

@keyframes rotate {
    100% {
        transform: rotate(360deg);
    }
}

@keyframes dash {
    0% {
        stroke-dasharray: 1, 150;
        stroke-dashoffset: 0;
    }

    50% {
        stroke-dasharray: 90, 150;
        stroke-dashoffset: -35;
    }

    100% {
        stroke-dasharray: 90, 150;
        stroke-dashoffset: -124;
    }
}
</style>