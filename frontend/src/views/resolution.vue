<template>
    <div class="document-container">
        <div class="title-container">
            <h1 class="resolution-title">{{ formattedCommitteeName }} Committee Resolutions</h1>
        </div>

        <!-- Single A4 page containing all resolutions -->
        <div class="a4-page">
            <div class="document-content" v-html="sanitizedResolutions"></div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import io from 'socket.io-client';
import DOMPurify from 'dompurify';

export default {
    data() {
        return {
            resolutions: [],
            committeeName: this.$route.params.committee,
            socket: null,
            committeeNameMap: {
                'junior': 'Junior',
                'senior': 'Senior',
                'security-council': 'Security Council'
            }
        };
    },
    created() {
        this.fetchResolutions();
        this.setupWebSocket();
    },
    computed: {
        formattedCommitteeName() {
            // Use the mapping if available, otherwise capitalize the first letter
            return this.committeeNameMap[this.committeeName] || 
                   this.committeeName.charAt(0).toUpperCase() + this.committeeName.slice(1);
        },
        combinedResolutions() {
            // Process all resolutions into a single document
            const processedResolutions = this.resolutions.map(resolution => {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = resolution.trim();

                const pElements = [];
                tempDiv.childNodes.forEach(node => {
                    if (node.nodeName === 'P') {
                        // Skip paragraphs that only contain &nbsp; or are empty
                        const content = node.textContent.trim();
                        if (content !== '' && content !== '\u00A0' && !/^(&nbsp;|\s)+$/.test(node.innerHTML)) {
                            pElements.push(node.outerHTML);
                        }
                    }
                });

                const olElement = tempDiv.querySelector('ol');
                const firstLevelLis = [];
                if (olElement) {
                    olElement.childNodes.forEach(node => {
                        if (node.nodeName === 'LI') {
                            firstLevelLis.push(node.outerHTML);
                        }
                    });
                }

                return {
                    paragraphs: pElements.join(''),
                    listItems: firstLevelLis.join('')
                };
            });

            // Combine all resolutions into a single document
            const mergedParagraphs = processedResolutions.map(r => r.paragraphs).join('');
            const mergedListItems = processedResolutions.map(r => r.listItems).join('');

            return DOMPurify.sanitize(`
                ${mergedParagraphs}
                ${mergedListItems ? `<ol>${mergedListItems}</ol>` : ''}
            `);
        },
        sanitizedResolutions() {
            return this.combinedResolutions;
        }
    },
    beforeUnmount() {
        if (this.socket) {
            this.socket.disconnect();
            console.log('Socket disconnected');
        }
    },
    methods: {
        fetchResolutions() {
            // Use the URL parameter as-is for API requests
            axios.get(`http://127.0.0.1:8000/api/resolutions/${this.committeeName}`)
                .then(response => {
                    this.resolutions = response.data;
                })
                .catch(error => {
                    console.error('Error fetching resolutions:', error);
                });
        },
        setupWebSocket() {
            this.socket = io('http://127.0.0.1:8000'); // Replace with your backend server URL

            this.socket.on(`update-${this.committeeName}`, (newResolution) => {
                this.resolutions.push(newResolution);
                console.log('New resolution received:', newResolution);
            });
        },
    },
};
</script>

<style>
/* Import Apatos font if not already imported globally */
@import url('https://fonts.googleapis.com/css2?family=Apatos:wght@400;500;600;700&display=swap');

.document-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    /* Prevent inheritance from glass-bg parent */
    color: #333333;
    all: initial;
    font-family: inherit;
    /* Restore the container styling after resetting inheritance */
    display: block;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

/* Title container to ensure proper positioning */
.title-container {
    width: 100%;
    text-align: center;
    margin-bottom: 30px;
    position: relative;
    z-index: 10;
}

/* Resolution title with !important to override any other styles */
.resolution-title {
    color: #FFFFFF !important;
    font-size: 2rem !important;
    font-weight: bold !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    margin: 0 !important;
    padding: 0 !important;
    display: inline-block !important;
    text-align: center !important;
    font-family: 'Apatos', sans-serif !important;
}

/* Re-style all elements to ensure they're not inheriting from parent */
.document-container * {
    all: revert;
}

/* Exclude the title from the revert */
.document-container .title-container,
.document-container .resolution-title {
    all: initial;
    display: block;
}

.document-container .title-container {
    width: 100%;
    text-align: center;
    margin-bottom: 30px;
}

.document-container .resolution-title {
    color: #FFFFFF;
    font-size: 2rem;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    font-family: 'Apatos', sans-serif;
}

h1 {
    color: #FFFFFF;
    margin-bottom: 30px;
    text-align: center;
    width: 100%;
    display: block;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.a4-page {
    background-color: rgba(255, 255, 255, 0.7);
    width: 210mm;
    min-height: 297mm;
    margin: 20px auto;
    padding: 20mm;
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
    page-break-after: always;
}

.document-content {
    font-family: 'Apatos', sans-serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000000;
}

/* Style paragraph elements */
.document-content p {
    color: #000000;
    margin-bottom: 1em;
}

/* Style ordered lists */
.document-content ol {
    padding-left: 2em;
    color: #000000;
}

.document-content li {
    margin-bottom: 0.5em;
}

@media print {
    .document-container {
        padding: 0;
        background: none;
        all: revert;
    }

    .a4-page {
        background: white;
        box-shadow: none;
        border: none;
        backdrop-filter: none;
        -webkit-backdrop-filter: none;
        margin: 0;
        padding: 20mm;
        page-break-before: always;
    }

    .a4-page:first-child {
        page-break-before: avoid;
    }

    h1:not(.resolution-title) {
        color: #000000;
    }

    /* Ensure title remains white even when printing */
    .resolution-title,
    .document-container .resolution-title {
        color: #FFFFFF !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        font-family: 'Apatos', sans-serif !important;
    }

    /* Ensure title container is properly positioned */
    .title-container,
    .document-container .title-container {
        width: 100% !important;
        text-align: center !important;
        margin-bottom: 30px !important;
    }
}
</style>
