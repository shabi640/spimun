<template>
  <div>
    <div class="main-container">
      <div class="editor-container editor-container_document-editor" ref="editorContainerElement">
        <div class="editor-container__menu-bar" ref="editorMenuBarElement"></div>
        <div class="editor-container__toolbar" ref="editorToolbarElement"></div>
        <div class="editor-container__editor-wrapper">
          <div class="editor-container__editor">
            <div ref="editorElement">
              <ckeditor v-if="isLayoutReady" :editor="editor" :config="config" v-model="editorData" @ready="onReady" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  DecoupledEditor,
  AccessibilityHelp,
  Alignment,
  Autoformat,
  Autosave,
  BalloonToolbar,
  Bold,
  Code,
  Essentials,
  FindAndReplace,
  FontFamily,
  FontSize,
  Heading,
  Highlight,
  HorizontalLine,
  Indent,
  IndentBlock,
  Italic,
  List,
  ListProperties,
  Mention,
  PageBreak,
  Paragraph,
  PasteFromOffice,
  RemoveFormat,
  SelectAll,
  SimpleUploadAdapter,
  SpecialCharacters,
  SpecialCharactersArrows,
  SpecialCharactersCurrency,
  SpecialCharactersEssentials,
  SpecialCharactersLatin,
  SpecialCharactersMathematical,
  SpecialCharactersText,
  Strikethrough,
  Subscript,
  Superscript,
  TodoList,
  Underline,
  Undo
} from 'ckeditor5';

import 'ckeditor5/ckeditor5.css';

export default {
  name: 'app',
  props: {
    modelValue: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      isLayoutReady: false,
      config: null,
      editor: DecoupledEditor,
      editorData: this.modelValue
    };
  },
  watch: {
    // Watch for changes in modelValue (from parent component)
    modelValue(newValue) {
      console.log('modelValue changed:', newValue);
      this.editorData = newValue;
    },
    // Emit changes in editorData back to parent component
    editorData(newValue) {
      this.$emit('update:modelValue', newValue);
    }
  },
  mounted() {
    this.config = {
      toolbar: {
        items: [
          'undo',
          'redo',
          '|',
          'heading',
          '|',
          'fontSize',
          'fontFamily',
          '|',
          'bold',
          'italic',
          'underline',
          'strikethrough',
          '|',
          'highlight',
          '|',
          'alignment',
          '|',
          'numberedList',
        ],
        shouldNotGroupWhenFull: false
      },
      plugins: [
        AccessibilityHelp,
        Alignment,
        Autoformat,
        Autosave,
        BalloonToolbar,
        Bold,
        Code,
        Essentials,
        FindAndReplace,
        FontFamily,
        FontSize,
        Heading,
        Highlight,
        HorizontalLine,
        Indent,
        IndentBlock,
        Italic,
        List,
        ListProperties,
        Mention,
        PageBreak,
        Paragraph,
        PasteFromOffice,
        RemoveFormat,
        SelectAll,
        SimpleUploadAdapter,
        SpecialCharacters,
        SpecialCharactersArrows,
        SpecialCharactersCurrency,
        SpecialCharactersEssentials,
        SpecialCharactersLatin,
        SpecialCharactersMathematical,
        SpecialCharactersText,
        Strikethrough,
        Subscript,
        Superscript,
        TodoList,
        Underline,
        Undo
      ],
      balloonToolbar: ['bold', 'italic', '|', 'bulletedList', 'numberedList'],
      fontFamily: {
        supportAllValues: true
      },
      fontSize: {
        options: [10, 12, 14, 'default', 18, 20, 22],
        supportAllValues: true
      },
      heading: {
        options: [
          {
            model: 'paragraph',
            title: 'Paragraph',
            class: 'ck-heading_paragraph'
          },
          {
            model: 'heading1',
            view: 'h1',
            title: 'Heading 1',
            class: 'ck-heading_heading1'
          },
          {
            model: 'heading2',
            view: 'h2',
            title: 'Heading 2',
            class: 'ck-heading_heading2'
          },
          {
            model: 'heading3',
            view: 'h3',
            title: 'Heading 3',
            class: 'ck-heading_heading3'
          },
          {
            model: 'heading4',
            view: 'h4',
            title: 'Heading 4',
            class: 'ck-heading_heading4'
          },
          {
            model: 'heading5',
            view: 'h5',
            title: 'Heading 5',
            class: 'ck-heading_heading5'
          },
          {
            model: 'heading6',
            view: 'h6',
            title: 'Heading 6',
            class: 'ck-heading_heading6'
          }
        ]
      },
      list: {
        properties: {
          styles: true,
          startIndex: true,
          reversed: true
        }
      },
      menuBar: {
        isVisible: true
      },
      placeholder: 'Submit our amendment here!',
      table: {
        contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties']
      },
      highlight: {
        options: [
          {
            model: 'yellowMarker',
            class: 'marker-yellow',
            title: 'Yellow marker',
            color: 'var(--ck-highlight-marker-yellow)',
            type: 'marker'
          },
          {
            model: 'greenMarker',
            class: 'marker-green',
            title: 'Green marker',
            color: 'var(--ck-highlight-marker-green)',
            type: 'marker'
          },
          {
            model: 'pinkMarker',
            class: 'marker-pink',
            title: 'Pink marker',
            color: 'var(--ck-highlight-marker-pink)',
            type: 'marker'
          },
          {
            model: 'blueMarker',
            class: 'marker-blue',
            title: 'Blue marker',
            color: 'var(--ck-highlight-marker-blue)',
            type: 'marker'
          },
          {
            model: 'redPen',
            class: 'pen-red',
            title: 'Red pen',
            color: 'var(--ck-highlight-pen-red)',
            type: 'pen'
          },
          {
            model: 'greenPen',
            class: 'pen-green',
            title: 'Green pen',
            color: 'var(--ck-highlight-pen-green)',
            type: 'pen'
          }
        ]
      }
    };

    this.isLayoutReady = true;
  },
  methods: {
    onReady(editor) {
      Array.from(this.$refs.editorToolbarElement.children).forEach(child => child.remove());
      Array.from(this.$refs.editorMenuBarElement.children).forEach(child => child.remove());

      this.$refs.editorToolbarElement.appendChild(editor.ui.view.toolbar.element);
      this.$refs.editorMenuBarElement.appendChild(editor.ui.view.menuBarView.element);
      editor.setData(this.modelValue);
      console.log(this.modelValue);

      // Fix dropdown positioning in the editor
      editor.ui.focusTracker.on('change:isFocused', () => {
        // Ensure proper z-index hierarchy when editor is focused
        if (editor.ui.focusTracker.isFocused) {
          this.$refs.editorContainerElement.style.zIndex = '1000';
        } else {
          this.$refs.editorContainerElement.style.zIndex = '1';
        }
      });
    }
  }
};
</script>

<style>
@media print {
  body {
    margin: 0 !important;
  }
}

.main-container {
  --ckeditor5-preview-height: 600px;
  font-family: 'Lato';
  width: 95%;
  /* Set a flexible width to make it responsive */
  max-width: 800px;
  /* Add a maximum width to prevent it from becoming too large on bigger screens */
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
  border-radius: 10px;
}

.ck-content {
  font-family: 'Arial';
  line-height: 1.6;
  word-break: break-word;
  color: #000000;
  text-shadow: none;
  position: relative;
  z-index: 1;
  border-radius: 6px;
}

/* Ensure consistent font color for all elements */
.ck-content *,
.ck-content p,
.ck-content h1,
.ck-content h2,
.ck-content h3,
.ck-content h4,
.ck-content h5,
.ck-content h6,
.ck-content li,
.ck-content span,
.ck-content div,
.ck-content a,
.ck-content table,
.ck-content td,
.ck-content th,
.ck-content blockquote,
.ck-content pre,
.ck-content code {
  color: #000000 !important;
}

/* Fix transparency inconsistency between paragraphs and list items */
.ck-content p,
.ck-content li,
.ck-content li p,
.ck-content>p,
.ck-content>li,
.ck-content ol>li,
.ck-content ul>li,
.ck-content ol>li>p,
.ck-content ul>li>p {
  color: #000000 !important;
  opacity: 1 !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
  text-rendering: optimizeLegibility !important;
  font-weight: 400 !important;
  background: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  filter: none !important;
  mix-blend-mode: normal !important;
  text-shadow: 0 0 0 #000000 !important;
}

/* Ensure consistent text color for paragraphs and list items with higher specificity */
.ck-content p,
.ck-content>p,
.ck-content li,
.ck-content li>p,
.ck-content ol>li,
.ck-content ul>li,
.ck-content ol>li>p,
.ck-content ul>li>p {
  color: #000000 !important;
  font-weight: normal !important;
  opacity: 1 !important;
  text-shadow: none !important;
}

/* Force consistent color for any elements with inline styles */
.ck-content [style],
.ck-content p[style],
.ck-content li[style],
.ck-content li p[style] {
  color: #000000 !important;
}

/* Ensure consistent rendering for text in different contexts */
.ck-content p::first-letter,
.ck-content li::first-letter,
.ck-content li p::first-letter {
  color: #000000 !important;
}

/* Specifically target underlined text to ensure consistent color */
.ck-content u,
.ck-content u *,
.ck-content span u,
.ck-content li u,
.ck-content [style*="text-decoration"] {
  color: #000000 !important;
  text-decoration-color: #000000 !important;
}

/* Target any inline styles that might be overriding our color */
.ck-content [style*="color"],
.ck-content [style*="Color"] {
  color: #000000 !important;
}

/* Preserve color for specific elements that need different colors */
.ck-content a:hover {
  color: #005a30 !important;
}

.ck-content mark,
.ck-content [class*="marker-"],
.ck-content [class*="pen-"] {
  /* Keep highlight colors intact */
  color: inherit !important;
}

.editor-container__editor-wrapper {
  display: flex;
  width: 100%;
}

.editor-container_document-editor {
  border: 1px solid rgba(106, 174, 154, 0.6);
  width: 100%;
  border-radius: 12px;
  /* This overflow property is crucial for dropdowns to be visible */
  overflow: visible !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background-color: rgba(186, 226, 206, 0.5);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  position: relative;
  z-index: 1;
}

/* Ensure all parent/ancestor elements have overflow: visible */
.main-container,
.editor-container_document-editor,
.editor-container__toolbar,
.editor-container__menu-bar {
  overflow: visible !important;
}

.editor-container_document-editor .editor-container__menu-bar {
  display: flex;
  position: relative;
  width: 100%;
  background-color: rgba(146, 200, 170, 0.9);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(106, 174, 154, 0.5);
  z-index: 9100;
  border-radius: 10px 10px 0 0;
}

.editor-container_document-editor .editor-container__toolbar {
  display: flex;
  position: relative;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.15);
  width: 100%;
  background-color: rgba(146, 200, 170, 0.9);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(106, 174, 154, 0.5);
  z-index: 9000;
  border-radius: 8px;
}

.editor-container_document-editor .editor-container__toolbar>.ck.ck-toolbar {
  flex-grow: 1;
  width: 100%;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  border-top: 0;
  border-left: 0;
  border-right: 0;
  background-color: transparent;
}

.editor-container_document-editor .editor-container__menu-bar>.ck.ck-menu-bar {
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  border-top: 0;
  border-left: 0;
  border-right: 0;
  width: 100%;
  background-color: transparent;
  border-radius: 8px;
}

.editor-container_document-editor .editor-container__editor-wrapper {
  position: relative;
  z-index: 1;
  max-height: var(--ckeditor5-preview-height);
  min-height: var(--ckeditor5-preview-height);
  overflow-y: scroll;
  background: rgba(186, 226, 206, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  width: 100%;
  border-top: 1px solid rgba(106, 174, 154, 0.3);
  border-radius: 0 0 10px 10px;
}

.editor-container_document-editor .editor-container__editor {
  margin-top: 0px;
  margin-bottom: 0px;
  height: 100%;
  width: 100%;
  padding: 20px;
  background-color: rgba(186, 226, 206, 0.4);
  border-radius: 0 0 10px 10px;
}

.editor-container_document-editor .editor-container__editor .ck.ck-editor__editable {
  box-sizing: border-box;
  width: 100%;
  min-height: 297mm;
  height: fit-content;
  padding: 20mm 12mm;
  border: 1px solid rgba(106, 174, 154, 0.5);
  background-color: rgba(186, 226, 206, 0.8);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow:
    0 4px 12px rgba(0, 0, 0, 0.12),
    inset 0 1px 1px rgba(255, 255, 255, 0.4);
  flex: 1 1 auto;
  margin-left: 0px;
  margin-right: 0px;
  color: #000000;
  border-radius: 8px;
  position: relative;
}

/* Add a light gradient overlay to enhance glass effect */
.editor-container_document-editor .editor-container__editor .ck.ck-editor__editable::before {
  content: '';
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 30%;
  background: linear-gradient(to bottom,
      rgba(186, 226, 206, 0.5) 0%,
      rgba(186, 226, 206, 0) 100%);
  pointer-events: none;
  border-radius: 6px 6px 0 0;
}

/* Add specific style for the blurred and focused states */
.ck.ck-content.ck-editor__editable {
  background-color: rgba(186, 226, 206, 0.8) !important;
  border-color: rgba(106, 174, 154, 0.5) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border-radius: 8px !important;
}

.ck.ck-content.ck-editor__editable.ck-focused {
  background-color: rgba(166, 213, 186, 0.9) !important;
  border-color: rgba(76, 154, 134, 0.8) !important;
  box-shadow: 0 0 0 3px rgba(76, 154, 134, 0.3) !important;
}

/* Apply consistent styling to toolbar buttons and UI elements */
.ck.ck-button,
.ck.ck-dropdown__button {
  background-color: rgba(166, 213, 186, 0.6) !important;
  border-color: rgba(106, 174, 154, 0.4) !important;
  border-radius: 6px !important;
}

.ck.ck-button:hover,
.ck.ck-dropdown__button:hover {
  background-color: rgba(146, 200, 170, 0.9) !important;
  border-color: rgba(76, 154, 134, 0.7) !important;
}

.ck.ck-button.ck-on {
  background-color: rgba(126, 190, 166, 0.95) !important;
  border-color: rgba(76, 154, 134, 0.8) !important;
}

/* Fix dropdowns and balloon panels - NEW APPROACH */
/* Ensure all dropdown panels appear above everything else */
.ck.ck-balloon-panel.ck-balloon-panel_visible,
.ck.ck-dropdown__panel {
  z-index: 100000 !important;
  background: rgba(166, 213, 186, 0.95) !important;
  border: 1px solid rgba(106, 174, 154, 0.6) !important;
  border-radius: 8px !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
  /* Remove fixed max-height to allow natural sizing */
  overflow-y: auto !important;
  /* Constrain width to prevent full-width expansion */
  width: auto !important;
  min-width: 15rem !important;
  max-width: 15rem !important;
  position: absolute !important;
}

/* Special handling for color picker dropdowns */
.ck.ck-color-ui-dropdown .ck-dropdown__panel,
.ck.ck-color-grid__container,
.ck-fontcolor .ck-dropdown__panel,
.ck-fontbackgroundcolor .ck-dropdown__panel,
.ck.ck-color-picker-dropdown .ck-dropdown__panel {
  min-width: auto !important;
  width: auto !important;
  max-width: none !important;
  background: rgba(166, 213, 186, 0.7) !important;
  /* More transparent background */
  padding: 8px !important;
  border-radius: 8px !important;
}

/* New approach to color grid - focus on making inline styles visible */
.ck.ck-color-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-gap: 4px;
  padding: 8px;
  width: auto;
  max-width: 180px;
  background: transparent;
}

/* Target the button element directly with simplified styling */
.ck.ck-color-grid__tile {
  width: 24px;
  height: 24px;
  min-width: 24px;
  min-height: 24px;
  border: 1px solid rgba(0, 0, 0, 0.2);
  padding: 0;
  margin: 2px;
  position: relative;
  z-index: 1;
  background-color: transparent;
  border-radius: 4px !important;
}

/* Target actual color tile element with inline style */
.ck.ck-color-grid button.ck-color-grid__tile[style*="background-color"] {
  background-color: inherit !important;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 4px !important;
}

/* Ensure all color grid buttons inherit their background color */
.ck.ck-color-grid .ck-button.ck-color-grid__tile {
  background-color: inherit !important;
}

/* Hide SVG icons and spans within color grid tiles */
.ck.ck-color-grid__tile svg,
.ck.ck-color-grid__tile span {
  display: none !important;
}

/* Ensure selected color has visible indicator */
.ck.ck-color-grid__tile.ck-on {
  z-index: 2;
  box-shadow: 0 0 0 2px #fff, 0 0 0 4px rgba(76, 154, 134, 0.8);
}

/* Fix clipping issues by ensuring all parent elements don't clip */
.ck.ck-toolbar .ck-toolbar__items,
.ck.ck-toolbar,
.ck-dropdown {
  overflow: visible !important;
}

/* Ensure dropdown has proper positioning context */
.ck.ck-dropdown {
  position: relative !important;
  display: inline-block !important;
}

/* Update global CSS variables */
:root {
  /* Core text and background colors */
  --ck-color-text: #000000;
  --ck-color-editor-base-text: #000000;
  --ck-color-base-text: #000000;
  --ck-color-base-background: rgba(186, 226, 206, 0.8);
  --ck-color-widget-editable-focus-background: rgba(166, 213, 186, 0.9);
  --ck-color-base-border: rgba(106, 174, 154, 0.5);
  --ck-color-focus-border: rgba(76, 154, 134, 0.8);
  --ck-focus-outer-shadow: 0 0 0 3px rgba(76, 154, 134, 0.3);

  /* Button styling - these are the key variables for toolbar buttons */
  --ck-color-button-default-background: rgba(166, 213, 186, 0.6);
  --ck-color-button-default-hover-background: rgba(146, 200, 170, 0.9);
  --ck-color-button-default-active-background: rgba(126, 190, 166, 0.95);
  --ck-color-button-default-active-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.15);
  --ck-color-button-on-background: rgba(126, 190, 166, 0.95);
  --ck-color-button-on-hover-background: rgba(126, 190, 166, 1);
  --ck-color-button-on-active-background: rgba(106, 174, 154, 0.4);
  --ck-color-button-on-active-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.15);
  --ck-color-button-on-disabled-background: rgba(186, 226, 206, 0.4);

  /* Z-index management */
  --ck-z-default: 1;
  --ck-z-modal: 100000;
  --ck-z-panel: 99999;
  --ck-z-toolbar: 9000;

  /* Dropdown panel styling */
  --ck-color-dropdown-panel-background: rgba(166, 213, 186, 0.95);

  /* CRITICAL: Add these variables for proper button styling */
  --ck-color-base-foreground: #ffffff;
  --ck-color-button-default-hover-background: rgba(146, 200, 170, 0.9);
  --ck-color-button-default-border: rgba(106, 174, 154, 0.4);

  /* Color grid specific variables */
  --ck-color-grid-tile-black: rgb(0, 0, 0);
  --ck-color-grid-tile-dim-grey: rgb(77, 77, 77);
  --ck-color-grid-tile-grey: rgb(153, 153, 153);
  --ck-color-grid-tile-light-grey: rgb(230, 230, 230);
  --ck-color-grid-tile-white: rgb(255, 255, 255);
  --ck-color-grid-tile-red: rgb(255, 94, 94);
  --ck-color-grid-tile-orange: rgb(255, 190, 94);
  --ck-color-grid-tile-yellow: rgb(255, 241, 94);
  --ck-color-grid-tile-light-green: rgb(184, 255, 94);
  --ck-color-grid-tile-green: rgb(94, 255, 143);
  --ck-color-grid-tile-aquamarine: rgb(94, 255, 214);
  --ck-color-grid-tile-light-blue: rgb(94, 207, 255);
  --ck-color-grid-tile-blue: rgb(94, 135, 255);
  --ck-color-grid-tile-purple: rgb(143, 94, 255);

  /* Highlight feature variables */
  --ck-highlight-marker-yellow: rgba(255, 241, 94, 0.5);
  --ck-highlight-marker-green: rgba(94, 255, 143, 0.5);
  --ck-highlight-marker-pink: rgba(255, 94, 207, 0.5);
  --ck-highlight-marker-blue: rgba(94, 207, 255, 0.5);
  --ck-highlight-pen-red: rgba(255, 94, 94, 0.5);
  --ck-highlight-pen-green: rgba(94, 255, 143, 0.7);

  /* Tooltip styling */
  --ck-color-tooltip-text: #005a30;
  --ck-color-tooltip-background: rgba(166, 213, 186, 0.6);
}

/* Style CKEditor tooltips with dark green text */
.ck.ck-tooltip .ck-tooltip__text {
  color: var(--ck-color-tooltip-text) !important;
  font-weight: 500 !important;
  background: var(--ck-color-tooltip-background) !important;
  border: none !important;
  box-shadow: none !important;
  border-radius: 6px !important;
}

/* Target the tooltip arrow */
.ck.ck-tooltip .ck-tooltip__text::after {
  border-color: var(--ck-color-tooltip-background) transparent transparent transparent !important;
}

/* Ensure tooltip text is dark green regardless of its position */
.ck.ck-tooltip.ck-tooltip_s .ck-tooltip__text::after,
.ck.ck-tooltip.ck-tooltip_n .ck-tooltip__text::after,
.ck.ck-tooltip.ck-tooltip_e .ck-tooltip__text::after,
.ck.ck-tooltip.ck-tooltip_w .ck-tooltip__text::after {
  border-color: var(--ck-color-tooltip-text) !important;
}

/* Also target data-cke-tooltip elements which are another way tooltips may be implemented */
[data-cke-tooltip] {
  position: relative;
}

[data-cke-tooltip]::after {
  content: attr(data-cke-tooltip);
  position: absolute;
  display: none;
  background: var(--ck-color-tooltip-background);
  color: var(--ck-color-tooltip-text);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  white-space: nowrap;
  z-index: 100001;
  box-shadow: none;
  border: none;
}

[data-cke-tooltip]:hover::after {
  display: block;
}

/* Ensure the native CKEditor tooltip styling is overridden */
.ck-tooltip,
.ck-tooltip__text {
  color: var(--ck-color-tooltip-text) !important;
}

/* Add more rounded styles for list items and other UI elements */
.ck.ck-list {
  border-radius: 6px !important;
}

.ck.ck-list__item {
  border-radius: 4px !important;
}

.ck.ck-list__item:hover {
  border-radius: 4px !important;
}

.ck-dropdown__panel .ck.ck-list {
  border-radius: 6px !important;
  overflow: hidden !important;
}

/* Add rounded corners to form elements */
.ck.ck-input {
  border-radius: 6px !important;
}

.ck.ck-labeled-field-view {
  border-radius: 6px !important;
}

/* Make toolbar more rounded */
.ck.ck-toolbar {
  border-radius: 8px !important;
}

/* Add rounded corners to the context menus */
.ck.ck-context-menu {
  border-radius: 8px !important;
}

.ck.ck-context-menu__item {
  border-radius: 4px !important;
}

/* Enhanced list styling for better indentation and formatting */
.ck-content ol,
.ck-content ul {
  padding-left: 2em !important;
  margin: 0.5em 0 !important;
}

.ck-content ol ol,
.ck-content ul ul,
.ck-content ol ul,
.ck-content ul ol {
  padding-left: 2em !important;
  margin: 0.5em 0 !important;
}

.ck-content li {
  margin-bottom: 0.5em !important;
  position: relative !important;
}

/* Handle different list styles */
.ck-content ol[type="1"],
.ck-content ol[style*="list-style-type:decimal"] {
  list-style-type: decimal !important;
}

.ck-content ol[type="a"],
.ck-content ol[style*="list-style-type:lower-alpha"],
.ck-content ol[style*="list-style-type:lower-latin"] {
  list-style-type: lower-alpha !important;
}

.ck-content ol[type="A"],
.ck-content ol[style*="list-style-type:upper-alpha"],
.ck-content ol[style*="list-style-type:upper-latin"] {
  list-style-type: upper-alpha !important;
}

.ck-content ol[type="i"],
.ck-content ol[style*="list-style-type:lower-roman"] {
  list-style-type: lower-roman !important;
}

.ck-content ol[type="I"],
.ck-content ol[style*="list-style-type:upper-roman"] {
  list-style-type: upper-roman !important;
}

/* Fix for nested list display */
.ck-content li>ol,
.ck-content li>ul {
  margin-top: 0.5em !important;
  margin-bottom: 0 !important;
}

/* Improve list properties UI in toolbar */
.ck.ck-list-properties {
  padding: 0.5em !important;
}

.ck.ck-list-properties .ck-list-properties__list-style-type-dropdown,
.ck.ck-list-properties .ck-list-properties__list-style-position-dropdown,
.ck.ck-list-properties .ck-list-properties__list-start-index-input {
  margin-bottom: 0.5em !important;
}

.ck.ck-list-properties .ck-list-properties__list-style-type-dropdown .ck-dropdown__panel,
.ck.ck-list-properties .ck-list-properties__list-style-position-dropdown .ck-dropdown__panel {
  max-height: 250px !important;
  overflow-y: auto !important;
}

/* Fix list style buttons in toolbar */
.ck.ck-toolbar .ck-button[class*="list"] {
  position: relative !important;
  z-index: 1 !important;
}

.ck.ck-toolbar .ck-dropdown[class*="list"] {
  position: relative !important;
  z-index: 1 !important;
}

/* Custom list markers and visual improvements */
.ck-content li::marker {
  color: #000000 !important;
  font-weight: bold !important;
}

/* Ensure proper spacing for list items with block elements */
.ck-content li p {
  margin: 0 !important;
  display: inline-block !important;
  width: 100% !important;
  color: #000000 !important;
  font-weight: normal !important;
  opacity: 1 !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
}

/* Fix for lists with multiple paragraphs */
.ck-content li p+p {
  margin-top: 0.5em !important;
  display: block !important;
  color: #000000 !important;
  font-weight: normal !important;
  opacity: 1 !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
}

/* Ensure proper alignment of list items */
.ck-content ol,
.ck-content ul {
  list-style-position: outside !important;
  color: #000000 !important;
}

/* Fix for nested lists with different list styles */
.ck-content ol>li::marker {
  font-weight: bold !important;
}

.ck-content ul>li::marker {
  font-weight: normal !important;
}

/* Add rounded corners to dialog/modal windows */
.ck.ck-dialog {
  border-radius: 10px !important;
}

.ck.ck-dialog__footer {
  border-radius: 0 0 10px 10px !important;
}

.ck.ck-dialog__header {
  border-radius: 10px 10px 0 0 !important;
}

/* Ensure the balloon toolbar has rounded corners */
.ck.ck-balloon-panel.ck-balloon-panel_with-arrow {
  border-radius: 8px !important;
}

/* Style source editing area if available */
.ck.ck-source-editing-area textarea {
  border-radius: 6px !important;
}

/* Override any potential CKEditor internal styles that might affect transparency */
.ck-content [class^="ck-"],
.ck-content [class*=" ck-"] {
  opacity: 1 !important;
  color: #000000 !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
  text-rendering: optimizeLegibility !important;
}
</style>
