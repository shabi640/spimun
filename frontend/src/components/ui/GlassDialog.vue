<template>
    <transition name="glass-dialog-fade">
        <div v-if="modelValue" class="glass-dialog__wrapper" @click.self="handleWrapperClick">
            <div class="glass-dialog" :style="{ width: width }">
                <div class="glass-dialog__header">
                    <div class="glass-dialog__title">
                        <slot name="title">{{ title }}</slot>
                    </div>
                    <button v-if="showClose" class="glass-dialog__close" @click="close">✕</button>
                </div>

                <div class="glass-dialog__body">
                    <slot></slot>
                </div>

                <div v-if="$slots.footer" class="glass-dialog__footer">
                    <slot name="footer"></slot>
                </div>
            </div>
        </div>
    </transition>
</template>

<script>
export default {
    name: 'GlassDialog',
    props: {
        modelValue: {
            type: Boolean,
            default: false
        },
        title: {
            type: String,
            default: ''
        },
        width: {
            type: String,
            default: '50%'
        },
        closeOnClickModal: {
            type: Boolean,
            default: true
        },
        showClose: {
            type: Boolean,
            default: true
        },
        modal: {
            type: Boolean,
            default: true
        },
        appendToBody: {
            type: Boolean,
            default: false
        }
    },
    emits: ['update:modelValue', 'close'],
    methods: {
        close() {
            this.$emit('update:modelValue', false);
            this.$emit('close');
        },
        handleWrapperClick() {
            if (this.closeOnClickModal) {
                this.close();
            }
        }
    },
    mounted() {
        if (this.appendToBody && this.$el) {
            document.body.appendChild(this.$el);
        }

        // Lock body scroll when dialog is open
        if (this.modelValue) {
            document.body.style.overflow = 'hidden';
        }
    },
    updated() {
        // Update body scroll lock status when modelValue changes
        if (this.modelValue) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    },
    beforeUnmount() {
        // Remove element from body if it was appended
        if (this.appendToBody && this.$el && this.$el.parentNode) {
            this.$el.parentNode.removeChild(this.$el);
        }

        // Restore body scroll
        document.body.style.overflow = '';
    }
}
</script>

<style scoped>
.glass-dialog__wrapper {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, 0.5);
    overflow: auto;
}

.glass-dialog {
    position: relative;
    margin: 30px auto;
    border-radius: 12px;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    background-color: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    overflow: hidden;
    max-width: 90%;
}

.glass-dialog__header {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-dialog__title {
    font-size: 18px;
    font-weight: bold;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    margin: 0;
    line-height: 1;
}

.glass-dialog__close {
    background: transparent;
    border: none;
    font-size: 20px;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    transition: color 0.2s;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    border-radius: 50%;
}

.glass-dialog__close:hover {
    color: white;
    background-color: rgba(255, 255, 255, 0.1);
}

.glass-dialog__body {
    padding: 20px;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    font-size: 14px;
    word-break: break-word;
}

.glass-dialog__footer {
    padding: 10px 20px 20px;
    text-align: right;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Animation */
.glass-dialog-fade-enter-active,
.glass-dialog-fade-leave-active {
    transition: opacity 0.3s ease;
}

.glass-dialog-fade-enter-from,
.glass-dialog-fade-leave-to {
    opacity: 0;
}

.glass-dialog-fade-enter-active .glass-dialog,
.glass-dialog-fade-leave-active .glass-dialog {
    transition: transform 0.3s ease-out;
}

.glass-dialog-fade-enter-from .glass-dialog,
.glass-dialog-fade-leave-to .glass-dialog {
    transform: translateY(-30px);
}
</style>