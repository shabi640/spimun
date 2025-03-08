<template>
    <div class="glass-collapse">
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'GlassCollapse',
    props: {
        modelValue: {
            type: [String, Array],
            default: ''
        },
        accordion: {
            type: Boolean,
            default: false
        }
    },
    emits: ['update:modelValue', 'change'],
    provide() {
        return {
            glassCollapse: this
        };
    },
    data() {
        return {
            activeNames: this.convertModelValue()
        };
    },
    watch: {
        modelValue() {
            this.activeNames = this.convertModelValue();
        }
    },
    methods: {
        convertModelValue() {
            if (this.accordion) {
                return [this.modelValue];
            } else {
                return Array.isArray(this.modelValue) ? this.modelValue : [this.modelValue];
            }
        },
        handleItemClick(name) {
            if (this.accordion) {
                const newValue = this.activeNames[0] === name ? '' : name;
                this.activeNames = [newValue];
                this.$emit('update:modelValue', newValue);
                this.$emit('change', newValue);
            } else {
                const index = this.activeNames.indexOf(name);
                if (index > -1) {
                    this.activeNames.splice(index, 1);
                } else {
                    this.activeNames.push(name);
                }
                this.$emit('update:modelValue', this.activeNames);
                this.$emit('change', this.activeNames);
            }
        },
        isActive(name) {
            return this.activeNames.includes(name);
        }
    }
};
</script>

<style scoped>
.glass-collapse {
    border-radius: 10px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.18);
    color: var(--text-color, rgba(255, 255, 255, 0.9));
}
</style>