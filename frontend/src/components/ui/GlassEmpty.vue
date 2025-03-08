<template>
    <div class="glass-empty" :style="{ '--image-size': imageSize + 'px' }">
        <div class="glass-empty__image">
            <slot name="image">
                <svg viewBox="0 0 79 86" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="linearGradient-1-empty" x1="38.78%" y1="0%" x2="61.22%" y2="100%">
                            <stop stop-color="#fff" stop-opacity="0.3" offset="0%"></stop>
                            <stop stop-color="#fff" stop-opacity="0.1" offset="100%"></stop>
                        </linearGradient>
                    </defs>
                    <g fill="url(#linearGradient-1-empty)" fill-rule="evenodd">
                        <path
                            d="M48.854 22.143H78.16c0 10.199-14.79 22.358-29.306 22.358S0 52.325 0 42.126c0-10.2 5.33-20.015 19.845-20.015s29.01 0 29.01 0zM20.327 41.669c.375-8.172 5.2-13.585 11.063-12.368 6.13 1.268 8.47 9.25 7.32 17.34-1.152 8.092-6.524 13.806-12.654 12.539-6.13-1.268-6.154-9.55-5.729-17.511z">
                        </path>
                        <path
                            d="M46.816 15.134v9.532s-4.56-15.158-7.202-17.001c-2.643-1.844-3.926-1.982-8.154-.456-4.229 1.526-13.983 5.296-16.891 6.425C11.81 14.763 2 11.766 2 5.285 2-1.197 8.682 0 16.95 0h20.002c7.864 0 9.864 8.05 9.864 15.134z">
                        </path>
                    </g>
                </svg>
            </slot>
        </div>
        <div class="glass-empty__description">
            <slot name="description">{{ description }}</slot>
        </div>
        <div v-if="$slots.default" class="glass-empty__bottom">
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'GlassEmpty',
    props: {
        imageSize: {
            type: Number,
            default: 160
        },
        description: {
            type: String,
            default: 'No data'
        }
    }
};
</script>

<style scoped>
.glass-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 0;
    text-align: center;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    margin: 20px 0;
}

.glass-empty__image {
    width: var(--image-size, 160px);
    height: var(--image-size, 160px);
    display: flex;
    justify-content: center;
    align-items: center;
}

.glass-empty__image svg {
    width: 100%;
    height: 100%;
}

.glass-empty__description {
    margin-top: 20px;
    color: rgba(255, 255, 255, 0.6);
    font-size: 14px;
}

.glass-empty__bottom {
    margin-top: 20px;
}
</style>