<template>
    <th v-if="renderHeader" class="glass-table-column" :style="{ width: width }">
        <slot name="header">{{ label }}</slot>
    </th>
    <td v-else-if="renderCell" class="glass-table-column__cell">
        <slot :row="row" :$index="$index">
            {{ getCellValue(row) }}
        </slot>
    </td>
</template>

<script>
export default {
    name: 'GlassTableColumn',
    props: {
        prop: {
            type: String,
            default: ''
        },
        label: {
            type: String,
            default: ''
        },
        width: {
            type: String,
            default: ''
        },
        formatter: {
            type: Function,
            default: null
        },
        align: {
            type: String,
            default: 'left',
            validator: (val) => ['left', 'center', 'right'].includes(val)
        },
        sortable: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            row: null,
            $index: null,
            renderHeader: false,
            renderCell: false
        };
    },
    inject: {
        glassTable: {
            default: null
        }
    },
    methods: {
        getCellValue(row) {
            if (!this.prop) return '';
            const value = this.getPropValue(row, this.prop);
            return this.formatter ? this.formatter(row, this.prop, value, this.$index) : value;
        },
        getPropValue(row, prop) {
            const props = prop.split('.');
            let result = row;
            for (const key of props) {
                if (result === null || result === undefined) return '';
                result = result[key];
            }
            return result ?? '';
        }
    },
    created() {
        if (this.glassTable) {
            this.renderHeader = true;
            this.glassTable.registerColumn(this);
        }
    },
    beforeUnmount() {
        if (this.glassTable) {
            this.glassTable.unregisterColumn(this);
        }
    },
    render() {
        // This is needed for slot compatibility with GlassTable
        return null;
    }
};
</script>

<style scoped>
.glass-table-column {
    text-align: v-bind('align');
}

.glass-table-column__cell {
    text-align: v-bind('align');
}

.glass-table-column.sortable {
    cursor: pointer;
}

.glass-table-column.sorting-asc::after {
    content: '▲';
    margin-left: 5px;
    font-size: 0.8em;
    opacity: 0.7;
}

.glass-table-column.sorting-desc::after {
    content: '▼';
    margin-left: 5px;
    font-size: 0.8em;
    opacity: 0.7;
}
</style>