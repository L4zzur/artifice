<script lang="ts">
  import Panel from "$lib/components/ui/Panel.svelte";
  import { FileText, Upload, X } from "lucide-svelte";
  interface Props {
    file: File | null;
    onFileSelect: (file: File | null) => void;
    maxSizeMB?: number;
  }

  let { file, onFileSelect, maxSizeMB = 15 }: Props = $props();

  let isDragging = $state(false);
  let error = $state<string | null>(null);

  function handleFileInput(event: Event) {
    const target = event.target as HTMLInputElement;
    const selectedFile = target.files?.[0];
    processFile(selectedFile);
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    isDragging = false;

    const droppedFile = event.dataTransfer?.files[0];
    processFile(droppedFile);
  }

  function handleDragOver(event: DragEvent) {
    event.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  function processFile(selectedFile: File | undefined) {
    error = null;

    if (!selectedFile) {
      return;
    }

    if (selectedFile.size > maxSizeMB * 1024 * 1024) {
      error = `File size must be less than ${maxSizeMB}MB`;
      return;
    }

    file = selectedFile;
    onFileSelect(selectedFile);
  }

  function removeFile() {
    file = null;
    onFileSelect(null);
    error = null;
  }
</script>

<Panel title="Upload File">
  {#if !file}
    <div
      class="dropzone {isDragging ? 'dragging' : ''}"
      role="button"
      tabindex="0"
      ondrop={handleDrop}
      ondragover={handleDragOver}
      ondragleave={handleDragLeave}
    >
      <input
        type="file"
        id="file-input"
        class="file-input"
        onchange={handleFileInput}
        aria-label="Upload file"
      />

      <label for="file-input" class="dropzone-label">
        <Upload size={32} />
        <p class="dropzone-title">
          Drop file here or <span class="link">browse</span>
        </p>
        <p class="dropzone-hint">Maximum file size: {maxSizeMB}MB</p>
      </label>
    </div>
  {:else}
    <div class="file-preview">
      <div class="file-icon">
        <FileText size={32} />
      </div>
      <div class="file-info">
        <p class="file-name">{file.name}</p>
        <p class="file-size">{(file.size / 1024 / 1024).toFixed(2)}MB}</p>
      </div>
      <button
        class="remove-button"
        onclick={removeFile}
        aria-label="Remove file"
      >
        <X size={18} />
      </button>
    </div>
  {/if}

  {#if error}
    <div class="error-box">{error}</div>
  {/if}
</Panel>

<style>
  .dropzone {
    position: relative;
    border: 2px dashed var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    padding: 2rem 1rem;
    text-align: center;
    transition: all 0.2s ease;
    background: var(--md-sys-color-surface-container-high);
  }

  .dropzone:hover,
  .dropzone.dragging {
    border-color: var(--md-sys-color-primary);
    background: rgba(176, 196, 222, 0.05);
  }

  .file-input {
    position: absolute;
    width: 1px;
    height: 1px;
    opacity: 0;
    overflow: hidden;
  }

  .dropzone-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    cursor: pointer;
    color: var(--md-sys-color-on-surface-variant);
  }

  .dropzone-title {
    margin: 0;
    font-size: 0.9375rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface);
  }

  .link {
    color: var(--md-sys-color-primary);
    text-decoration: underline;
  }

  .dropzone-hint {
    margin: 0;
    font-size: 0.8125rem;
    color: var(--md-sys-color-on-surface-variant);
  }

  .file-preview {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: var(--md-sys-color-surface-container-high);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
  }

  .file-icon {
    padding: 0.5rem;
    background: var(--md-sys-color-primary-container);
    color: var(--md-sys-color-on-primary-container);
    border-radius: var(--md-sys-shape-corner-small);
  }

  .file-info {
    flex: 1;
    min-width: 0;
  }

  .file-name {
    margin: 0 0 0.25rem 0;
    font-size: 0.9375rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .file-size {
    margin: 0;
    font-size: 0.8125rem;
    color: var(--md-sys-color-on-surface-variant);
  }

  .remove-button {
    padding: 0.5rem;
    background: none;
    border: none;
    color: var(--md-sys-color-error);
    border-radius: var(--md-sys-shape-corner-small);
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .remove-button:hover {
    background: var(--md-sys-color-error-container);
  }

  .error-box {
    margin-top: 0.75rem;
    padding: 0.75rem;
    background: var(--md-sys-color-error-container);
    color: var(--md-sys-color-on-error-container);
    border-radius: var(--md-sys-shape-corner-small);
    font-size: 0.875rem;
  }
</style>
