<template>
    <div class="glass-collapse-item" :class="{ 'is-active': isActive }">
        <div class="glass-collapse-item__header" @click="handleHeaderClick">
            <div class="glass-collapse-item__header-text">
                <slot name="title">{{ title }}</slot>
            </div>
            <div class="glass-collapse-item__arrow" :class="{ 'is-active': isActive }">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
            </div>
        </div>
        <div class="glass-collapse-item__wrapper" :style="{ height: contentHeight }">
            <div class="glass-collapse-item__content" ref="content">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'GlassCollapseItem',
    props: {
        name: {
            type: [String, Number],
            required: true
        },
        title: {
            type: String,
            default: ''
        },
        disabled: {
            type: Boolean,
            default: false
        }
    },
    inject: {
        glassCollapse: {
            default: null
        }
    },
    data() {
        return {
            contentHeight: '0px'
        };
    },
    computed: {
        isActive() {
            return this.glassCollapse?.isActive(this.name) || false;
        }
    },
    watch: {
        isActive() {
            this.updateContentHeight();
        }
    },
    mounted() {
        this.updateContentHeight();
    },
    updated() {
        this.updateContentHeight();
    },
    methods: {
        handleHeaderClick() {
            if (this.disabled) return;
            this.glassCollapse?.handleItemClick(this.name);
        },
        updateContentHeight() {
            if (!this.$refs.content) return;

            if (this.isActive) {
                const height = this.$refs.content.offsetHeight;
                this.contentHeight = `${height}px`;
            } else {
                this.contentHeight = '0px';
            }
        }
    }
};
</script>

<style scoped>
.glass-collapse-item {
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-collapse-item:last-child {
    border-bottom: none;
}

.glass-collapse-item__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 48px;
    line-height: 48px;
    padding: 0 15px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    cursor: pointer;
    transition: background-color 0.3s;
}

.glass-collapse-item__header:hover {
    background-color: rgba(255, 255, 255, 0.05);
}

.glass-collapse-item__header-text {
    flex: 1;
}

.glass-collapse-item__arrow {
    color: rgba(255, 255, 255, 0.5);
    transition: transform 0.3s;
}

.glass-collapse-item__arrow.is-active {
    transform: rotate(180deg);
}

.glass-collapse-item__wrapper {
    overflow: hidden;
    transition: height 0.3s ease-in-out;
}

.glass-collapse-item__content {
    padding: 15px;
    font-size: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background-color: rgba(0, 0, 0, 0.1);
}

.glass-collapse-item.is-active .glass-collapse-item__header {
    background-color: rgba(255, 255, 255, 0.05);
}
</style>