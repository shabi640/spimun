<template>
    <GlassDrawer v-model="visible" title="Gossip Portal" direction="rtl" size="50%" :modal="false"
        :append-to-body="true" class="gossip-drawer">
        <div class="gossip-container">
            <GlassSkeleton v-if="isLoading" :rows="6" animated />
            <template v-else>
                <GlassEmpty v-if="messages.length === 0" description="No gossip yet" />

                <div v-else class="message-list">
                    <div v-for="message in messages" :key="message.id" class="message-item">
                        <div class="message-header">
                            <span class="sender">{{ message.sender }}</span>
                            <span class="date">{{ formatDate(message.date) }}</span>
                            <div class="message-actions">
                                <button class="custom-delete-btn" @click.stop="deleteMessage(message.id)"
                                    title="Delete message">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16">
                                        <path fill="currentColor"
                                            d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                                    </svg>
                                </button>
                            </div>

                        </div>
                        <div class="message-content">{{ message.text }}</div>
                    </div>
                </div>
            </template>
        </div>
    </GlassDrawer>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { GlassMessage } from '../components/ui';

export default {
    name: 'GossipPortal',
    props: {
        show: Boolean
    },
    emits: ['update:show'],
    setup(props, { emit }) {
        const messages = ref([]);
        const isLoading = ref(false);
        const visible = ref(props.show);

        const fetchGossips = async () => {
            isLoading.value = true;
            try {
                const response = await axios.get('http://127.0.0.1:8000/groups/1/messages');
                messages.value = response.data
                    .filter(msg => msg.id !== 1)
                    .map(msg => ({
                        ...msg,
                        sender: msg.sender_name || 'Anonymous'
                    }));
            } catch (error) {
                console.error('Error fetching gossips:', error);
                GlassMessage.error('Failed to load gossips');
            } finally {
                isLoading.value = false;
            }
        };

        const formatTimestamp = (timestamp) => {
            return new Date(timestamp).toLocaleTimeString();
        };

        const formatDate = (dateString) => {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        };

        const deleteMessage = async (messageId) => {
            try {
                await axios.delete(`http://127.0.0.1:8000/messages/${messageId}`);
                messages.value = messages.value.filter(msg => msg.id !== messageId);
                GlassMessage.success('Message deleted successfully');
            } catch (error) {
                console.error('Error deleting message:', error);
                GlassMessage.error('Failed to delete message');
            }
        };

        onMounted(fetchGossips);

        watch(() => props.show, (newVal) => {
            visible.value = newVal;
        });

        watch(visible, (val) => {
            emit('update:show', val);
            if (val) {
                console.log('Portal visibility changed to:', val);
                fetchGossips();
            }
        });

        return {
            messages,
            visible,
            formatTimestamp,
            formatDate,
            deleteMessage,
            isLoading
        };
    }
};
</script>

<style scoped>
.gossip-drawer {
    z-index: 2000 !important;
    /* Ensure it appears above other elements */
}

.gossip-container {
    padding: 20px;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.message-list {
    flex-grow: 1;
    overflow-y: auto;
}

.message-item {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    background-color: #f8f9fa;
}

.message-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 0.9em;
}

.sender {
    font-weight: 500;
    color: #606266;
}

.date {
    color: #909399;
    font-size: 0.85em;
    margin-right: 10px;
}

.timestamp {
    color: #909399;
}

.message-content {
    color: #303133;
    line-height: 1.6;
}

.message-actions {
    display: flex;
    gap: 8px;
}

/* Custom delete button styles */
.custom-delete-btn {
    background-color: var(--primary, #8a2be2);
    color: white;
    border: none;
    border-radius: 50%;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    padding: 6px;
}

.custom-delete-btn:hover {
    background-color: var(--primary-dark, #6a1cb2);
    transform: scale(1.1);
}

.custom-delete-btn:active {
    transform: scale(0.9);
}
</style>