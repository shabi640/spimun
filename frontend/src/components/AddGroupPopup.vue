<template>
    <GlassDialog :model-value="isVisible" title="Create New Group" width="600px" @close="closePopup"
        :close-on-click-modal="false">
        <!-- Group Name Input -->
        <GlassForm label-position="top" label-width="auto">
            <GlassFormItem label="Group Name">
                <GlassInput v-model="groupName" placeholder="Enter group name" ref="groupNameInput" />
            </GlassFormItem>

            <!-- Dropdown to select country -->
            <GlassFormItem label="Filter Delegate by Country">
                <GlassSelect v-model="selectedCountry" placeholder="Select Country" clearable @change="filterDelegates">
                    <GlassOption v-for="country in countries" :key="country" :label="country" :value="country" />
                </GlassSelect>
            </GlassFormItem>

            <!-- Dropdown to select committee -->
            <GlassFormItem label="Filter Delegate by Committee">
                <GlassSelect v-model="selectedCommittee" placeholder="Select Committee" clearable
                    @change="filterDelegates">
                    <GlassOption v-for="committee in committees" :key="committee" :label="committee"
                        :value="committee" />
                </GlassSelect>
            </GlassFormItem>

            <!-- Display selected delegates -->
            <h3>Selected Delegates: <span class="delegate-count">({{ selectedDelegatesList.length }})</span></h3>
            <div v-if="selectedDelegatesList.length === 0" class="no-delegates-message">
                No delegates selected yet. Use the table below to select delegates.
            </div>
            <table v-else class="custom-table selected-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Country</th>
                        <th>Committee</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="delegate in selectedDelegatesList" :key="delegate.id" class="custom-table-row">
                        <td>{{ delegate.name }}</td>
                        <td>{{ delegate.country }}</td>
                        <td>{{ delegate.committee }}</td>
                        <td>
                            <GlassButton size="small" type="danger" @click="removeDelegate(delegate.id)">
                                Remove</GlassButton>
                        </td>
                    </tr>
                </tbody>
            </table>

            <!-- List of filtered delegates to choose from -->
            <div class="delegates-selection-header">
                <h3>Available Delegates: <span class="delegate-count">({{ filteredDelegates.length }})</span></h3>
                <div class="selection-actions" v-if="filteredDelegates.length > 0">
                    <GlassButton size="small" @click="selectAllDelegates" v-if="!allDelegatesSelected">Select All
                    </GlassButton>
                    <GlassButton size="small" @click="deselectAllDelegates" v-else>Deselect All</GlassButton>
                </div>
            </div>
            <div v-if="filteredDelegates.length === 0" class="no-delegates-message">
                {{ (!selectedCountry || !selectedCommittee) ?
                    'Please select both a country and committee to view available delegates.' :
                    'No delegates match the selected country and committee.' }}
            </div>
            <table v-else class="custom-table available-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Country</th>
                        <th>Committee</th>
                        <th class="select-header">Select</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="delegate in filteredDelegates" :key="delegate.id" class="custom-table-row">
                        <td>{{ delegate.name }}</td>
                        <td>{{ delegate.country }}</td>
                        <td>{{ delegate.committee }}</td>
                        <td class="select-cell">
                            <GlassCheckbox class="blue-checkbox" :checked="selectedDelegates.includes(delegate.id)"
                                @change="toggleDelegateSelection(delegate)" />
                        </td>
                    </tr>
                </tbody>
            </table>

            <!-- Committee Chair Section -->
            <div v-if="selectedCountry && selectedCommittee">
                <div class="chair-section">
                    <h3>Committee Chair:</h3>
                    <div v-if="committeeChair" class="chair-card">
                        <div class="chair-info">
                            <span class="chair-name">{{ committeeChair.name }}</span>
                            <span class="chair-badge">Chair</span>
                        </div>
                        <GlassCheckbox class="blue-checkbox chair-checkbox"
                            :checked="selectedDelegates.includes(committeeChair.id)"
                            @change="toggleDelegateSelection(committeeChair)" />
                    </div>
                    <div v-else class="no-chair-message">
                        No chair found for this committee.
                    </div>
                </div>
            </div>

            <div class="dialog-footer" slot="footer">
                <GlassButton @click="closePopup">Cancel</GlassButton>
                <GlassButton type="primary" @click="createGroup">Create Group</GlassButton>
            </div>
        </GlassForm>
    </GlassDialog>
</template>

<script>
import axios from 'axios';
import { GlassMessage } from '../components/ui';

export default {
    props: ['isVisible', 'currentUserId'],
    data() {
        return {
            groupName: '',
            delegates: [], // All delegates fetched from the backend
            countries: [], // Extracted unique countries
            committees: [], // Extracted unique committees
            filteredDelegates: [], // Delegates filtered by selected country and committee
            selectedCountry: '',
            selectedCommittee: '',
            selectedDelegates: [], // Selected delegate IDs (only IDs)
            selectedDelegatesList: [], // List of selected delegate objects (for display)
        };
    },
    computed: {
        allDelegatesSelected() {
            return this.filteredDelegates.length > 0 &&
                this.filteredDelegates.every(delegate => this.selectedDelegates.includes(delegate.id));
        },
        committeeChair() {
            if (!this.selectedCommittee) return null;
            return this.delegates.find(delegate =>
                delegate.country === 'Chair' &&
                delegate.committee === this.selectedCommittee
            );
        }
    },
    mounted() {
        this.fetchAllDelegates();
    },
    methods: {
        // Fetch all delegates from the backend
        fetchAllDelegates() {
            axios.get('http://127.0.0.1:8000/delegates')
                .then(response => {
                    this.delegates = response.data;

                    // Extract unique countries and committees from the delegate data
                    this.countries = [...new Set(this.delegates.map(delegate => delegate.country))];

                    // Get all committees but exclude 'gossip' from the options
                    const allCommittees = [...new Set(this.delegates.map(delegate => delegate.committee))];
                    this.committees = allCommittees.filter(committee => committee !== 'gossip');

                    // Initialize filteredDelegates as empty until both filters are applied
                    this.filteredDelegates = [];
                })
                .catch(error => {
                    console.error('Error fetching delegates:', error);
                });
        },

        // Filter delegates based on selected country and committee
        filterDelegates() {
            if (this.selectedCountry && this.selectedCommittee) {
                // Only show delegates when both filters are applied
                this.filteredDelegates = this.delegates.filter(delegate =>
                    delegate.country === this.selectedCountry &&
                    delegate.committee === this.selectedCommittee
                );
            } else {
                // Clear the filtered delegates if both filters are not applied
                this.filteredDelegates = [];
            }
        },

        // Toggle delegate selection
        toggleDelegateSelection(delegate) {
            const index = this.selectedDelegates.indexOf(delegate.id);
            if (index === -1) {
                this.selectedDelegates.push(delegate.id);
                this.selectedDelegatesList.push(delegate);
            } else {
                this.selectedDelegates.splice(index, 1);
                this.selectedDelegatesList = this.selectedDelegatesList.filter(d => d.id !== delegate.id);
            }
        },

        // Select all currently filtered delegates
        selectAllDelegates() {
            this.filteredDelegates.forEach(delegate => {
                if (!this.selectedDelegates.includes(delegate.id)) {
                    this.selectedDelegates.push(delegate.id);
                    this.selectedDelegatesList.push(delegate);
                }
            });
        },

        // Deselect all currently filtered delegates
        deselectAllDelegates() {
            this.filteredDelegates.forEach(delegate => {
                const index = this.selectedDelegates.indexOf(delegate.id);
                if (index !== -1) {
                    this.selectedDelegates.splice(index, 1);
                    this.selectedDelegatesList = this.selectedDelegatesList.filter(d => d.id !== delegate.id);
                }
            });
        },

        // Remove a delegate from the selected list
        removeDelegate(delegateId) {
            this.selectedDelegates = this.selectedDelegates.filter(id => id !== delegateId);
            this.selectedDelegatesList = this.selectedDelegatesList.filter(delegate => delegate.id !== delegateId);
        },

        // Create a new group by sending the selected delegates and group name to the backend
        createGroup() {
            if (!this.groupName.trim()) {
                // Show error message using GlassMessage
                GlassMessage({
                    message: 'Please provide a group name.',
                    type: 'error',
                    duration: 3000,
                });

                // Focus on the group name input field
                this.$nextTick(() => {
                    this.$refs.groupNameInput.focus();
                });

                return;
            }

            if (this.selectedDelegates.length === 0) {
                GlassMessage({
                    message: 'Please select at least one delegate to create the group.',
                    type: 'error',
                    duration: 3000,
                });
                return;
            }

            const delegateIds = [...new Set([...this.selectedDelegates, this.currentUserId])];

            // Send data to the backend
            axios.post('http://127.0.0.1:8000/groups', {
                name: this.groupName,
                delegate_ids: delegateIds,
                inviting_user_id: this.currentUserId,
            })
                .then(response => {
                    GlassMessage({
                        message: 'Group created successfully!',
                        type: 'success',
                        duration: 3000,
                    });
                    this.closePopup(); // Close the popup
                })
                .catch(error => {
                    console.error('Error creating group:', error);
                    GlassMessage({
                        message: 'Failed to create the group.',
                        type: 'error',
                        duration: 3000,
                    });
                });
        },


        // Close the popup window
        closePopup() {
            this.$emit('close'); // Emit an event to the parent component to close the popup
        },
    },
};
</script>

<style scoped>
.delegates-selection-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.selection-actions {
    display: flex;
    gap: 8px;
}

.delegate-count {
    font-size: 0.9em;
    color: #666;
    font-weight: normal;
}

.no-delegates-message {
    padding: 20px;
    text-align: center;
    background-color: rgba(248, 249, 250, 0.6);
    border-radius: 8px;
    margin-bottom: 20px;
    color: #909399;
    font-style: italic;
}

/* Custom table styles to replace GlassTable */
.custom-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.custom-table thead {
    background-color: rgba(240, 240, 240, 0.5);
    border-bottom: 1px solid #ebeef5;
}

.custom-table th {
    padding: 12px 15px;
    text-align: left;
    font-weight: 600;
    color: #606266;
    font-size: 14px;
}

.custom-table td {
    padding: 12px 15px;
    border-bottom: 1px solid #ebeef5;
    color: #606266;
}

.custom-table-row:hover {
    background-color: rgba(64, 158, 255, 0.1);
}

.select-header {
    text-align: center;
}

.select-cell {
    text-align: center;
}

.custom-table tr:last-child td {
    border-bottom: none;
}

/* Selected table specific styling */
.selected-table td:last-child {
    text-align: center;
}

/* Available table specific styling */
.available-table th:last-child,
.available-table td:last-child {
    width: 80px;
}

/* Blue checkbox styling */
.blue-checkbox {
    --checkbox-border-color: #409EFF;
    --checkbox-background-color: rgba(64, 158, 255, 0.1);
}

:deep(.blue-checkbox .glass-checkbox__input:checked + .glass-checkbox__inner) {
    background-color: #409EFF;
    border-color: #409EFF;
    box-shadow: 0 0 8px rgba(64, 158, 255, 0.5);
}

:deep(.blue-checkbox .glass-checkbox__inner) {
    border: 2px solid #409EFF;
    background-color: rgba(255, 255, 255, 0.8);
    width: 18px;
    height: 18px;
    transition: all 0.3s;
}

:deep(.blue-checkbox .glass-checkbox__inner:hover) {
    border-color: #66B1FF;
    background-color: rgba(64, 158, 255, 0.1);
    transform: scale(1.05);
}

.chair-section {
    margin-top: 20px;
    margin-bottom: 20px;
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.chair-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    background-color: rgba(248, 249, 250, 0.6);
    border-radius: 6px;
    border-left: 4px solid #409EFF;
}

.chair-info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.chair-name {
    font-weight: 600;
    color: #303133;
}

.chair-badge {
    background-color: #409EFF;
    color: white;
    font-size: 0.8em;
    padding: 2px 6px;
    border-radius: 4px;
}

.chair-checkbox {
    margin-right: 10px;
}

.no-chair-message {
    color: #909399;
    font-style: italic;
    padding: 10px;
}
</style>
