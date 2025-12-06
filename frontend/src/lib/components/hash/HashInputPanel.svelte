<script lang="ts">
  import { FileText, Upload, X } from "lucide-svelte";
  import Panel from "$lib/components/ui/Panel.svelte";
  import ModeToggle from "$lib/components/ui/ModeToggle.svelte";
  import FileUpload from "$lib/components/ui/FileUpload.svelte";

  type InputMode = "text" | "file";

  interface Props {
    inputMode: InputMode;
    inputData: string;
    uploadedFile: File | null;

    onModeChange: (mode: InputMode) => void;
    onFileSelect: (file: File | null) => void;
    onError: (message: string) => void;

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
    onError,
    textLabel,
    textPlaceholder,
    textRows,
    maxFileSizeMB,
  }: Props = $props();

  const modeOptions = [
    { value: "text" as const, label: "Text" },
    { value: "file" as const, label: "File" },
  ];
</script>

<Panel height="240px">
  {#snippet header()}
    <div class="header">
      <h2>Input Data</h2>
      <ModeToggle
        options={modeOptions}
        selected={inputMode}
        onChange={onModeChange}
      />
    </div>
  {/snippet}

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
        <FileUpload
          bind:file={uploadedFile}
          {onFileSelect}
          {onError}
          maxSizeMB={maxFileSizeMB}
          label="Drop file here or browse"
          hint="Maximum file size: {maxFileSizeMB}MB"
        />
      </div>
    {/if}
  </div>
</Panel>

<style>
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
</style>
