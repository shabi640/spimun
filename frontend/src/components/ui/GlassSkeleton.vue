<template>
    <div class="glass-skeleton" :class="{
        'is-animated': animated,
        [`glass-skeleton--${variant}`]: variant
    }">
        <template v-if="loading">
            <div v-for="i in count" :key="i" class="glass-skeleton-item" :style="{
                width: width,
                height: height
            }">
                <template v-if="variant === 'circle'">
                    <div class="glass-skeleton-circle"></div>
                </template>
                <template v-else-if="variant === 'image'">
                    <div class="glass-skeleton-image"></div>
                </template>
                <template v-else>
                    <div v-for="j in rows" :key="j" class="glass-skeleton-paragraph" :style="{
                        width: getRowWidth(j)
                    }"></div>
                </template>
            </div>
        </template>
        <template v-else>
            <slot></slot>
        </template>
    </div>
</template>

<script>
export default {
    name: 'GlassSkeleton',
    props: {
        animated: {
            type: Boolean,
            default: true
        },
        count: {
            type: Number,
            default: 1
        },
        rows: {
            type: Number,
            default: 3
        },
        loading: {
            type: Boolean,
            default: true
        },
        variant: {
            type: String,
            default: 'text',
            validator: (val) => ['text', 'circle', 'image'].includes(val)
        },
        width: {
            type: String,
            default: '100%'
        },
        height: {
            type: String,
            default: ''
        }
    },
    methods: {
        getRowWidth(index) {
            if (this.variant !== 'text') return '100%';

            // Last row is shorter
            if (index === this.rows && this.rows > 1) {
                return '60%';
            }

            // Random width between 80% and 100% for other rows
            return `${Math.floor(Math.random() * 20) + 80}%`;
        }
    }
};
</script>

<style scoped>
.glass-skeleton {
    width: 100%;
}

.glass-skeleton-item {
    margin-bottom: 16px;
}

.glass-skeleton-paragraph {
    height: 16px;
    margin-top: 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

.glass-skeleton-circle {
    width: 100%;
    height: 100%;
    min-height: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
}

.glass-skeleton-image {
    width: 100%;
    height: 0;
    padding-bottom: 56.25%;
    /* 16:9 aspect ratio */
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

.glass-skeleton.is-animated .glass-skeleton-paragraph,
.glass-skeleton.is-animated .glass-skeleton-circle,
.glass-skeleton.is-animated .glass-skeleton-image {
    position: relative;
    overflow: hidden;
    z-index: 1;
}

.glass-skeleton.is-animated .glass-skeleton-paragraph::after,
.glass-skeleton.is-animated .glass-skeleton-circle::after,
.glass-skeleton.is-animated .glass-skeleton-image::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg,
            rgba(255, 255, 255, 0.05) 25%,
            rgba(255, 255, 255, 0.15) 37%,
            rgba(255, 255, 255, 0.05) 63%);
    animation: glass-skeleton-loading 1.4s ease infinite;
    background-size: 400% 100%;
}

@keyframes glass-skeleton-loading {
    0% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0 50%;
    }
}
</style>