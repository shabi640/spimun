<template>
    <form class="glass-form" :class="{ ['glass-form--' + labelPosition]: true }" @submit.prevent="handleSubmit">
        <slot></slot>
    </form>
</template>

<script>
export default {
    name: 'GlassForm',
    props: {
        labelPosition: {
            type: String,
            default: 'top',
            validator: (value) => ['top', 'left', 'right'].includes(value)
        },
        labelWidth: {
            type: String,
            default: 'auto'
        },
        model: {
            type: Object,
            default: () => ({})
        },
        rules: {
            type: Object,
            default: () => ({})
        },
    },
    emits: ['submit'],
    provide() {
        return {
            glassForm: this
        };
    },
    methods: {
        handleSubmit(event) {
            this.$emit('submit', event);
        },
        validate(callback) {
            // Basic implementation - In a real app, you'd implement proper validation
            const formItems = this.getFormItems();
            const valid = formItems.every(item => !item.validateField());
            if (typeof callback === 'function') {
                callback(valid);
            }
            return Promise.resolve(valid);
        },
        validateField(prop, callback) {
            const formItems = this.getFormItems();
            const item = formItems.find(item => item.prop === prop);
            if (item) {
                const error = item.validateField();
                if (typeof callback === 'function') {
                    callback(error);
                }
                return Promise.resolve(!error);
            }
            return Promise.resolve(true);
        },
        resetFields() {
            const formItems = this.getFormItems();
            formItems.forEach(item => item.resetField());
        },
        getFormItems() {
            // Helper to get all child GlassFormItem components
            const findFormItems = (children) => {
                let result = [];
                if (!children) return result;

                children.forEach(child => {
                    if (child.$options && child.$options.name === 'GlassFormItem') {
                        result.push(child);
                    }
                    if (child.$children) {
                        result = result.concat(findFormItems(child.$children));
                    }
                });
                return result;
            };

            return findFormItems(this.$children || []);
        }
    }
}
</script>

<style scoped>
.glass-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.glass-form--left .glass-form-item {
    display: flex;
    align-items: flex-start;
}

.glass-form--left .glass-form-item__label {
    text-align: right;
    margin-right: 10px;
}

.glass-form--right .glass-form-item {
    display: flex;
    align-items: flex-start;
}

.glass-form--right .glass-form-item__label {
    text-align: left;
    margin-left: 10px;
    order: 2;
}

.glass-form--right .glass-form-item__content {
    order: 1;
}
</style>