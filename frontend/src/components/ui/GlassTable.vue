<template>
    <div class="glass-table-container">
        <table class="glass-table">
            <thead class="glass-table__header">
                <tr>
                    <slot name="header">
                        <!-- This will be populated by GlassTableColumn components -->
                    </slot>
                </tr>
            </thead>
            <tbody class="glass-table__body">
                <template v-if="data && data.length > 0">
                    <tr v-for="(row, rowIndex) in data" :key="rowIndex" class="glass-table__row">
                        <slot :row="row" :$index="rowIndex"></slot>
                    </tr>
                </template>
                <template v-else>
                    <tr class="glass-table__empty-row">
                        <td :colspan="columnCount" class="glass-table__empty-cell">
                            <slot name="empty">
                                <div class="glass-table__empty">
                                    No data
                                </div>
                            </slot>
                        </td>
                    </tr>
                </template>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    name: 'GlassTable',
    props: {
        data: {
            type: Array,
            default: () => []
        },
        stripe: {
            type: Boolean,
            default: false
        },
        border: {
            type: Boolean,
            default: false
        },
        size: {
            type: String,
            default: 'default',
            validator: (val) => ['large', 'default', 'small'].includes(val)
        }
    },
    data() {
        return {
            columns: [],
            columnCount: 0
        };
    },
    provide() {
        return {
            glassTable: this
        };
    },
    methods: {
        registerColumn(column) {
            this.columns.push(column);
            this.columnCount = this.columns.length;
        },
        unregisterColumn(column) {
            const index = this.columns.indexOf(column);
            if (index !== -1) {
                this.columns.splice(index, 1);
                this.columnCount = this.columns.length;
            }
        }
    }
};
</script>

<style scoped>
.glass-table-container {
    width: 100%;
    overflow-x: auto;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.glass-table {
    width: 100%;
    border-collapse: collapse;
    color: var(--text-color, rgba(255, 255, 255, 0.9));
    table-layout: fixed;
}

.glass-table__header {
    background: rgba(255, 255, 255, 0.15);
    position: sticky;
    top: 0;
    z-index: 2;
}

.glass-table__header th {
    padding: 12px 15px;
    text-align: left;
    font-weight: 600;
    font-size: 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.glass-table__body tr {
    transition: background-color 0.3s;
}

.glass-table__body tr:hover {
    background-color: rgba(255, 255, 255, 0.05);
}

.glass-table__body td {
    padding: 12px 15px;
    font-size: 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-table__body tr:last-child td {
    border-bottom: none;
}

.glass-table__empty-cell {
    text-align: center;
    padding: 32px 0;
}

.glass-table__empty {
    color: rgba(255, 255, 255, 0.5);
    font-size: 14px;
}

/* Stripe effect */
.glass-table__body tr:nth-child(even) {
    background-color: rgba(255, 255, 255, 0.03);
}

/* Border style */
.glass-table[border="true"] {
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.glass-table[border="true"] th,
.glass-table[border="true"] td {
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Size variants */
.glass-table[size="small"] th,
.glass-table[size="small"] td {
    padding: 8px 10px;
    font-size: 13px;
}

.glass-table[size="large"] th,
.glass-table[size="large"] td {
    padding: 16px 20px;
    font-size: 15px;
}
</style>