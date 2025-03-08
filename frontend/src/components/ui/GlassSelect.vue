<template>
    <div class="glass-select" :class="{
        'glass-select--disabled': disabled,
        'glass-select--open': isOpen,
        'glass-select--clearable': clearable && modelValue
    }">
        <label v-if="label" class="glass-select__label">{{ label }}</label>
        <div class="glass-select__wrapper" ref="selectWrapper">
            <div class="glass-select__input" @click="toggleDropdown">
                <div v-if="!modelValue" class="glass-select__placeholder">{{ placeholder }}</div>
                <div v-else class="glass-select__value">
                    <slot name="selected" :value="modelValue">
                        {{ selectedLabel }}
                    </slot>
                </div>
                <div class="glass-select__suffix">
                    <span v-if="clearable && modelValue" class="glass-select__clear" @click.stop="clearValue">✕</span>
                    <span class="glass-select__arrow">▼</span>
                </div>
            </div>

            <div v-show="isOpen" class="glass-select__dropdown">
                <div class="glass-select__search-container" @click.stop>
                    <input ref="searchInput" v-model="searchQuery" class="glass-select__search-input"
                        placeholder="Type to search..." @keydown.down.prevent="navigateOptions('down')"
                        @keydown.up.prevent="navigateOptions('up')" @keydown.enter.prevent="selectHighlightedOption"
                        @keydown.esc.prevent="closeDropdown" />
                </div>
                <div class="glass-select__dropdown-inner">
                    <div v-if="$slots.default" class="glass-select__options">
                        <slot></slot>
                    </div>
                    <div v-else-if="filteredOptions.length === 0" class="glass-select__empty">
                        No matching options
                    </div>
                    <div v-else class="glass-select__options">
                        <glass-option v-for="(option, index) in filteredOptions" :key="option.value"
                            :value="option.value" :label="option.label" :disabled="option.disabled"
                            :class="{ 'option-highlighted': index === highlightedIndex }"
                            @mouseover="highlightedIndex = index"></glass-option>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import GlassOption from './GlassOption.vue';

export default {
    name: 'GlassSelect',
    components: {
        GlassOption
    },
    props: {
        modelValue: {
            type: [String, Number, Boolean, Array],
            default: ''
        },
        options: {
            type: Array,
            default: () => []
        },
        placeholder: {
            type: String,
            default: 'Please select'
        },
        disabled: {
            type: Boolean,
            default: false
        },
        clearable: {
            type: Boolean,
            default: false
        },
        label: {
            type: String,
            default: ''
        },
        multiple: {
            type: Boolean,
            default: false
        }
    },
    emits: ['update:modelValue', 'change'],
    data() {
        return {
            isOpen: false,
            childOptions: [],
            searchQuery: '',
            highlightedIndex: -1
        }
    },
    computed: {
        selectedLabel() {
            // First try to find the label in the options prop
            if (this.options && this.options.length > 0) {
                if (this.multiple && Array.isArray(this.modelValue)) {
                    const selectedLabels = this.options
                        .filter(option => this.modelValue.includes(option.value))
                        .map(option => option.label);
                    return selectedLabels.join(', ');
                } else {
                    const selected = this.options.find(option => option.value === this.modelValue);
                    if (selected) return selected.label;
                }
            }

            // If not found in options, try to find in child components
            if (this.$slots.default) {
                // This is a simplified approach - in a real component we'd need to access the child options
                // For now, we'll use a fallback
                return this.modelValue;
            }

            return '';
        },
        filteredOptions() {
            if (!this.searchQuery) {
                return this.options;
            }

            const query = this.searchQuery.toLowerCase();
            return this.options.filter(option => {
                const label = String(option.label).toLowerCase();
                const value = String(option.value).toLowerCase();
                return label.includes(query) || value.includes(query);
            });
        }
    },
    provide() {
        return {
            select: this
        };
    },
    watch: {
        isOpen(newVal) {
            if (newVal) {
                this.$nextTick(() => {
                    if (this.$refs.searchInput) {
                        this.$refs.searchInput.focus();
                    }
                    this.highlightedIndex = -1;
                    this.searchQuery = '';
                });
            }
        },
        searchQuery() {
            // Reset highlighted index when search query changes
            this.highlightedIndex = -1;
        }
    },
    mounted() {
        document.addEventListener('click', this.handleClickOutside);

        // Find all child options to get their labels
        this.updateChildOptions();
    },
    updated() {
        // Update child options when component updates
        this.updateChildOptions();
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    methods: {
        updateChildOptions() {
            // This is a simplified approach - in a real component we'd need to access the child options
            // through $children or other means
            this.childOptions = [];
        },
        toggleDropdown() {
            if (this.disabled) return;
            this.isOpen = !this.isOpen;
        },
        closeDropdown() {
            this.isOpen = false;
        },
        handleOptionClick(option) {
            if (this.multiple && Array.isArray(this.modelValue)) {
                const newValue = [...this.modelValue];
                const index = newValue.indexOf(option.value);

                if (index === -1) {
                    newValue.push(option.value);
                } else {
                    newValue.splice(index, 1);
                }

                this.$emit('update:modelValue', newValue);
                this.$emit('change', newValue);
            } else {
                this.$emit('update:modelValue', option.value);
                this.$emit('change', option.value);
                this.isOpen = false;
                this.searchQuery = '';
            }
        },
        clearValue(event) {
            event.stopPropagation();
            const emptyValue = this.multiple ? [] : '';
            this.$emit('update:modelValue', emptyValue);
            this.$emit('change', emptyValue);
        },
        handleClickOutside(event) {
            const selectWrapper = this.$refs.selectWrapper;
            if (selectWrapper && !selectWrapper.contains(event.target) && this.isOpen) {
                this.isOpen = false;
            }
        },
        navigateOptions(direction) {
            if (this.filteredOptions.length === 0) return;

            if (direction === 'down') {
                if (this.highlightedIndex < this.filteredOptions.length - 1) {
                    this.highlightedIndex++;
                } else {
                    this.highlightedIndex = 0; // Wrap to first option
                }
            } else if (direction === 'up') {
                if (this.highlightedIndex > 0) {
                    this.highlightedIndex--;
                } else {
                    this.highlightedIndex = this.filteredOptions.length - 1; // Wrap to last option
                }
            }

            // Ensure the highlighted option is visible in the dropdown
            this.$nextTick(() => {
                const options = this.$el.querySelectorAll('.glass-option');
                if (options[this.highlightedIndex]) {
                    options[this.highlightedIndex].scrollIntoView({ block: 'nearest' });
                }
            });
        },
        selectHighlightedOption() {
            if (this.highlightedIndex >= 0 && this.highlightedIndex < this.filteredOptions.length) {
                const option = this.filteredOptions[this.highlightedIndex];
                if (!option.disabled) {
                    this.handleOptionClick(option);
                }
            }
        }
    }
}
</script>

<style scoped>
.glass-select {
    position: relative;
    width: 100%;
    margin-bottom: 15px;
}

.glass-select__label {
    display: block;
    font-size: 14px;
    margin-bottom: 6px;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    font-weight: 500;
}

.glass-select__wrapper {
    position: relative;
}

.glass-select__input {
    position: relative;
    min-height: 40px;
    padding: 0 30px 0 15px;
    border-radius: 8px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    background-color: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s;
    cursor: pointer;
    display: flex;
    align-items: center;
}

.glass-select__placeholder {
    color: rgba(255, 255, 255, 0.5);
    font-size: 14px;
}

.glass-select__value {
    flex: 1;
    font-size: 14px;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-height: 20px;
    /* Ensure minimum height */
    padding: 10px 0;
    /* Add padding to ensure content is visible */
}

.glass-select__suffix {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    align-items: center;
}

.glass-select__arrow {
    font-size: 10px;
    color: rgba(255, 255, 255, 0.7);
    transition: transform 0.3s;
}

.glass-select--open .glass-select__arrow {
    transform: rotate(180deg);
}

.glass-select__clear {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
    margin-right: 5px;
    cursor: pointer;
}

.glass-select__clear:hover {
    color: #fff;
}

.glass-select__dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    margin-top: 5px;
    border-radius: 8px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    background-color: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    max-height: 250px;
    overflow-y: auto;
}

.glass-select__search-container {
    padding: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-select__search-input {
    width: 100%;
    height: 32px;
    padding: 0 10px;
    border-radius: 6px;
    background-color: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
    outline: none;
    transition: all 0.3s;
}

.glass-select__search-input:focus {
    border-color: rgba(64, 158, 255, 0.8);
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.glass-select__search-input::placeholder {
    color: rgba(255, 255, 255, 0.5);
}

.glass-select__dropdown-inner {
    padding: 5px 0;
}

.glass-select__options {
    max-height: 190px;
    overflow-y: auto;
}

.glass-select__empty {
    padding: 10px 15px;
    text-align: center;
    color: rgba(255, 255, 255, 0.5);
    font-size: 14px;
}

/* States */
.glass-select--open .glass-select__input {
    border-color: rgba(64, 158, 255, 0.8);
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.glass-select--disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.glass-select--disabled .glass-select__input {
    cursor: not-allowed;
    background-color: rgba(255, 255, 255, 0.05);
}

.option-highlighted {
    background-color: rgba(255, 255, 255, 0.2) !important;
}
</style>