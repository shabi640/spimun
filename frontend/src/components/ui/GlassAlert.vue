<template>
    <div v-if="visible" class="glass-alert" :class="[
        `glass-alert--${type}`,
        { 'glass-alert--with-icon': showIcon },
        { 'glass-alert--center': center }
    ]">
        <div v-if="showIcon" class="glass-alert__icon">
            <svg v-if="type === 'success'" viewBox="0 0 24 24" class="alert-icon">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
            </svg>
            <svg v-else-if="type === 'warning'" viewBox="0 0 24 24" class="alert-icon">
                <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z" />
            </svg>
            <svg v-else-if="type === 'error'" viewBox="0 0 24 24" class="alert-icon">
                <path
                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" />
            </svg>
            <svg v-else viewBox="0 0 24 24" class="alert-icon">
                <path
                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" />
            </svg>
        </div>
        <div class="glass-alert__content">
            <div v-if="title" class="glass-alert__title">
                {{ title }}
            </div>
            <div v-if="$slots.default" class="glass-alert__description">
                <slot></slot>
            </div>
        </div>
        <div v-if="closable" class="glass-alert__close-btn" @click="close">
            <svg viewBox="0 0 24 24" class="close-icon">
                <path
                    d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
            </svg>
        </div>
    </div>
</template>

<script>
export default {
    name: 'GlassAlert',
    props: {
        title: {
            type: String,
            default: ''
        },
        type: {
            type: String,
            default: 'info',
            validator: (value) => ['success', 'warning', 'info', 'error'].includes(value)
        },
        description: {
            type: String,
            default: ''
        },
        closable: {
            type: Boolean,
            default: true
        },
        showIcon: {
            type: Boolean,
            default: true
        },
        center: {
            type: Boolean,
            default: false
        },
        effect: {
            type: String,
            default: 'light',
            validator: value => ['light', 'dark'].includes(value)
        }
    },
    emits: ['close'],
    data() {
        return {
            visible: true
        };
    },
    methods: {
        close() {
            this.visible = false;
            this.$emit('close');
        }
    }
}
</script>

<style scoped>
.glass-alert {
    width: 100%;
    position: relative;
    margin-bottom: 16px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    padding: 14px 16px;
    overflow: hidden;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: opacity 0.3s;
}

.glass-alert--success {
    background-color: rgba(103, 194, 58, 0.3);
    border-left: 4px solid rgba(103, 194, 58, 0.8);
    color: #67c23a;
}

.glass-alert--warning {
    background-color: rgba(230, 162, 60, 0.3);
    border-left: 4px solid rgba(230, 162, 60, 0.8);
    color: #e6a23c;
}

.glass-alert--info {
    background-color: rgba(144, 147, 153, 0.3);
    border-left: 4px solid rgba(144, 147, 153, 0.8);
    color: #909399;
}

.glass-alert--error {
    background-color: rgba(245, 108, 108, 0.3);
    border-left: 4px solid rgba(245, 108, 108, 0.8);
    color: #f56c6c;
}

.glass-alert__icon {
    margin-right: 10px;
    display: flex;
    align-items: center;
}

.alert-icon {
    width: 20px;
    height: 20px;
    fill: currentColor;
}

.glass-alert__content {
    flex: 1;
}

.glass-alert__title {
    font-size: 14px;
    line-height: 1.4;
    font-weight: bold;
}

.glass-alert__description {
    font-size: 12px;
    margin-top: 6px;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    line-height: 1.4;
}

.glass-alert__close-btn {
    position: absolute;
    top: 14px;
    right: 16px;
    cursor: pointer;
    color: rgba(255, 255, 255, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
}

.close-icon {
    width: 14px;
    height: 14px;
    fill: currentColor;
}

.glass-alert--with-icon .glass-alert__content {
    padding-right: 16px;
}

.glass-alert--center {
    justify-content: center;
    text-align: center;
}

.glass-alert--center .glass-alert__icon {
    margin-right: 0;
}
</style>