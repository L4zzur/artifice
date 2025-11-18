<script lang="ts">
  import { ImageIcon } from "lucide-svelte";
  import Button from "./Button.svelte";

  interface Props {
    preview: string | null;
    label?: string;
    hint?: string;
    maxSize?: number; // in MB
    accept?: string;
    onUpload: (base64: string) => void;
    onRemove: () => void;
    onError?: (message: string) => void;
  }

  let {
    preview = $bindable(),
    label = "Upload image",
    hint = "PNG, JPG, WEBP up to 3MB",
    maxSize = 3,
    accept = "image/*",
    onUpload,
    onRemove,
    onError,
  }: Props = $props();

  const id = "image-upload-" + Math.random().toString(36).slice(2);

  function handleFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (!file) return;

    if (
      !file.type.startsWith("image/") ||
      (!file.type.endsWith("jpeg") &&
        !file.type.endsWith("png") &&
        !file.type.endsWith("webp"))
    ) {
      onError?.("Please select an image file (only JPEG, PNG, WebP)");
      return;
    }

    if (file.size > maxSize * 1024 * 1024) {
      onError?.(`Image file size should be less than ${maxSize} MB`);
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
  <div class="upload-area">
    <input
      type="file"
      {accept}
      onchange={handleFileChange}
      {id}
      style="display: none;"
    />
    <label for={id} class="upload-label">
      <ImageIcon size={32} />
      <span>{label}</span>
      <small>{hint}</small>
    </label>
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
    margin: 0.5rem 0 0.75rem 0;
  }

  .upload-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 2rem;
    border: 2px dashed var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    cursor: pointer;
    transition: all var(--md-sys-color-primary);
    color: var(--md-sys-color-on-surface-variant);
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
    gap: 0.75rem;
    margin: 0.5rem 0 0.5rem 0;
  }

  .uploaded-preview img {
    max-width: 150px;
    max-height: 150px;
    border-radius: var(--md-sys-shape-corner-small);
    border: 1px solid var(--md-sys-color-outline-variant);
    display: block;
  }
</style>
