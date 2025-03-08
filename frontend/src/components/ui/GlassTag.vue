<template>
    <span class="glass-tag" :class="[
        `glass-tag--${type}`,
        `glass-tag--${size}`,
        `glass-tag--${effect}`,
        { 'glass-tag--closable': closable }
    ]">
        <slot></slot>
        <svg v-if="closable" class="glass-tag__close" viewBox="0 0 24 24" @click.stop="handleClose">
            <path
                d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
        </svg>
    </span>
</template>

<script>
export default {
    name: 'GlassTag',
    props: {
        type: {
            type: String,
            default: 'default',
            validator: (value) => {
                if (value === '') return true;
                return ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value);
            }
        },
        closable: {
            type: Boolean,
            default: false
        },
        size: {
            type: String,
            default: 'medium',
            validator: (value) => ['small', 'medium', 'large'].includes(value)
        },
        effect: {
            type: String,
            default: 'light',
            validator: (value) => ['light', 'dark'].includes(value)
        }
    },
    emits: ['close'],
    methods: {
        handleClose(event) {
            event.stopPropagation();
            this.$emit('close', event);
        }
    }
}
</script>

<style scoped>
.glass-tag {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0 8px;
    font-size: 12px;
    border-radius: 4px;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    white-space: nowrap;
    border: 1px solid transparent;
    box-sizing: border-box;
    transition: all 0.2s ease;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* Sizes */
.glass-tag--small {
    height: 20px;
    font-size: 10px;
    padding: 0 6px;
}

.glass-tag--medium {
    height: 24px;
    font-size: 12px;
}

.glass-tag--large {
    height: 28px;
    font-size: 14px;
    padding: 0 10px;
}

/* Light effect */
.glass-tag--light.glass-tag--default {
    background-color: rgba(255, 255, 255, 0.2);
    color: #909399;
    border-color: rgba(144, 147, 153, 0.2);
}

.glass-tag--light.glass-tag--primary {
    background-color: rgba(64, 158, 255, 0.1);
    color: #409eff;
    border-color: rgba(64, 158, 255, 0.2);
}

.glass-tag--light.glass-tag--success {
    background-color: rgba(103, 194, 58, 0.1);
    color: #67c23a;
    border-color: rgba(103, 194, 58, 0.2);
}

.glass-tag--light.glass-tag--warning {
    background-color: rgba(230, 162, 60, 0.1);
    color: #e6a23c;
    border-color: rgba(230, 162, 60, 0.2);
}

.glass-tag--light.glass-tag--danger {
    background-color: rgba(245, 108, 108, 0.1);
    color: #f56c6c;
    border-color: rgba(245, 108, 108, 0.2);
}

.glass-tag--light.glass-tag--info {
    background-color: rgba(144, 147, 153, 0.1);
    color: #909399;
    border-color: rgba(144, 147, 153, 0.2);
}

/* Dark effect */
.glass-tag--dark.glass-tag--default {
    background-color: rgba(144, 147, 153, 0.7);
    color: #fff;
}

.glass-tag--dark.glass-tag--primary {
    background-color: rgba(64, 158, 255, 0.7);
    color: #fff;
}

.glass-tag--dark.glass-tag--success {
    background-color: rgba(103, 194, 58, 0.7);
    color: #fff;
}

.glass-tag--dark.glass-tag--warning {
    background-color: rgba(230, 162, 60, 0.7);
    color: #fff;
}

.glass-tag--dark.glass-tag--danger {
    background-color: rgba(245, 108, 108, 0.7);
    color: #fff;
}

.glass-tag--dark.glass-tag--info {
    background-color: rgba(144, 147, 153, 0.7);
    color: #fff;
}

/* Close button */
.glass-tag__close {
    width: 12px;
    height: 12px;
    margin-left: 6px;
    cursor: pointer;
    fill: currentColor;
    transition: transform 0.2s ease;
}

.glass-tag__close:hover {
    transform: scale(1.2);
}

.glass-tag--closable {
    padding-right: 6px;
}
</style>