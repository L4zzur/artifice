<script lang="ts">
  import { FileText, Upload, X } from "lucide-svelte";

  interface Props {
    file: File | null;
    accept?: string;
    maxSizeMB: number;

    label: string;
    hint: string;
    showPreview?: boolean;

    onFileSelect: (file: File | null) => void;
    onError: (message: string) => void;
  }

  let {
    file = $bindable(),
    accept = "*/*",
    maxSizeMB,
    label,
    hint,
    showPreview = true,
    onFileSelect,
    onError,
  }: Props = $props();

  let isDragging = $state(false);

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
    if (!selectedFile) {
      return;
    }

    if (accept !== "*/*") {
      const acceptedTypes = accept.split(",").map((type) => type.trim());
      const fileType = selectedFile.type;
      const fileExtension = `.${selectedFile.name.split(".").pop()}`;

      const isValidType = acceptedTypes.some(
        (type) =>
          type === fileType ||
          type === fileExtension ||
          (type.endsWith("/*") && fileType.startsWith(type.replace("/*", ""))),
      );

      if (!isValidType) {
        onError?.(`Invalid file type. Accepted: ${accept}`);
        return;
      }
    }

    console.log("📏 Checking file size", {
      size: selectedFile.size,
      maxSize: maxSizeMB * 1024 * 1024,
      isTooBig: selectedFile.size > maxSizeMB * 1024 * 1024,
    });

    if (selectedFile.size > maxSizeMB * 1024 * 1024) {
      onError?.(`File size must be less than ${maxSizeMB}MB`);
      return;
    }

    file = selectedFile;
    onFileSelect(selectedFile);
  }

  function removeFile() {
    file = null;
    onFileSelect(null);
  }
</script>

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
      id="file-upload-input"
      class="file-input"
      {accept}
      onchange={handleFileInput}
      aria-label="Upload file"
    />

    <label for="file-upload-input" class="dropzone-label">
      <Upload size={32} />
      <p class="dropzone-title">
        {label}
      </p>
      {#if hint}
        <p class="dropzone-hint">{hint}</p>
      {/if}
    </label>
  </div>
{:else if showPreview}
  <div class="file-preview">
    <div class="file-icon">
      <FileText size={32} />
    </div>
    <div class="file-info">
      <p class="file-name">{file.name}</p>
      <p class="file-size">{(file.size / 1024 / 1024).toFixed(2)}MB</p>
    </div>
    <button class="remove-button" onclick={removeFile} aria-label="Remove file">
      <X size={18} />
    </button>
  </div>
{/if}

<style>
  .dropzone {
    position: relative;
    border: 2px dashed var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    padding: 2rem 1rem;
    text-align: center;
    transition: all 0.2s ease;
    background: var(--md-sys-color-surface-container-high);
    flex: 1;
    min-height: 0;
    display: flex;
    align-items: center;
    justify-content: center;
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
    flex-shrink: 0;
  }

  .file-icon {
    padding: 0.5rem;
    background: var(--md-sys-color-primary-container);
    color: var(--md-sys-color-on-primary-container);
    border-radius: var(--md-sys-shape-corner-small);
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
</style>
