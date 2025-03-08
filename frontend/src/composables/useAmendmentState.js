import { ref, readonly } from 'vue';

// Create singleton state that will be shared between components
const editingContent = ref('');
const editingAmendmentId = ref(null);
const originalContent = ref('');
const isEditingActive = ref(false);

export function useAmendmentState() {
    // Function to update the amendment editing state
    const updateAmendmentEdit = (newEditingContent, amendmentId, origContent) => {
        editingContent.value = newEditingContent;
        editingAmendmentId.value = amendmentId;
        originalContent.value = origContent || '';
        isEditingActive.value = true;
    };

    // Function to clear the amendment editing state
    const clearAmendmentEdit = () => {
        editingContent.value = '';
        editingAmendmentId.value = null;
        originalContent.value = '';
        isEditingActive.value = false;
    };

    return {
        // Expose state as readonly to prevent direct mutation
        editingContent: readonly(editingContent),
        editingAmendmentId: readonly(editingAmendmentId),
        originalContent: readonly(originalContent),
        isEditingActive: readonly(isEditingActive),
        
        // Expose methods to update state
        updateAmendmentEdit,
        clearAmendmentEdit
    };
} 