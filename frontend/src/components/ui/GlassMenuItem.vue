<template>
    <div class="glass-menu-item" :class="{ 'is-active': isActive, 'is-disabled': disabled }" @click="handleClick">
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'GlassMenuItem',
    props: {
        index: {
            type: String,
            required: true
        },
        disabled: {
            type: Boolean,
            default: false
        }
    },
    inject: {
        glassMenu: {
            default: null
        },
        glassSubMenu: {
            default: null
        }
    },
    computed: {
        isActive() {
            return this.glassMenu?.activeIndex === this.index;
        }
    },
    methods: {
        handleClick() {
            if (this.disabled) return;

            this.glassMenu?.setActiveItem(this.index);

            // If this menu item is inside a submenu, notify the submenu
            if (this.glassSubMenu) {
                this.glassSubMenu.handleItemClick();
            }

            this.$emit('click');
        }
    }
};
</script>

<style scoped>
.glass-menu-item {
    padding: 0 20px;
    height: 100%;
    display: flex;
    align-items: center;
    cursor: pointer;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    font-size: 14px;
    transition: all 0.3s;
    position: relative;
    white-space: nowrap;
    min-height: 40px;
}

.glass-menu-item:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.glass-menu-item.is-active {
    color: var(--primary-color, #409eff);
    font-weight: 500;
}

.glass-menu-item.is-active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--primary-color, #409eff);
}

/* 子菜单中的菜单项样式 */
.glass-submenu .glass-menu-item {
    height: 40px;
    /* 固定高度 */
    width: 100%;
    justify-content: flex-start;
    padding: 0 20px;
    box-sizing: border-box;
}

.glass-submenu .glass-menu-item.is-active::after {
    display: none;
    /* 子菜单中的活动指示器不显示 */
}

.glass-menu-item.is-disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.glass-menu--vertical .glass-menu-item {
    height: 50px;
}

.glass-menu--vertical .glass-menu-item.is-active::after {
    width: 2px;
    height: 100%;
    top: 0;
    right: 0;
    left: auto;
    bottom: auto;
}
</style>