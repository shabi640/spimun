<template>
    <div class="glass-menu" :class="[`glass-menu--${mode}`]">
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'GlassMenu',
    props: {
        defaultActive: {
            type: String,
            default: ''
        },
        mode: {
            type: String,
            default: 'horizontal',
            validator: (val) => ['horizontal', 'vertical'].includes(val)
        }
    },
    provide() {
        return {
            glassMenu: this
        };
    },
    data() {
        return {
            activeIndex: this.defaultActive
        };
    },
    watch: {
        defaultActive(val) {
            this.activeIndex = val;
        }
    },
    methods: {
        setActiveItem(index) {
            this.activeIndex = index;
            this.$emit('select', index);
        }
    }
};
</script>

<style scoped>
.glass-menu {
    display: flex;
    padding: 0;
    margin: 0;
    list-style: none;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.glass-menu--horizontal {
    flex-direction: row;
    align-items: center;
    height: 60px;
}

.glass-menu--vertical {
    flex-direction: column;
    width: 200px;
}
</style>