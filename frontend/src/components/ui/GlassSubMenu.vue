<template>
    <div class="glass-submenu" :class="{ 'is-active': isActive, 'is-opened': opened }" @mouseenter="handleMouseEnter"
        @mouseleave="handleMouseLeave">
        <div class="glass-submenu__title" @click="handleClick">
            <slot name="title"></slot>
            <div class="glass-submenu__icon" :class="{ 'is-opened': opened }">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
            </div>
        </div>
        <div class="glass-submenu__popup" :style="popupStyle">
            <div class="glass-submenu__content">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'GlassSubMenu',
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
        }
    },
    provide() {
        return {
            glassSubMenu: this
        };
    },
    data() {
        return {
            opened: false,
            timeout: null
        };
    },
    computed: {
        isActive() {
            return this.glassMenu?.activeIndex?.startsWith(this.index + '-');
        },
        isHorizontal() {
            return this.glassMenu?.mode === 'horizontal';
        },
        popupStyle() {
            return this.isHorizontal ? {} : { height: this.opened ? 'auto' : '0px' };
        }
    },
    methods: {
        handleClick() {
            if (this.disabled) return;

            if (!this.isHorizontal) {
                this.opened = !this.opened;
            }
        },
        handleMouseEnter() {
            if (this.disabled || !this.isHorizontal) return;

            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                this.opened = true;
            }, 200);
        },
        handleMouseLeave() {
            if (this.disabled || !this.isHorizontal) return;

            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                this.opened = false;
            }, 200);
        },
        handleItemClick() {
            if (this.isHorizontal) {
                this.opened = false;
            }
        }
    }
};
</script>

<style scoped>
.glass-submenu {
    position: relative;
}

.glass-submenu__title {
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
}

.glass-submenu__title:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.glass-submenu.is-active>.glass-submenu__title {
    color: var(--primary-color, #409eff);
    font-weight: 500;
}

.glass-submenu__icon {
    margin-left: 8px;
    transition: transform 0.3s;
}

.glass-submenu__icon.is-opened {
    transform: rotate(180deg);
}

.glass-menu--horizontal .glass-submenu__popup {
    position: absolute;
    top: 100%;
    left: 0;
    min-width: 220px;
    background: rgba(30, 60, 90, 0.9);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.18);
    z-index: 100;
    display: none;
    margin-top: 5px;
    padding: 8px 0;
}

.glass-menu--horizontal .glass-submenu.is-opened>.glass-submenu__popup {
    display: block;
}

.glass-menu--vertical .glass-submenu__popup {
    overflow: hidden;
    transition: height 0.3s ease-in-out;
}

.glass-menu--vertical .glass-submenu__content {
    padding-left: 20px;
    background-color: rgba(0, 0, 0, 0.05);
}

.glass-menu--vertical .glass-submenu__title {
    height: 50px;
}
</style>