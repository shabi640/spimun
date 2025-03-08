<template>
    <div class="container">
        <!-- Login Dialog Component -->
        <LoginDialog v-if="!isAuthenticated" @login-success="handleLoginSuccess" />

        <div v-if="isAuthenticated" class="main-content full-screen">
            <!-- Sidebar Navigation -->
            <nav class="sidebar" :class="{ folded: isSidebarFolded }">
                <div class="sidebar-content">
                    <div class="top-nav">
                        <button class="toggle-button" @click="toggleSidebar">
                            {{ isSidebarFolded ? '>>' : '<<' }} </button>

                                <!-- Back button -->
                                <button
                                    v-if="!isSidebarFolded && (previousState.committee || previousState.contentType)"
                                    class="back-button" @click="goBack">
                                    Back to Previous
                                </button>

                                <ul v-if="!isSidebarFolded">
                                    <li :class="{ active: selectedCommittee === 'Senior' }"
                                        @click="selectCommittee('Senior')">
                                        Senior Committee
                                    </li>
                                    <li :class="{ active: selectedCommittee === 'Junior' }"
                                        @click="selectCommittee('Junior')">
                                        Junior Committee
                                    </li>
                                    <li :class="{ active: selectedCommittee === 'Security Council' }"
                                        @click="selectCommittee('Security Council')">
                                        Security Council
                                    </li>
                                </ul>

                                <ul v-if="!isSidebarFolded && selectedCommittee">
                                    <li :class="{ active: contentType === 'clauses' }"
                                        @click="selectContentType('clauses')">
                                        Clauses
                                    </li>
                                    <li :class="{ active: contentType === 'amendments' }"
                                        @click="selectContentType('amendments')">
                                        Amendments
                                    </li>
                                </ul>
                    </div>

                    <!-- Gossip Portal Button - Now at bottom -->
                    <div class="bottom-nav">
                        <!-- Gossip for expanded sidebar -->
                        <ul v-if="!isSidebarFolded" class="gossip-section">
                            <li class="gossip-nav-item" @click="showGossipPortal = !showGossipPortal"
                                :class="{ active: showGossipPortal }">
                                {{ showGossipPortal ? 'Close Gossip' : 'View Gossips' }}
                            </li>
                        </ul>

                        <!-- Gossip icon for folded sidebar -->
                        <div v-if="isSidebarFolded" class="folded-gossip" @click="showGossipPortal = !showGossipPortal"
                            :class="{ active: showGossipPortal }">
                            G
                        </div>
                    </div>
                </div>
            </nav>

            <!-- Main Display Area -->
            <div class="content full-width">
                <!-- Content List -->
                <div v-if="!clausesHtml && selectedCommittee && contentType">
                    <h2>{{ contentType.charAt(0).toUpperCase() + contentType.slice(1) }} for {{ selectedCommittee }}
                    </h2>

                    <div v-if="contentType === 'clauses'" class="content-container">
                        <!-- Published Clause Section -->
                        <div class="section-header">
                            <div class="section-title">
                                <i class="fas fa-star"></i> Published Clause
                            </div>
                        </div>
                        <div class="clause-section">
                            <div v-if="publishedClauses.length > 0">
                                <div class="published-clause-card" v-for="clause in publishedClauses" :key="clause.id">
                                    <div class="status-badge">Currently Published</div>
                                    <div class="published-details">
                                        <div class="detail-row">
                                            <span class="detail-label">Title:</span>
                                            <span class="detail-value">{{ clause.title || clause.filename }}</span>
                                        </div>
                                        <div class="detail-row">
                                            <span class="detail-label">Submitted by:</span>
                                            <span class="detail-value">{{ clause.country }}</span>
                                        </div>
                                        <div class="detail-row">
                                            <span class="detail-label">Published on:</span>
                                            <span class="detail-value">{{ formatDate(clause.timestamp) }}</span>
                                        </div>
                                        <div class="detail-row">
                                            <span class="detail-label">Actions:</span>
                                            <span class="detail-value">
                                                <button class="action-button" @click="viewClause(clause)">View
                                                    Details</button>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="empty-published">
                                <i class="fas fa-scroll fa-2x"></i>
                                <p>No clause has been published yet.</p>
                            </div>
                        </div>

                        <!-- Pending Clauses Section -->
                        <div class="section-header">
                            <div class="section-title">
                                <i class="fas fa-clock"></i> Pending Clauses
                                <span class="section-count">{{ pendingClauses.length }}</span>
                            </div>
                        </div>
                        <div class="clause-section">
                            <div class="clause-cards">
                                <div v-for="clause in pendingClauses" :key="clause.id" class="clause-card pending-card"
                                    @click="viewClause(clause)">
                                    <div class="card-header">{{ clause.title || clause.filename }}</div>
                                    <div class="card-body">
                                        <p><strong>Submitted by:</strong> {{ clause.country }}</p>
                                        <p><strong>Submitted on:</strong> {{ formatDate(clause.timestamp) }}</p>
                                    </div>
                                </div>
                            </div>
                            <div v-if="pendingClauses.length === 0" class="empty-state">
                                <i class="fas fa-inbox fa-2x"></i>
                                <p>No pending clauses at the moment.</p>
                            </div>
                        </div>

                        <!-- Passed Clauses Section (Collapsible) -->
                        <div class="section-header collapsible-header" @click="toggleSection('passed')">
                            <div class="section-title">
                                <i class="fas fa-check-circle"></i> Passed Clauses
                                <span class="section-count">{{ passedClauses.length }}</span>
                            </div>
                            <i
                                :class="['fas', 'fa-chevron-down', 'toggle-icon', sectionStates.passed ? 'toggle-icon-open' : '']"></i>
                        </div>
                        <div
                            :class="['collapsible-section', sectionStates.passed ? 'collapsible-section-visible' : 'collapsible-section-hidden']">
                            <div class="clause-cards">
                                <div v-for="clause in passedClauses" :key="clause.id" class="clause-card passed-card"
                                    @click="viewClause(clause)">
                                    <div class="card-header">{{ clause.title || clause.filename }}</div>
                                    <div class="card-body">
                                        <p><strong>Submitted by:</strong> {{ clause.country }}</p>
                                        <p><strong>Passed on:</strong> {{ formatDate(clause.timestamp) }}</p>
                                    </div>
                                </div>
                            </div>
                            <div v-if="passedClauses.length === 0" class="empty-state">
                                <i class="fas fa-check fa-2x"></i>
                                <p>No passed clauses yet.</p>
                            </div>
                        </div>

                        <!-- Rejected Clauses Section (Collapsible) -->
                        <div class="section-header collapsible-header" @click="toggleSection('rejected')">
                            <div class="section-title">
                                <i class="fas fa-times-circle"></i> Rejected Clauses
                                <span class="section-count">{{ rejectedClauses.length }}</span>
                            </div>
                            <i
                                :class="['fas', 'fa-chevron-down', 'toggle-icon', sectionStates.rejected ? 'toggle-icon-open' : '']"></i>
                        </div>
                        <div
                            :class="['collapsible-section', sectionStates.rejected ? 'collapsible-section-visible' : 'collapsible-section-hidden']">
                            <div class="clause-cards">
                                <div v-for="clause in rejectedClauses" :key="clause.id"
                                    class="clause-card rejected-card" @click="viewClause(clause)">
                                    <div class="card-header">{{ clause.title || clause.filename }}</div>
                                    <div class="card-body">
                                        <p><strong>Submitted by:</strong> {{ clause.country }}</p>
                                        <p><strong>Rejected on:</strong> {{ formatDate(clause.timestamp) }}</p>
                                    </div>
                                </div>
                            </div>
                            <div v-if="rejectedClauses.length === 0" class="empty-state">
                                <i class="fas fa-ban fa-2x"></i>
                                <p>No rejected clauses yet.</p>
                            </div>
                        </div>
                    </div>

                    <AmendmentsView v-if="contentType === 'amendments' && selectedCommittee"
                        :committee="selectedCommittee" />
                </div>

                <!-- Clauses View (shown when clausesHtml is not null) -->
                <ClausesView v-if="clausesHtml" :initialHtmlData="clausesHtml" :group="selectedCommittee"
                    :clauseId="currentClauseId" @go-back="handleGoBack" />

                <GossipPortal v-model:show="showGossipPortal" v-if="isAuthenticated" />
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onBeforeMount, onBeforeUnmount, watch, onMounted, computed, reactive } from 'vue';
import axios from 'axios';
import AmendmentsView from '../components/amendmentsView.vue';
import ClausesView from '../components/display.vue';
import LoginDialog from '../components/login.vue';
import { io } from 'socket.io-client';
import { useRouter } from 'vue-router';
import GossipPortal from '../components/GossipPortal.vue';
import { GlassMessage } from '../components/ui';

export default {
    name: 'ChairComponent',
    components: {
        AmendmentsView,
        ClausesView,
        LoginDialog,
        GossipPortal,
    },
    setup() {
        const router = useRouter();

        // Persistent state using sessionStorage
        const selectedCommittee = ref(sessionStorage.getItem('chairSelectedCommittee') || '');
        const contentType = ref(sessionStorage.getItem('chairContentType') || '');
        const isSidebarFolded = ref(sessionStorage.getItem('chairSidebarFolded') === 'true');

        // Section states for collapsible sections
        const sectionStates = reactive({
            passed: false,
            rejected: false
        });

        // Toggle section visibility
        const toggleSection = (section) => {
            sectionStates[section] = !sectionStates[section];
        };

        // Watchers to persist state
        watch(selectedCommittee, (newVal) => {
            sessionStorage.setItem('chairSelectedCommittee', newVal);
        });

        watch(contentType, (newVal) => {
            sessionStorage.setItem('chairContentType', newVal);
        });

        watch(isSidebarFolded, (newVal) => {
            sessionStorage.setItem('chairSidebarFolded', newVal);
        });

        const socket = io('http://127.0.0.1:8000');
        console.log('[CHAIR] Creating socket connection in setup');
        socket.on('connect', () => {
            console.log('[CHAIR] Socket connected with ID:', socket.id);
        });
        const contentList = ref([]);
        const clausesHtml = ref(null);
        const currentClauseId = ref(null);
        const isAuthenticated = ref(localStorage.getItem('token') !== null);
        const publishedClauses = ref([]);
        const rejectedClauses = ref([]);
        const passedClauses = ref([]);
        const pendingClauses = ref([]);
        const previousState = ref({
            committee: '',
            contentType: '',
        });
        const showGossipPortal = ref(false);

        const fetchContent = async () => {
            if (!selectedCommittee.value || !contentType.value) {
                return;
            }

            if (contentType.value === 'clauses') {
                try {
                    const committee = selectedCommittee.value.toLowerCase();
                    console.log('Fetching clauses for committee:', committee);
                    const response = await axios.get(`http://127.0.0.1:8000/files/${committee}`);
                    console.log('Received clauses:', response.data);

                    // Categorize clauses
                    publishedClauses.value = response.data.filter(clause => clause.is_published);
                    rejectedClauses.value = response.data.filter(clause => clause.is_rejected);
                    passedClauses.value = response.data.filter(clause => clause.is_passed);
                    pendingClauses.value = response.data.filter(clause =>
                        !clause.is_published && !clause.is_rejected && !clause.is_passed
                    );

                    // Keep the full list for reference
                    contentList.value = response.data;
                } catch (error) {
                    console.error('Failed to fetch data:', error);
                    alert('Failed to fetch data.');
                }
            }
        };

        const viewClause = async (clause) => {
            // Check if we received a full clause object or just an ID
            const clauseId = typeof clause === 'object' ? clause.id : clause;

            // Add the clause to view history for back button functionality
            previousState.value = {
                type: 'list',
                committee: selectedCommittee.value,
                contentType: contentType.value // Save current content type
            };

            try {
                const response = await axios.get(`http://127.0.0.1:8000/clause/${clauseId}`);
                clausesHtml.value = response.data.html_content;
                currentClauseId.value = clauseId;
                contentType.value = 'clause-detail';

                console.log(`Viewing clause ${clauseId}`);
            } catch (error) {
                console.error('Failed to load clause content:', error);
                alert('Failed to load clause content.');
            }
        };

        const handleGoBack = () => {
            clausesHtml.value = null;
            currentClauseId.value = null;

            // Restore the previous content type
            if (previousState.value.contentType) {
                contentType.value = previousState.value.contentType;
            } else {
                contentType.value = 'clauses'; // Default fallback
            }

            fetchContent(); // Refresh the content list

            // Make sure the state is persisted to session storage
            sessionStorage.setItem('chairContentType', contentType.value);
        };

        const handleLoginSuccess = () => {
            isAuthenticated.value = true;
        };

        const selectCommittee = (committee) => {
            console.log('Committee selected:', committee);
            if (typeof committee === 'string' && committee.trim() !== '') {
                // Store previous state if changing committee
                if (selectedCommittee.value !== committee) {
                    previousState.value = {
                        committee: selectedCommittee.value,
                        contentType: contentType.value
                    };
                }

                selectedCommittee.value = committee;
                clausesHtml.value = null; // Close any open clause view

                // If content type is already selected, fetch new content
                if (contentType.value) {
                    fetchContent();
                }

                // Save to session storage
                sessionStorage.setItem('chairSelectedCommittee', committee);
                sessionStorage.setItem('chairContentType', contentType.value);
            }
        };

        const selectContentType = (type) => {
            console.log('Content type selected:', type);
            if (typeof type === 'string' && type.trim() !== '') {
                // Store previous state if changing content type
                if (contentType.value !== type) {
                    previousState.value = {
                        committee: selectedCommittee.value,
                        contentType: contentType.value
                    };
                }

                contentType.value = type;
                clausesHtml.value = null; // Close any open clause view

                if (selectedCommittee.value) {
                    fetchContent();
                }

                // Save to session storage
                sessionStorage.setItem('chairContentType', type);
            }
        };

        const toggleSidebar = () => {
            isSidebarFolded.value = !isSidebarFolded.value;
            sessionStorage.setItem('chairSidebarFolded', isSidebarFolded.value);
        };

        watch(selectedCommittee, (newVal, oldVal) => {
            if (newVal !== oldVal) {
                console.log('Committee changed, resetting states');
                clausesHtml.value = null;
                if (contentType.value) {
                    fetchContent();
                }
            }
        });

        const formatDate = (timestamp) => {
            if (!timestamp) {
                return 'N/A';
            }

            let date;

            // Check if timestamp is a string that looks like an ISO date
            if (typeof timestamp === 'string' && timestamp.includes('T')) {
                // Handle ISO format like "2025-03-05T02:42:20.266930"
                date = new Date(timestamp);
            } else if (!isNaN(Number(timestamp))) {
                // Handle numeric timestamp (seconds or milliseconds)
                const timeMs = timestamp.toString().length === 10
                    ? Number(timestamp) * 1000
                    : Number(timestamp);
                date = new Date(timeMs);
            } else {
                // Handle as date string
                date = new Date(timestamp);
            }

            // Check if date is valid
            if (!date || isNaN(date.getTime())) {
                console.log('Invalid date format:', timestamp);
                return 'Invalid date';
            }

            // Format: Month Day, Year at Hour:Minute
            const months = [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ];

            const month = months[date.getMonth()];
            const day = date.getDate();
            const year = date.getFullYear();

            // Get hours and minutes with leading zeros if needed
            let hours = date.getHours();
            const minutes = date.getMinutes().toString().padStart(2, '0');

            // Format for 24-hour time
            const formattedTime = `${hours}:${minutes}`;

            return `${month} ${day}, ${year} at ${formattedTime}`;
        };

        // Setup socket listeners for real-time updates
        const setupSocketListeners = () => {
            socket.on('connect', () => {
                console.log('Connected to websocket');
            });

            socket.on('new_clause', (data) => {
                console.log('Received new clause:', data);
                if (data.committee.toLowerCase() === selectedCommittee.value.toLowerCase() &&
                    contentType.value === 'clauses') {
                    fetchContent();
                    GlassMessage.info(`New clause uploaded by ${data.country}`);
                }
            });

            socket.on('clause_published', (data) => {
                console.log('[CHAIR] Received clause_published event:', data);
                if (data.committee.toLowerCase() === selectedCommittee.value.toLowerCase()) {
                    console.log('[CHAIR] Committee matches, fetching content');
                    fetchContent();

                    // Check if the silent flag exists and is explicitly set to true
                    // This ensures we don't show a message if silent is true
                    if (data.silent !== true) {
                        console.log('[CHAIR] silent is not true, showing success message');
                        GlassMessage.success('A clause has been published');
                    } else {
                        console.log('[CHAIR] silent=true, not showing success message');
                    }
                } else {
                    console.log('[CHAIR] Committee does not match, ignoring event');
                }
            });

            socket.on('clause_rejected', (data) => {
                console.log('[CHAIR] Received clause_rejected event:', data);
                if (data.committee.toLowerCase() === selectedCommittee.value.toLowerCase()) {
                    console.log('[CHAIR] Committee matches, fetching content');
                    fetchContent();
                    // Only show the message if the silent flag is not set
                    if (!data.silent) {
                        console.log('[CHAIR] silent=false, showing warning message');
                        GlassMessage.warning('A clause has been rejected');
                    } else {
                        console.log('[CHAIR] silent=true, not showing warning message');
                    }
                } else {
                    console.log('[CHAIR] Committee does not match, ignoring event');
                }
            });

            socket.on('clause_unpublished', (data) => {
                console.log('[CHAIR] Received clause_unpublished event:', data);
                if (data.committee.toLowerCase() === selectedCommittee.value.toLowerCase()) {
                    console.log('[CHAIR] Committee matches, fetching content');
                    fetchContent();
                    // Only show the message if the silent flag is not set
                    if (!data.silent) {
                        console.log('[CHAIR] silent=false, showing info message');
                        GlassMessage.info('A clause has been unpublished');
                    } else {
                        console.log('[CHAIR] silent=true, not showing info message');
                    }
                } else {
                    console.log('[CHAIR] Committee does not match, ignoring event');
                }
            });

            socket.on('error', (error) => {
                console.error('Socket error:', error);
            });
        };

        const goBack = () => {
            if (previousState.value.committee || previousState.value.contentType) {
                selectedCommittee.value = previousState.value.committee;
                contentType.value = previousState.value.contentType;
                clausesHtml.value = null;

                if (selectedCommittee.value && contentType.value) {
                    fetchContent();

                    // Persist state to session storage
                    sessionStorage.setItem('chairSelectedCommittee', selectedCommittee.value);
                    sessionStorage.setItem('chairContentType', contentType.value);
                }

                // Clear previous state after using it
                previousState.value = { committee: '', contentType: '' };
            }
        };

        onMounted(() => {
            setupSocketListeners();
            // Restore previous state from sessionStorage
            const savedCommittee = sessionStorage.getItem('chairSelectedCommittee');
            const savedContentType = sessionStorage.getItem('chairContentType');

            if (savedCommittee) {
                selectedCommittee.value = savedCommittee;
            }
            if (savedContentType) {
                contentType.value = savedContentType;
            }

            // Fetch content if both committee and content type are available
            if (selectedCommittee.value && contentType.value) {
                fetchContent();
            }
        });

        onBeforeUnmount(() => {
            socket.disconnect();
            sessionStorage.setItem('chairSelectedCommittee', selectedCommittee.value);
        });

        return {
            selectedCommittee,
            contentType,
            contentList,
            publishedClauses,
            rejectedClauses,
            passedClauses,
            pendingClauses,
            clausesHtml,
            currentClauseId,
            isAuthenticated,
            isSidebarFolded,
            handleGoBack,
            handleLoginSuccess,
            selectCommittee,
            selectContentType,
            toggleSidebar,
            viewClause,
            formatDate,
            previousState,
            goBack,
            showGossipPortal,
            sectionStates,
            toggleSection
        };
    },
};
</script>

<style scoped>
/* Setting new colors */
.container {
    --primary: #2c8a54;
    /* Professional green as primary */
    --primary-dark: #1e6140;
    /* Darker green for hover states */
    --primary-light: #e8f5ee;
    /* Light green for backgrounds */

    --pending: #f39c12;
    /* Orange for pending */
    --passed: #27ae60;
    /* Green for passed */
    --rejected: #e74c3c;
    /* Red for rejected */

    --text-dark: #333333;
    --text-medium: #555555;
    --text-light: #777777;

    --border-light: #d4eede;
    --border-medium: #a5d9bc;

    --shadow-light: rgba(44, 138, 84, 0.1);
    --shadow-medium: rgba(44, 138, 84, 0.2);
}

.container {
    display: flex;
    width: 100%;
    height: 100vh;
    margin: 0;
    padding: 0;
}

.sidebar {
    width: 200px;
    border-right: 1px solid var(--border-medium);
    padding: 15px;
    transition: width 0.3s ease;
    height: 100vh;
    overflow-y: auto;
    background-color: transparent;
}

.sidebar-content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
}

.top-nav {
    flex-grow: 1;
}

.bottom-nav {
    margin-top: auto;
    margin-bottom: 20px;
}

.sidebar.folded {
    width: 50px;
    padding: 15px 5px;
}

.sidebar ul {
    list-style: none;
    padding: 0;
    margin: 15px 0;
}

.sidebar li {
    padding: 10px;
    margin: 5px 0;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 4px;
    border: 1px solid transparent;
}

.sidebar li:hover {
    background-color: var(--primary-light);
    border-color: var(--primary);
}

.sidebar li.active {
    background-color: var(--primary);
    color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    font-weight: bold;
    /* Add a little more contrast for better visibility */
    border: 2px solid var(--primary-dark);
}

.toggle-button {
    background: var(--primary-light);
    border: 1px solid var(--primary);
    border-radius: 4px;
    color: var(--primary);
    cursor: pointer;
    margin-bottom: 10px;
    padding: 5px 10px;
    width: 100%;
}

.toggle-button:hover {
    background-color: var(--primary);
    color: white;
}

.main-content {
    display: flex;
    width: 100%;
}

.content {
    flex-grow: 1;
    padding-left: 20px;
    transition: margin-left 0.3s ease;
    height: 100%;
}

.content.full-width {
    margin-left: 0;
}

.content-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

.content-table th,
.content-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
}

.clause-section {
    margin-bottom: 25px;
}

.clause-section h3 {
    color: #333;
    margin: 20px 0 10px 0;
    padding-bottom: 5px;
    border-bottom: 2px solid #eee;
}

.published-clause {
    background-color: var(--primary-light);
}

.passed-clause {
    background-color: #e8f5e9;
}

.rejected-clause {
    background-color: #ffebee;
}

.content-table tr:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

.back-button {
    width: 100%;
    padding: 8px;
    margin-bottom: 15px;
    background-color: var(--primary-light);
    border: 1px solid var(--primary);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
    color: var(--primary-dark);
    font-weight: 500;
}

.back-button:hover {
    background-color: var(--primary);
    border-color: var(--primary-dark);
    color: white;
}

.gossip-section {
    margin-bottom: 0;
    border-top: 1px solid var(--border-medium);
    padding-top: 10px;
}

.gossip-nav-item {
    padding: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.gossip-nav-item:hover {
    background-color: var(--primary-light);
}

.gossip-nav-item.active {
    background-color: var(--primary);
    color: white;
    border-radius: 4px;
}

.folded-gossip {
    padding: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    font-weight: bold;
    margin: 5px auto;
}

.folded-gossip:hover {
    background-color: var(--primary-light);
}

.folded-gossip.active {
    background-color: var(--primary);
    color: white;
    border-radius: 4px;
}

.clauses-container {
    margin-bottom: 30px;
}

.clause-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    width: 100%;
}

.clause-card {
    flex: 0 0 calc(33.333% - 14px);
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    cursor: pointer;
    background-color: white;
    position: relative;
}

.clause-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.clause-card::before {
    content: '';
    height: 5px;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
}

.pending-card::before {
    background-color: var(--pending);
}

.passed-card::before {
    background-color: var(--passed);
}

.rejected-card::before {
    background-color: var(--rejected);
}

.card-header {
    padding: 15px;
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--text-dark);
    background-color: var(--primary-light);
    border-bottom: 1px solid var(--border-medium);
}

.card-body {
    padding: 15px;
}

.card-body p {
    margin: 8px 0;
    color: var(--text-medium);
}

/* Published clause styling */
.published-clause-card {
    width: 100%;
    border: 1px solid var(--border-medium);
    border-radius: 8px;
    overflow: hidden;
    background-color: #ffffff;
    box-shadow: 0 4px 12px var(--shadow-light);
    margin-bottom: 20px;
}

.status-badge {
    background-color: var(--primary);
    color: white;
    padding: 10px 15px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.published-details {
    padding: 15px;
    background-color: #ffffff;
}

.detail-row {
    padding: 8px 0;
    display: flex;
    border-bottom: 1px solid var(--border-light);
    color: var(--text-dark);
}

.detail-row:last-child {
    border-bottom: none;
}

.detail-label {
    font-weight: 600;
    color: var(--primary-dark);
    min-width: 120px;
}

.detail-value {
    flex: 1;
    color: var(--text-medium);
}

/* Empty states */
.empty-state,
.empty-published {
    text-align: center;
    padding: 30px;
    background-color: #f9f9f9;
    border-radius: 8px;
    color: var(--text-light);
    margin: 15px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}

.empty-published {
    background-color: var(--primary-light);
    border: 2px dashed var(--border-medium);
    padding: 40px;
}

.empty-state i,
.empty-published i {
    color: var(--text-light);
    margin-bottom: 10px;
}

/* Buttons */
.action-button {
    background-color: var(--passed);
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
    font-weight: 500;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-button:hover {
    background-color: #229954;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.action-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Responsive adjustments */
@media (max-width: 1200px) {
    .clause-card {
        flex: 0 0 calc(50% - 10px);
    }
}

@media (max-width: 768px) {
    .clause-card {
        flex: 0 0 100%;
    }

    .detail-row {
        flex-direction: column;
    }

    .detail-label {
        margin-bottom: 5px;
        min-width: 100%;
    }

    .content {
        padding-left: 10px;
        padding-right: 10px;
    }
}

/* Section styling */
.section-header {
    margin: 30px 0 15px;
    padding: 12px 20px;
    background-color: var(--primary-light);
    border-radius: 8px;
    border-left: 5px solid var(--primary);
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: default;
    box-shadow: 0 2px 4px var(--shadow-light);
}

.collapsible-header {
    cursor: pointer;
    transition: background-color 0.2s, transform 0.2s;
    border-left-color: var(--border-medium);
}

.collapsible-header:hover {
    background-color: #c7e6d7;
    transform: translateY(-1px);
}

.section-title {
    font-weight: 600;
    color: var(--primary);
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-count {
    background-color: var(--border-medium);
    color: var(--primary-dark);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.9rem;
    font-weight: 600;
}

.collapsible-section {
    overflow: hidden;
    transition: all 0.3s ease-in-out;
}

.collapsible-section-hidden {
    max-height: 0;
    opacity: 0;
    margin-top: 0;
    margin-bottom: 0;
    pointer-events: none;
}

.collapsible-section-visible {
    max-height: 2000px;
    /* Or a suitable large value */
    opacity: 1;
    margin-top: 15px;
    margin-bottom: 30px;
}

.toggle-icon {
    color: var(--primary);
    transition: transform 0.3s ease;
}

.toggle-icon-open {
    transform: rotate(180deg);
}

/* Published clause slot */
.published-clause-slot {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
    border: 1px solid #e0e0e0;
}

.empty-slot {
    padding: 30px;
    text-align: center;
    color: #666;
    font-style: italic;
    background-color: rgba(44, 138, 84, 0.05);
    border-radius: 4px;
}

.empty-message {
    display: block;
    margin: 10px 0;
}

.pending-clauses-section {
    margin-bottom: 30px;
}



/* Keep clause card styling */
.published-clause .clause-card {
    width: 100%;
    max-width: none;
    margin-bottom: 0;
}

.empty-state {
    text-align: center;
    padding: 20px;
    color: var(--text-light);
    background-color: #f5f5f5;
    border-radius: 4px;
    margin: 15px 0;
}

.content-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}
</style>
