<script lang="ts">
  import { scanQRCode } from "$lib/api/qr";
  import Button from "$lib/components/ui/Button.svelte";
  import ImageUpload from "$lib/components/ui/ImageUpload.svelte";
  import PageHeader from "$lib/components/ui/PageHeader.svelte";
  import Spinner from "$lib/components/ui/Spinner.svelte";
  import Toast from "$lib/components/ui/Toast.svelte";
  import {
    CircleCheckBig,
    CircleX,
    Copy,
    ScanBarcode,
    ScanIcon,
    ScanQrCode,
  } from "lucide-svelte";

  let imagePreview = $state<string | null>(null);
  let imageBase64 = $state<string | null>(null);

  let isScanning = $state(false);
  let error = $state<string | null>(null);
  let scannedCodes = $state<Array<string>>([]);
  let hasScanned = $state(false);

  let toastMessage = $state<string | null>(null);
  let toastTimeout: ReturnType<typeof setTimeout> | null = null;

  function showToast(message: string, duration: number = 4000) {
    toastMessage = message;

    if (toastTimeout) {
      clearTimeout(toastTimeout);
    }

    toastTimeout = setTimeout(() => {
      toastMessage = null;
    }, duration);
  }

  function handleImageUpload(imagebase64: string) {
    imagePreview = imagebase64;
    imageBase64 = imagebase64;
    error = null;
    scannedCodes = [];
    hasScanned = false;
  }

  function handleImageRemove() {
    imagePreview = null;
    imageBase64 = null;
    error = null;
    scannedCodes = [];
    hasScanned = false;
  }

  async function handleScan() {
    if (!imageBase64) {
      error = "Please upload an image first";
      return;
    }

    isScanning = true;
    error = null;
    scannedCodes = [];

    try {
      const result = await scanQRCode({
        image: imageBase64,
        auto_resize: true,
      });

      scannedCodes = result.codes || [];
      hasScanned = true;

      if (scannedCodes.length == 0) {
        error = "No QR codes found in the image";
      } else {
        showToast(
          `Successfully found ${scannedCodes.length} QR code${scannedCodes.length > 1 ? "s" : ""}`,
        );
      }
    } catch (e) {
      if (e instanceof Error) {
        error = e.message;
      } else {
        error = "An unexpected error occurred";
      }
      console.error("QR scan error:", e);
    } finally {
      isScanning = false;
    }
  }

  async function copyToClipboard(text: string) {
    try {
      await navigator.clipboard.writeText(text);
      showToast("Copied to clipboard");
    } catch (e) {
      showToast("Failed to copy to clipboard");
    }
  }

  function isUrl(text: string): boolean {
    try {
      new URL(text);
      return true;
    } catch (e) {
      return false;
    }
  }
</script>

<div class="page-container">
  <PageHeader
    title="QR Code Scanner"
    description="Scan QR code to get information"
    backLink={{ href: "/qr", label: "Back to QR Tools" }}
  >
    {#snippet icon()}
      <ScanQrCode size={48} strokeWidth={1.7} />
    {/snippet}
  </PageHeader>

  {#if error}
    <div class="error-message">
      <CircleX size={18} />
      {error}
    </div>
  {/if}

  <div class="scanner-layout">
    <section class="upload-panel">
      <h2>Settings</h2>

      <ImageUpload
        preview={imagePreview}
        label="Upload image containing QR code"
        hint="PNG, JPG, WEBP up to 5MB"
        maxSize={5}
        onUpload={handleImageUpload}
        onRemove={handleImageRemove}
        onError={(msg) => (error = msg)}
      />

      <Button
        fullWidth
        disabled={!imageBase64 || isScanning}
        onclick={handleScan}
      >
        {#if isScanning}
          <Spinner size={20} />
        {:else}
          <ScanIcon size={20} strokeWidth={2} />
          <span>Scan QR Code</span>
        {/if}
      </Button>
    </section>

    <section class="result-panel">
      <h2>Results</h2>

      {#if isScanning}
        <Spinner message="Scanning QR code..." />
      {:else if hasScanned && scannedCodes.length > 0}
        <div class="results-container">
          <div class="success-banner">
            <CircleCheckBig size={24} strokeWidth={2} />
            Successfully found {scannedCodes.length} QR code{scannedCodes.length >
            1
              ? "s"
              : ""}
          </div>

          <div class="codes-list">
            {#each scannedCodes as code, i}
              <div class="code-card">
                <div class="code-header">
                  <span class="code-index">QR №{i + 1}</span>
                  <Button
                    variant="secondary"
                    onclick={() => copyToClipboard(code)}
                  >
                    <Copy size={16} strokeWidth={2} />
                    Copy
                  </Button>
                </div>

                <div class="code-content">
                  {#if isUrl(code)}
                    <a
                      href={code}
                      target="_blank"
                      rel="noopener noreferrer"
                      class="code-link"
                    >
                      {code}
                    </a>
                  {:else}
                    <p class="code-text">{code}</p>
                  {/if}
                </div>
              </div>
            {/each}
          </div>
        </div>
      {:else if hasScanned && scannedCodes.length === 0}
        <div class="placeholder">
          <CircleX size={64} strokeWidth={2} />
          <p>No QR codes found in the image</p>
          <small
            >Try uploading a clearer image or ensure the QR code is visible</small
          >
        </div>
      {:else}
        <div class="placeholder">
          <ScanBarcode size={64} strokeWidth={2} />
          <p>Upload and image to scan</p>
          <small>Supports multiple QR codes in a single image</small>
        </div>
      {/if}
    </section>
  </div>

  <Toast message={toastMessage} onClose={() => (toastMessage = null)} />
</div>

<style>
  .page-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
  }

  .scanner-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }

  @media (max-width: 900px) {
    .scanner-layout {
      grid-template-columns: 1fr;
    }
  }

  .upload-panel,
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

  .error-message {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1rem;
    padding: 0.75rem;
    background: var(--md-sys-color-error-container);
    color: var(--md-sys-color-on-error-container);
    border-radius: var(--md-sys-shape-corner-medium);
    font-size: 0.9rem;
  }

  .placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    border: 2px dashed var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-large);
    color: var(--md-sys-color-on-surface-variant);
    text-align: center;
    padding: 2rem;
  }

  .placeholder p {
    margin: 1rem 0 0.5rem 0;
    font-size: 1.125rem;
    font-weight: 500;
  }

  .placeholder small {
    opacity: 0.7;
  }

  .results-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .success-banner {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: var(--md-sys-color-tertiary-container);
    color: var(--md-sys-color-on-tertiary-container);
    border-radius: var(--md-sys-shape-corner-small);
    font-weight: 500;
  }

  .codes-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .code-card {
    padding: 0.9rem 1.5rem 1.5rem 1.5rem;
    background: var(--md-sys-color-surface-container-high);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
  }

  .code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .code-index {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--md-sys-color-on-surface-variant);
    text-transform: uppercase;
  }

  .code-link {
    font-weight: 500;
    text-decoration: none;
    color: var(--md-sys-color-primary);
  }

  .code-link:hover {
    text-decoration: underline;
  }

  .code-text {
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface);
  }
</style>
