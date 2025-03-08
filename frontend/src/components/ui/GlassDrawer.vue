<template>
    <transition name="glass-drawer-fade">
        <div v-show="visible" class="glass-drawer__wrapper" @click.self="handleWrapperClick">
            <transition :name="'glass-drawer-' + direction">
                <div v-show="visible" class="glass-drawer" :class="[direction, customClass]" :style="drawerStyle">
                    <div class="glass-drawer__header">
                        <slot name="title">
                            <span class="glass-drawer__title">{{ title }}</span>
                        </slot>
                        <button v-if="showClose" class="glass-drawer__close-btn" @click="handleClose">
                            <span class="glass-drawer__close-icon">×</span>
                        </button>
                    </div>
                    <div class="glass-drawer__body">
                        <slot></slot>
                    </div>
                    <div v-if="$slots.footer" class="glass-drawer__footer">
                        <slot name="footer"></slot>
                    </div>
                </div>
            </transition>
        </div>
    </transition>
</template>

<script>
export default {
    name: 'GlassDrawer',
    props: {
        modelValue: {
            type: Boolean,
            default: false
        },
        title: {
            type: String,
            default: ''
        },
        direction: {
            type: String,
            default: 'rtl',
            validator: (val) => ['ltr', 'rtl', 'ttb', 'btt'].includes(val)
        },
        size: {
            type: [Number, String],
            default: '30%'
        },
        showClose: {
            type: Boolean,
            default: true
        },
        closeOnClickModal: {
            type: Boolean,
            default: true
        },
        customClass: {
            type: String,
            default: ''
        },
        zIndex: {
            type: Number,
            default: 2000
        }
    },
    emits: ['update:modelValue', 'open', 'opened', 'close', 'closed'],
    data() {
        return {
            closed: false
        };
    },
    computed: {
        visible: {
            get() {
                return this.modelValue;
            },
            set(val) {
                this.$emit('update:modelValue', val);
            }
        },
        drawerStyle() {
            const style = {};
            if (this.direction === 'rtl' || this.direction === 'ltr') {
                style.width = typeof this.size === 'number' ? `${this.size}px` : this.size;
            } else {
                style.height = typeof this.size === 'number' ? `${this.size}px` : this.size;
            }
            style.zIndex = this.zIndex;
            return style;
        }
    },
    watch: {
        visible(val) {
            if (val) {
                this.closed = false;
                this.$emit('open');
                this.$nextTick(() => {
                    this.$emit('opened');
                });
            } else {
                if (!this.closed) {
                    this.$emit('close');
                    this.closed = true;
                    this.$nextTick(() => {
                        this.$emit('closed');
                    });
                }
            }
        }
    },
    methods: {
        handleWrapperClick() {
            if (this.closeOnClickModal) {
                this.handleClose();
            }
        },
        handleClose() {
            this.visible = false;
        }
    }
};
</script>

<style scoped>
.glass-drawer__wrapper {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    overflow: hidden;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 2000;
}

.glass-drawer {
    position: absolute;
    display: flex;
    flex-direction: column;
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    overflow: auto;
}

.glass-drawer.rtl {
    top: 0;
    right: 0;
    bottom: 0;
}

.glass-drawer.ltr {
    top: 0;
    left: 0;
    bottom: 0;
}

.glass-drawer.ttb {
    left: 0;
    right: 0;
    top: 0;
}

.glass-drawer.btt {
    left: 0;
    right: 0;
    bottom: 0;
}

.glass-drawer__header {
    display: flex;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-drawer__title {
    flex: 1;
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
}

.glass-drawer__close-btn {
    background: transparent;
    border: none;
    outline: none;
    cursor: pointer;
    font-size: 20px;
    color: rgba(255, 255, 255, 0.7);
    transition: color 0.3s;
}

.glass-drawer__close-btn:hover {
    color: rgba(255, 255, 255, 1);
}

.glass-drawer__body {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    color: rgba(255, 255, 255, 0.8);
}

.glass-drawer__footer {
    padding: 16px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Transitions */
.glass-drawer-fade-enter-active,
.glass-drawer-fade-leave-active {
    transition: opacity 0.3s;
}

.glass-drawer-fade-enter-from,
.glass-drawer-fade-leave-to {
    opacity: 0;
}

.glass-drawer-rtl-enter-active,
.glass-drawer-rtl-leave-active,
.glass-drawer-ltr-enter-active,
.glass-drawer-ltr-leave-active,
.glass-drawer-ttb-enter-active,
.glass-drawer-ttb-leave-active,
.glass-drawer-btt-enter-active,
.glass-drawer-btt-leave-active {
    transition: transform 0.3s ease-in-out;
}

.glass-drawer-rtl-enter-from,
.glass-drawer-rtl-leave-to {
    transform: translateX(100%);
}

.glass-drawer-ltr-enter-from,
.glass-drawer-ltr-leave-to {
    transform: translateX(-100%);
}

.glass-drawer-ttb-enter-from,
.glass-drawer-ttb-leave-to {
    transform: translateY(-100%);
}

.glass-drawer-btt-enter-from,
.glass-drawer-btt-leave-to {
    transform: translateY(100%);
}
</style>