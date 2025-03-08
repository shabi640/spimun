<template>
    <div class="glass-icon" :class="[
        size ? `glass-icon--${size}` : '',
        color ? `glass-icon--${color}` : '',
        { 'glass-icon--spin': spin }
    ]" :style="customStyle">
        <component v-if="iconComponent" :is="iconComponent"></component>
        <svg v-else-if="isDefaultIcon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <!-- Default set of icons -->
            <template v-if="name === 'chat'">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </template>
            <template v-else-if="name === 'delete'">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </template>
            <template v-else-if="name === 'edit'">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </template>
            <template v-else-if="name === 'arrow-down'">
                <polyline points="6 9 12 15 18 9"></polyline>
            </template>
            <template v-else-if="name === 'arrow-up'">
                <polyline points="18 15 12 9 6 15"></polyline>
            </template>
            <template v-else-if="name === 'arrow-left'">
                <polyline points="15 18 9 12 15 6"></polyline>
            </template>
            <template v-else-if="name === 'arrow-right'">
                <polyline points="9 6 15 12 9 18"></polyline>
            </template>
            <template v-else-if="name === 'search'">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </template>
            <template v-else-if="name === 'plus'">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
            </template>
            <template v-else-if="name === 'check'">
                <polyline points="20 6 9 17 4 12"></polyline>
            </template>
            <template v-else-if="name === 'close'">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </template>
            <template v-else>
                <!-- Default icon if name not recognized -->
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="16"></line>
                <line x1="8" y1="12" x2="16" y2="12"></line>
            </template>
        </svg>
        <slot v-else></slot>
    </div>
</template>

<script>
export default {
    name: 'GlassIcon',
    props: {
        name: {
            type: String,
            default: ''
        },
        size: {
            type: String,
            default: '',
            validator: (val) => ['small', 'large'].includes(val)
        },
        color: {
            type: String,
            default: '',
            validator: (val) => ['primary', 'success', 'warning', 'danger', 'info'].includes(val)
        },
        spin: {
            type: Boolean,
            default: false
        },
        customStyle: {
            type: Object,
            default: () => ({})
        }
    },
    computed: {
        iconComponent() {
            // This would be where you'd integrate with an external icon library if desired
            return null;
        },
        isDefaultIcon() {
            return this.name && !this.iconComponent;
        }
    }
};
</script>

<style scoped>
.glass-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    transition: all 0.3s;
}

/* Sizes */
.glass-icon--small {
    width: 16px;
    height: 16px;
}

.glass-icon--large {
    width: 32px;
    height: 32px;
}

/* Colors */
.glass-icon--primary {
    color: var(--primary-color, #409eff);
}

.glass-icon--success {
    color: var(--success-color, #67c23a);
}

.glass-icon--warning {
    color: var(--warning-color, #e6a23c);
}

.glass-icon--danger {
    color: var(--danger-color, #f56c6c);
}

.glass-icon--info {
    color: var(--info-color, #909399);
}

/* Animation */
.glass-icon--spin {
    animation: glass-icon-spin 2s linear infinite;
}

@keyframes glass-icon-spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* Sizing for SVG and contents */
.glass-icon svg,
.glass-icon i {
    width: 100%;
    height: 100%;
}
</style>