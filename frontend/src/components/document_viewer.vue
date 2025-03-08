<template>
  <div style="height: 83vh;">
    <div class="header">
      <h1>{{ clauseData.filename }}</h1>
      <GlassButton type="primary" @click="goBack">Back</GlassButton>
    </div>
    <div v-html="sanitizedContent" class="document-content"></div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DOMPurify from 'dompurify'
import axios from 'axios'
import { GlassButton, GlassMessage } from '../components/ui'

const route = useRoute()
const router = useRouter()
const clauseId = route.params.id as string
const clauseData = ref({ filename: '', html_content: '' })

// Computed property for sanitized content
const sanitizedContent = computed(() => {
  return DOMPurify.sanitize(clauseData.value.html_content)
})

const goBack = () => {
  router.push('/clauses_upload')
}

// Fetch the document content when the component is mounted
onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/clause/${clauseId}`)
    clauseData.value = response.data
  } catch (error: any) {
    GlassMessage.error('Failed to load document content.')
    console.error('Error loading document:', error)
  }
})
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  justify-content: space-between;
}

.document-content {
  background-color: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: var(--text-color, rgba(255, 255, 255, 0.9));
  max-height: calc(83vh - 80px);
  overflow-y: auto;
}

.document-content :deep(p) {
  margin-bottom: 1rem;
}

.document-content :deep(ul),
.document-content :deep(ol) {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}

.document-content :deep(h1),
.document-content :deep(h2),
.document-content :deep(h3) {
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}
</style>
