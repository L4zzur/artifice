<script lang="ts">
  import { FileText, Upload, X } from "lucide-svelte";

  type InputMode = "text" | "file";

  interface Props {
    inputMode: InputMode;
    inputData: string;
    uploadedFile: File | null;

    onModeChange: (mode: InputMode) => void;
    onFileSelect: (file: File | null) => void;

    textLabel: string;
    textPlaceholder: string;
    textRows: number;
    maxFileSizeMB: number;
  }

  let {
    inputMode = $bindable(),
    inputData = $bindable(),
    uploadedFile = $bindable(),
    onModeChange,
    onFileSelect,
    textLabel,
    textPlaceholder,
    textRows,
    maxFileSizeMB,
  }: Props = $props();

  let isDragging = $state(false);
  let fileError = $state<string | null>(null);

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
    fileError = null;

    if (!selectedFile) {
      return;
    }

    if (selectedFile.size > maxFileSizeMB * 1024 * 1024) {
      fileError = `File size must be less than ${maxFileSizeMB}MB`;
      return;
    }

    uploadedFile = selectedFile;
    onFileSelect(selectedFile);
  }

  function removeFile() {
    uploadedFile = null;
    onFileSelect(null);
    fileError = null;
  }
</script>

<section class="input-panel">
  <div class="header">
    <h2>Input Data</h2>

    <div class="mode-toggle">
      <button
        class="mode-button {inputMode === 'text' ? 'active' : ''}"
        onclick={() => onModeChange("text")}
        aria-label="Switch to text input mode"
      >
        Text
      </button>
      <button
        class="mode-button {inputMode === 'file' ? 'active' : ''}"
        onclick={() => onModeChange("file")}
        aria-label="Switch to file upload mode"
      >
        File
      </button>
    </div>
  </div>

  <div class="input">
    {#if inputMode === "text"}
      <div class="input-group">
        <label for="input-data" class="input-label">{textLabel}</label>

        <textarea
          id="input-data"
          bind:value={inputData}
          placeholder={textPlaceholder}
          class="input-data"
          rows={textRows}
          spellcheck="false"
        ></textarea>

        {#if inputData.length > 0}
          <p class="input-length">
            {inputData.length} character{inputData.length === 1 ? "" : "s"}
          </p>
        {/if}
      </div>
    {:else}
      <div class="file-section">
        {#if !uploadedFile}
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
              <p class="dropzone-hint">Maximum file size: {maxFileSizeMB}MB</p>
            </label>
          </div>
        {:else}
          <div class="file-preview">
            <div class="file-icon">
              <FileText size={32} />
            </div>
            <div class="file-info">
              <p class="file-name">{uploadedFile.name}</p>
              <p class="file-size">
                {(uploadedFile.size / 1024 / 1024).toFixed(2)}MB
              </p>
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
        {#if fileError}
          <div class="error-box">{fileError}</div>
        {/if}
      </div>
    {/if}
  </div>
</section>

<style>
  .input-panel {
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-large);
    padding: 1.5rem;
    display: flex;
    height: 240px;
    flex-direction: column;
    gap: 0.5rem;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.2rem;
  }

  h2 {
    font-size: 1.125rem;
    font-weight: 600;
    margin: 0;
    color: var(--md-sys-color-on-surface);
  }

  .mode-toggle {
    display: flex;
    gap: 0.25rem;
    padding: 0.25rem;
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    width: fit-content;
  }

  .mode-button {
    padding: 0.375rem 1rem;
    background: none;
    border: none;
    border-radius: var(--md-sys-shape-corner-small);
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface-variant);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .mode-button:hover {
    background: var(--md-sys-color-surface-container-high);
    color: var(--md-sys-color-on-surface);
  }

  .mode-button.active {
    background: var(--md-sys-color-primary);
    color: var(--md-sys-color-on-primary);
  }

  .input {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
  }

  .input-group,
  .file-section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    flex: 1;
    min-height: 0;
  }

  .input-label {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface-variant);
    flex-shrink: 0;
  }

  .input-data {
    width: 100%;
    padding: 1rem;
    background: var(--md-sys-color-surface-container-high);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    font-family: "Courier New", Consolas, Monaco, monospace;
    font-size: 0.9375rem;
    color: var(--md-sys-color-on-surface);
    resize: none;
    transition: border-color 0.2s ease;
    flex: 1;
    min-height: 0;
  }

  .input-data:focus {
    outline: none;
    border-color: var(--md-sys-color-primary);
  }

  .input-data::placeholder {
    color: var(--md-sys-color-on-surface-variant);
    opacity: 0.5;
  }

  .input-length {
    margin: 0;
    font-size: 0.75rem;
    color: var(--md-sys-color-on-surface-variant);
    opacity: 0.7;
  }

  .dropzone {
    position: relative;
    border: 2px dashed var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    padding: 1.5rem 1rem;
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
    flex-shrink: 0;
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
