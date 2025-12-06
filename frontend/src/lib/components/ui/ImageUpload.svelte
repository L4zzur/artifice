<script lang="ts">
  import { ImageIcon } from "lucide-svelte";
  import Button from "./Button.svelte";
  import FileUpload from "./FileUpload.svelte";

  interface Props {
    preview: string | null;
    label?: string;
    hint?: string;
    maxSizeMB?: number;
    accept?: string;
    onUpload: (base64: string) => void;
    onRemove: () => void;
    onError?: (message: string) => void;
  }

  let {
    preview = $bindable(),
    label = "Upload image",
    hint = "PNG, JPG, WEBP up to 3MB",
    maxSizeMB = 3,
    accept = "image/*",
    onUpload,
    onRemove,
    onError,
  }: Props = $props();

  const id = "image-upload-" + Math.random().toString(36).slice(2);
  let imageFile = $state<File | null>(null);

  function handleFileSelect(file: File | null) {
    if (!file) {
      imageFile = null;
      preview = null;
      return;
    }

    if (
      !file.type.startsWith("image/") ||
      (!file.type.endsWith("jpeg") &&
        !file.type.endsWith("png") &&
        !file.type.endsWith("webp"))
    ) {
      onError?.("Please select an image file (only JPEG, PNG, WebP)");
      return;
    }

    if (file.size > maxSizeMB * 1024 * 1024) {
      onError?.(`Image file size should be less than ${maxSizeMB} MB`);
      return;
    }

    const reader = new FileReader();

    reader.onload = (e) => {
      const result = e.target?.result as string;
      onUpload(result);
    };

    reader.onerror = () => {
      onError?.("Failed to read image file");
    };

    reader.readAsDataURL(file);
  }
</script>

{#if !preview}
  <div class="upload-container">
    <FileUpload
      bind:file={imageFile}
      onFileSelect={handleFileSelect}
      accept="image/jpeg,image/png,image/webp"
      {maxSizeMB}
      {label}
      {hint}
      showPreview={false}
    />
  </div>
{:else}
  <div class="uploaded-preview">
    <img src={preview} alt="Preview" />

    <Button variant="error" onclick={onRemove}>
      <ImageIcon size={18} />
      <span>Remove</span>
    </Button>
  </div>
{/if}

<style>
  .upload-area {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .upload-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 1.5rem;
    border: 2px dashed var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    cursor: pointer;
    transition: all var(--md-sys-color-primary);
    color: var(--md-sys-color-on-surface-variant);
    flex: 1;
    min-height: 0;
  }

  .upload-label:hover {
    border-color: var(--md-sys-color-primary);
    background: var(--md-sys-color-surface-container-high);
  }

  .upload-label small {
    font-size: 0.85rem;
    opacity: 0.7;
  }

  .uploaded-preview {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    flex: 1;
    justify-content: center;
  }

  .uploaded-preview img {
    max-width: 100%;
    max-height: 200px;
    width: auto;
    height: auto;
    border-radius: var(--md-sys-shape-corner-small);
    border: 1px solid var(--md-sys-color-outline-variant);
    display: block;
  }
</style>
