<template>
    <!-- Use a single root element to avoid fragment issues -->
    <div>
        <div class="chat-container">
            <vue-advanced-chat height="calc(100vh - 80px)" :show-audio="false" :current-user-id="currentUserId"
                :rooms="JSON.stringify(rooms)" :rooms-loaded="true" :messages="JSON.stringify(messages)"
                :messages-loaded="messagesLoaded" :room-actions="JSON.stringify(roomActions)"
                :message-actions="JSON.stringify(messageActions)" @send-message="sendMessage"
                @add-room="showAddGroupPopup" @open-file="openFile" @fetch-messages="fetchMessages" />
        </div>

        <AddGroupPopup :isVisible="isAddGroupPopupVisible" :currentUserId="currentUserId"
            @close="isAddGroupPopupVisible = false" />
    </div>
</template>

<script>
import { register } from 'vue-advanced-chat'
register()
import axios from 'axios';
import io from 'socket.io-client';
import AddGroupPopup from '@/components/AddGroupPopup.vue';
import { GlassMessage } from '../components/ui';


export default {
    name: 'ChatComponent',
    components: { AddGroupPopup },
    props: {
        setNavBarVisibility: Function, // Add this prop to handle the attribute being passed
    },
    data() {
        // Get delegate ID from history state
        const id = history.state?.delegateid || '';

        // Ensure ID is a valid integer
        let validId = '';
        if (id && !isNaN(parseInt(id))) {
            validId = parseInt(id);
        }

        // Convert to string for component props
        const strid = String(validId);

        console.log('ChatComponent initialized with delegate ID:', validId, 'converted to string:', strid);

        return {
            isAddGroupPopupVisible: false,
            id: validId,
            strid,
            groups: [],
            currentUserId: strid,
            rooms: [],
            messages: [],
            messagesLoaded: false,
            roomActions: [],
            socket: null, // For Socket.IO connection
            currentRoomId: null, // Track the current room ID
            messageActions: [],
            delegatesMap: {}, // Map to store delegate ID to country mappings
        }
    },
    mounted() {
        console.log('ChatComponent mounted');

        this.fetchAllDelegates(); // Fetch all delegates to get their countries
        this.fetchGroupsForDelegate(this.id);
        this.initializeSocketConnection(); // Initialize Socket.IO connection

        // Call the setNavBarVisibility function if it exists
        if (this.setNavBarVisibility) {
            this.setNavBarVisibility(true); // Show nav bar when this component is mounted
        }
    },
    beforeDestroy() {
        console.log('ChatComponent being destroyed, cleaning up resources');
        if (this.socket) {
            this.socket.disconnect();
        }
    },
    methods: {
        // Add a new method to fetch all delegates and build the mapping
        async fetchAllDelegates() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/delegates');
                // Create a mapping from delegate ID to country
                const delegatesMap = {};
                response.data.forEach(delegate => {
                    delegatesMap[delegate.id] = delegate.country;
                });
                this.delegatesMap = delegatesMap;
                console.log('Delegates map created:', this.delegatesMap);
            } catch (error) {
                console.error('Error fetching delegates for country mapping:', error);
            }
        },

        showAddGroupPopup() {
            this.isAddGroupPopupVisible = true;
            console.log('visible')
        },

        async fetchGroupsForDelegate(delegateId) {
            console.log('Fetching groups for delegate ID:', delegateId);

            // Check if delegateId is valid
            if (!delegateId) {
                console.error('Invalid delegate ID. Cannot fetch groups.');
                return;
            }

            try {
                const response = await axios.get(`http://127.0.0.1:8000/searchgroup/${delegateId}`);
                console.log('Received groups response:', response.data);
                this.rooms = response.data.map(group => ({
                    roomId: group.id,
                    roomName: group.name,
                    unreadCount: group.unreadCount || 0,
                    users: group.delegates.map(delegate => ({
                        _id: delegate.id,
                        username: delegate.country || delegate.name // Use country instead of name
                    })),
                    lastMessage: group.lastMessage || null,
                    index: group.lastMessage && group.lastMessage.id ? parseInt(group.lastMessage.id, 10) : 0
                }));
                //this.joinAllGroups(); #will be performed when establishing socket connection
            } catch (error) {
                console.error('Error fetching rooms:', error);
            }
        },

        // Helper method to get country from delegate ID
        getDelegateCountry(delegateId) {
            // Use the mapping to get the country for the given delegate ID
            // If not found, fall back to the ID as string for display
            return this.delegatesMap[delegateId] || `Unknown (${delegateId})`;
        },

        fetchMessages(eventDetail) {
            const roomId = eventDetail.detail[0].room.roomId;
            console.log('Fetching messages for room:', roomId);
            this.currentRoomId = roomId;

            // Reset unread count when opening room
            const roomIndex = this.rooms.findIndex(room => room.roomId === roomId);
            if (roomIndex !== -1) {
                // Create a deep copy of rooms to modify
                const updatedRooms = [...this.rooms];
                updatedRooms[roomIndex] = {
                    ...updatedRooms[roomIndex],
                    unreadCount: 0
                };
                this.rooms = updatedRooms;

                // Also reset the unread count in the database
                this.resetUnreadCount(roomId);
            }

            const options = eventDetail.detail[0].options || {}; // Options passed along with the event

            // Use 'page' and 'per_page' as provided by the backend
            const page = options.reset ? 1 : Math.ceil((this.messages?.length || 0) / 30) + 1;

            // Set messages loaded to false before fetching
            this.messagesLoaded = false;

            // Clear messages if doing a reset to avoid flashing old messages
            if (options.reset) {
                this.messages = [];
            }

            console.log(`Fetching messages for room ${roomId}, page ${page}`);
            axios
                .get(`http://127.0.0.1:8000/groups/${roomId}/messages`, {
                    params: {
                        page: page,
                        per_page: 30, // Fetch 30 messages per page
                    }
                })
                .then((response) => {
                    console.log(`Received ${response.data.length} messages for room ${roomId}`);
                    let fetchedMessages = response.data;

                    // Check if the roomId is 1, and filter out messages sent by the current user
                    if (parseInt(roomId) === 1) {
                        fetchedMessages = fetchedMessages.filter(
                            message => message.id === 1  // Only keep message with ID 1
                        );
                    }

                    // Transform messages to match vue-advanced-chat requirements
                    fetchedMessages = fetchedMessages.map(msg => ({
                        _id: msg.id,
                        senderId: msg.sender_id ? msg.sender_id.toString() : '',
                        content: msg.text || '',
                        timestamp: msg.timestamp || '',
                        date: msg.date || '',
                        username: this.getDelegateCountry(msg.sender_id) || msg.sender_name || 'Unknown', // Use country instead of name
                        files: msg.files ? msg.files.map(file => ({
                            name: file.name || '',
                            size: file.size || 0,
                            type: file.type || 'application/octet-stream',
                            url: file.url || '',
                            preview: file.preview || null
                        })) : []
                    }));

                    // Update messages with proper reactivity
                    if (options.reset) {
                        // For reset, just set to fetched messages
                        this.messages = fetchedMessages;
                    } else {
                        // For pagination, prepend fetched messages
                        const existingMessages = this.messages || [];
                        this.messages = [...fetchedMessages, ...existingMessages];
                    }

                    // Set messages loaded with a delay to ensure rendering
                    setTimeout(() => {
                        this.messagesLoaded = true;
                        console.log('Messages loaded set to true');
                    }, 100);
                })
                .catch(error => {
                    console.error('Error fetching messages:', error);
                    // Ensure we still set messages loaded
                    setTimeout(() => {
                        this.messagesLoaded = true;
                    }, 100);
                });
        },

        // Method to reset unread count in the database
        resetUnreadCount(roomId) {
            axios.post(`http://127.0.0.1:8000/unread/${this.currentUserId}/${roomId}`, {
                count: 0
            }).catch(error => {
                console.error('Error resetting unread count:', error);
            });
        },

        openFile(eventDetail) {
            console.log('File opened');

            // Extract the file details from the eventDetail
            const fileDetail = eventDetail.detail[0].file;
            const downloadUrl = fileDetail.file.url;

            // Open the URL in a new tab to initiate the download
            window.open(downloadUrl, '_blank');
        },
        sendMessage(eventDetail) {
            console.log('Send message event received:', eventDetail);
            const messageDetail = eventDetail.detail[0]; // Extract message detail from the event
            const formData = new FormData();

            // Append text content if available
            if (messageDetail.content) {
                formData.append('content', messageDetail.content);
            }

            // Ensure roomId is a string for FormData
            const roomId = String(messageDetail.roomId);

            // Append the roomId, senderId, timestamp, and date
            formData.append('roomId', roomId);
            formData.append('senderId', this.currentUserId);
            const currentTimestamp = new Date();
            const timeString = currentTimestamp.toTimeString().substring(0, 5); // e.g., 'HH:MM'
            const dateString = currentTimestamp.toISOString().substring(0, 10); // e.g., 'YYYY-MM-DD'
            formData.append('timestamp', timeString);
            formData.append('date', dateString);

            // Check if there are any files and append them
            const hasFiles = messageDetail.files && messageDetail.files.length > 0;
            if (hasFiles) {
                console.log('Message has files:', messageDetail.files.length);
                messageDetail.files.forEach((file, index) => {
                    // Extract the actual file (Blob/File instance)
                    const actualFile = file.blob || file;  // Get the Blob/File object

                    if (!actualFile) {
                        console.error('No file blob found for file', index);
                        return;
                    }

                    // Extract the file extension
                    const fileExtension = file.extension || ''; // Assuming the extension is available in the `file` object

                    // Construct a new filename with the extension if needed
                    const originalFilename = file.name.includes('.') ? file.name : `${file.name}${fileExtension ? '.' + fileExtension : ''}`;

                    console.log(`Appending file ${index}:`, originalFilename);
                    // Append the file to FormData, passing the correct filename with extension
                    formData.append('files', actualFile, originalFilename);
                });
            }

            // Log the data being sent
            console.log('Sending message to server:', {
                content: messageDetail.content,
                roomId: roomId,
                senderId: this.currentUserId,
                timestamp: timeString,
                date: dateString,
                files: hasFiles ? 'Has files' : 'No files'
            });

            axios.post('http://127.0.0.1:8000/messages', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-Requested-With': 'XMLHttpRequest' // Add this for better CORS handling in Chrome
                },
            })
                .then(response => {
                    console.log('Message sent successfully:', response.data);
                    // We'll wait for the message to come back through the socket
                })
                .catch(error => {
                    console.error('Error sending message:', error);
                    // Show error notification
                    const errorMsg = error.response?.data?.error || 'Network error';
                    alert('Failed to send message: ' + errorMsg);
                });
        },

        initializeSocketConnection() {
            // Chrome-friendly socket configuration
            this.socket = io('http://127.0.0.1:8000/chatsocket', {
                reconnectionAttempts: 5,
                reconnectionDelay: 1000,
                transports: ['polling', 'websocket'], // Put polling first for Chrome compatibility
                upgrade: true
            });

            // Unified connection handling for all browsers
            this.socket.on('connect', () => {
                console.log('Socket connected successfully', this.socket.id);

                // Delay joining to ensure socket is ready
                setTimeout(() => {
                    this.joinAllGroups();

                    // Join the user's private room
                    this.socket.emit('join_user_room', { user_id: this.currentUserId });
                }, 100);
            });

            this.socket.on('error', (error) => {
                console.error('Socket error:', error);
            });

            this.socket.on('disconnect', () => {
                console.log('Socket disconnected, attempting to reconnect');
                // Try to reconnect manually
                setTimeout(() => {
                    this.socket.connect();
                }, 1000);
            });

            // Listen for new messages - unified approach for all browsers
            this.socket.on('new_message', (message) => {
                // Early validation - exit immediately if invalid format
                if (!message._id || !message.senderId) {
                    console.error('Invalid message format:', message);
                    return;
                }

                // Early filter for special room 1
                if (message.group_id === 1 && message.id !== 1) return;

                console.log('Received message:', message);
                console.log('Processing new message:', message);

                // Format the message
                const formattedMessage = {
                    _id: message._id,
                    content: message.text || '',
                    senderId: message.senderId,
                    timestamp: message.timestamp,
                    date: message.date,
                    username: this.getDelegateCountry(message.senderId) || message.username || 'Unknown', // Use country instead of name
                    files: message.files ? message.files.map(file => ({
                        name: file.name,
                        size: file.size,
                        type: file.type,
                        url: file.url,
                        preview: file.preview || null,
                    })) : []
                };

                try {
                    // Find the room index and update room data (last message, unread count)
                    const roomIndex = this.rooms.findIndex(room => room.roomId === message.group_id);
                    if (roomIndex !== -1) {
                        // Create a copy of rooms
                        const updatedRooms = [...this.rooms];

                        // Update last message
                        updatedRooms[roomIndex] = {
                            ...updatedRooms[roomIndex],
                            lastMessage: formattedMessage,
                            index: formattedMessage._id
                        };

                        // Update unread count if not current room
                        if (message.group_id !== this.currentRoomId) {
                            updatedRooms[roomIndex].unreadCount =
                                (updatedRooms[roomIndex].unreadCount || 0) + 1;
                        }

                        // Update the rooms array to trigger reactivity
                        this.rooms = updatedRooms;
                    }

                    // Add to messages if current room
                    if (message.group_id === this.currentRoomId) {
                        // Regular new message - add to collection
                        this.messages = [...this.messages, formattedMessage];
                    }
                } catch (error) {
                    console.error('Error processing message:', error);
                }
            });

            // Listen for the user being added to a new group
            this.socket.on('added_to_group', (groupData) => {
                console.log('Added to new group:', groupData);

                const newRoom = {
                    roomId: groupData.id,
                    roomName: groupData.name,
                    users: groupData.delegates.map(delegate => ({
                        _id: delegate.id,
                        username: delegate.country || delegate.name // Use country instead of name
                    })),
                    lastMessage: groupData.messages && groupData.messages.length > 0 ? groupData.messages[0] : null,
                    index: groupData.messages && groupData.messages.length > 0 ? groupData.messages[0].id : 0,
                    unreadCount: 0
                };

                // Add the new room to the list of rooms
                this.rooms = [...this.rooms, newRoom];

                // Join the newly added room after a short delay
                setTimeout(() => {
                    this.socket.emit('join_room', { roomId: newRoom.roomId });
                }, 100);

                // Show notification if GlassMessage is available
                if (typeof GlassMessage !== 'undefined') {
                    GlassMessage({
                        message: `You have been added to the group: ${groupData.name}`,
                        type: 'success',
                        duration: 3000,
                    });
                } else {
                    alert(`You have been added to the group: ${groupData.name}`);
                }
            });
        },

        joinAllGroups() {
            // Ensure the user joins all the groups they're a part of
            if (this.rooms && this.rooms.length > 0) {
                this.rooms.forEach((room) => {
                    if (room && room.roomId) {
                        console.log('Joining room:', room.roomId);
                        this.socket.emit('join_room', { roomId: room.roomId });
                    }
                });
            } else {
                console.log('No rooms to join yet');
            }
        },
    }
}
</script>


<style lang="scss">
body {
    font-family: 'Quicksand', sans-serif;
}

.chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    position: relative;
    overflow: hidden;
    /* Prevent scrolling issues */
}

/* Chrome and Safari compatible styles */
.vue-advanced-chat {
    height: calc(100vh - 80px) !important;
    max-height: 100vh;
}

/* Apply flexible box sizing for better compatibility */
.vac-room-roster,
.vac-room-list,
.vac-message-list {
    box-sizing: border-box !important;
}

/* Improve scrolling for all browsers */
.vac-message-list {
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch;
    /* Better scrolling on iOS */
    scrollbar-width: thin;
    /* Firefox */
}

/* Handle scrollbars in WebKit browsers */
.vac-message-list::-webkit-scrollbar {
    width: 5px;
}

.vac-message-list::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.2);
    border-radius: 3px;
}
</style>