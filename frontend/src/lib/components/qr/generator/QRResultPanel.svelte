<script lang="ts">
  import { Check, Copy, Download, QrCode } from "lucide-svelte";
  import Button from "$lib/components/ui/Button.svelte";

  interface Props {
    generatedQR: string | null;
    isLoading: boolean;
    onDownload: () => void;
  }

  let { generatedQR, isLoading, onDownload }: Props = $props();

  let copied = $state(false);

  async function copyToClipboard() {
    if (!generatedQR) return;

    try {
      const response = await fetch(generatedQR);
      const blob = await response.blob();

      await navigator.clipboard.write([
        new ClipboardItem({ "image/png": blob }),
      ]);

      copied = true;
      setTimeout(() => (copied = false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  }
</script>

<section class="result-panel">
  <h2>Result</h2>

  {#if isLoading}
    <div class="loading-state">
      <div class="spinner"></div>
      <p>Generating QR code...</p>
    </div>
  {:else if generatedQR}
    <div class="qr-result">
      <div class="qr-preview">
        <img src={generatedQR} alt="Generated QR Code" />
      </div>

      <div class="button-group">
        <Button onclick={onDownload} fullWidth>
          <Download size={18} strokeWidth={2} />
          Download QR Code
        </Button>

        <Button onclick={copyToClipboard} variant="secondary" fullWidth>
          {#if copied}
            <Check size={18} strokeWidth={2} />
            Copied!
          {:else}
            <Copy size={18} strokeWidth={2} />
            Copy QR Code
          {/if}
        </Button>
      </div>
    </div>
  {:else}
    <div class="placeholder">
      <QrCode size={64} strokeWidth={1.7} />
      <p>Your QR code will appear here</p>
    </div>
  {/if}
</section>

<style>
  .result-panel {
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-large);
    padding: 2rem;
  }

  h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 1.5rem 0;
    color: var(--md-sys-color-on-surface);
  }

  .qr-result {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .qr-preview {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    background: var(--md-sys-color-surface-container-highest);
    min-height: 400px;
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
  }

  .qr-preview img {
    max-width: 100%;
    height: auto;
    display: block;
    border-radius: var(--md-sys-shape-corner-small);
  }

  .placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    border: 2px dashed var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    color: var(--md-sys-color-on-surface-variant);
  }

  .placeholder p {
    margin-top: 1rem;
  }

  .button-group {
    display: flex;
    gap: 0.75rem;
  }
</style>
