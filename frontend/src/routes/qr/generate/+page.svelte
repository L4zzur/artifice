<script lang="ts">
  import { CircleX, ImageIcon, QrCode } from "lucide-svelte";
  import {
    generateQRCode,
    type ColorMaskType,
    type ErrorCorrectionLevel,
    type EyeDrawerType,
    type ModuleDrawerType,
    type QRCodeRequest,
  } from "$lib/api/qr";
  import Toast from "$lib/components/ui/Toast.svelte";
  import ImageUpload from "$lib/components/ui/ImageUpload.svelte";
  import FormGroup from "$lib/components/ui/FormGroup.svelte";
  import ModeToggle from "$lib/components/qr/generator/ModeToggle.svelte";
  import QRBasicSettings from "$lib/components/qr/generator/QRBasicSettings.svelte";
  import QRModuleSettings from "$lib/components/qr/generator/QRModuleSettings.svelte";
  import QREyeSettings from "$lib/components/qr/generator/QREyeSettings.svelte";
  import QRColorMaskSettings from "$lib/components/qr/generator/QRColorMaskSettings.svelte";
  import SettingsSection from "$lib/components/ui/SettingsSection.svelte";
  import QRResultPanel from "$lib/components/qr/generator/QRResultPanel.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import PageHeader from "$lib/components/ui/PageHeader.svelte";

  let qrData = $state("https://example.com");
  let errorCorrection = $state<ErrorCorrectionLevel>("M");
  let finalSize = $state<number>(300);

  let useStyledImage = $state(false);

  let fillColor = $state("#000000");
  let backColor = $state("#ffffff");

  // Module Drawer
  let moduleDrawerType = $state<ModuleDrawerType>("square");
  let moduleDrawerSizeRatio = $state<number>(1.0);
  let moduleDrawerRadiusRatio = $state<number>(0.0);

  // Eye Drawer
  let eyeDrawerType = $state<EyeDrawerType>("square");
  let eyeDrawerRadiusRatio = $state<number>(0.5);

  // Color Mask
  let colorMaskType = $state<ColorMaskType>("solid");
  let colorMaskFrontColor = $state("#000000");
  let colorMaskBackColor = $state("#ffffff");
  let colorMaskCenterColor = $state("#ff0000");
  let colorMaskEdgeColor = $state("#0000ff");
  let colorMaskLeftColor = $state("#ff0000");
  let colorMaskRightColor = $state("#0000ff");
  let colorMaskTopColor = $state("#ff0000");
  let colorMaskBottomColor = $state("#0000ff");

  let colorMaskImageBase64 = $state<string | null>(null);
  let colorMaskImagePreview = $state<string | null>(null);

  // Logo
  let embeddedImageBase64 = $state<string | null>(null);
  let embeddedImagePreview = $state<string | null>(null);

  let generatedQR = $state<string | null>(null);
  let isLoading = $state(false);
  let error = $state<string | null>(null);

  let activeTab = $state<"basic" | "advanced">("basic");

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

  function handleLogoUpload(imagebase64: string) {
    embeddedImageBase64 = imagebase64;
    embeddedImagePreview = imagebase64;

    if (!useStyledImage || errorCorrection !== "H") {
      if (!useStyledImage) {
        showToast(
          "ℹ️ Switched to Advanced mode with High (30%) error correction for logo embedding",
        );
        useStyledImage = true;
        activeTab = "advanced";
      } else if (errorCorrection !== "H") {
        showToast(
          "ℹ️ Error correction set to High (30%) for optimal logo quality",
        );
      }

      errorCorrection = "H";
    }
  }

  function removeLogo() {
    embeddedImageBase64 = null;
    embeddedImagePreview = null;
  }

  function handleColorMaskImageUpload(imagebase64: string) {
    colorMaskImageBase64 = imagebase64;
    colorMaskImagePreview = imagebase64;

    showToast(
      "ℹ️ Pattern image loaded. It will be used as QR code fill texture",
    );
  }

  function removeColorMaskImage() {
    colorMaskImageBase64 = null;
    colorMaskImagePreview = null;
  }

  const adjustBackgroundColor = (color: string): string => {
    if (color.toLowerCase() === "#000000" || color.toLowerCase() === "#000") {
      showToast(
        "ℹ️ Background color adjusted to #010101 for better QR code visibility",
      );
      return "#010101";
    }
    return color;
  };

  async function handleGenerate() {
    if (!qrData.trim()) {
      error = "Please enter data to encode";
      return;
    }

    isLoading = true;
    error = null;
    generatedQR = null;

    try {
      const request: QRCodeRequest = {
        data: qrData,
        error_correction: errorCorrection,
        final_size: finalSize,
        use_styled_image: useStyledImage,
      };

      if (!useStyledImage) {
        request.fill_color = fillColor;
        request.back_color = backColor;
      }

      if (useStyledImage) {
        request.module_drawer = {
          type: moduleDrawerType,
        };

        if (moduleDrawerType === "rounded") {
          request.module_drawer.radius_ratio = moduleDrawerRadiusRatio;
        }

        if (moduleDrawerType === "gapped_square") {
          request.module_drawer.radius_ratio = moduleDrawerRadiusRatio;
        }

        request.eye_drawer = {
          type: eyeDrawerType,
        };

        if (eyeDrawerType === "rounded") {
          request.eye_drawer.radius_ratio = eyeDrawerRadiusRatio;
        }

        request.color_mask = {
          type: colorMaskType,
        };

        switch (colorMaskType) {
          case "solid":
            request.color_mask.front_color = colorMaskFrontColor;
            request.color_mask.back_color =
              adjustBackgroundColor(colorMaskBackColor);
            break;
          case "radial_gradient":
          case "square_gradient":
            request.color_mask.center_color = colorMaskCenterColor;
            request.color_mask.edge_color = colorMaskEdgeColor;
            request.color_mask.back_color =
              adjustBackgroundColor(colorMaskBackColor);
            break;
          case "horizontal_gradient":
            request.color_mask.left_color = colorMaskLeftColor;
            request.color_mask.right_color = colorMaskRightColor;
            request.color_mask.back_color =
              adjustBackgroundColor(colorMaskBackColor);
            break;
          case "vertical_gradient":
            request.color_mask.top_color = colorMaskTopColor;
            request.color_mask.bottom_color = colorMaskBottomColor;
            request.color_mask.back_color =
              adjustBackgroundColor(colorMaskBackColor);
            break;
          case "image":
            if (colorMaskImageBase64) {
              request.color_mask.color_mask_image = colorMaskImageBase64;
              request.color_mask.back_color =
                adjustBackgroundColor(colorMaskBackColor);
            } else {
              error = "Please upload a pattern image for Image Pattern mode";
              isLoading = false;
              return;
            }
            break;
        }
      }

      if (embeddedImageBase64) {
        request.embedded_image = embeddedImageBase64;
      }

      const response = await generateQRCode(request);

      if (response.format === "svg") {
        generatedQR = `data:image/svg+xml;base64,${btoa(response.image)}`;
      } else {
        generatedQR = `data:image/png;base64,${response.image}`;
      }
    } catch (e) {
      if (e instanceof Error) {
        error = e.message;
      } else {
        error = "An unexpected error occurred";
      }
      console.error("QR generation error:", e);
    } finally {
      isLoading = false;
    }
  }

  function downloadQR() {
    if (!generatedQR) return;

    const link = document.createElement("a");
    link.href = generatedQR;
    link.download = `qrcode-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
</script>

<div class="page-container">
  <PageHeader
    title="QR Code Generator"
    description="Create customizable QR codes with image support"
    backLink={{ href: "/qr", label: "Back to QR Tools" }}
  >
    {#snippet icon()}
      <QrCode size={48} strokeWidth={1.7} />
    {/snippet}
  </PageHeader>

  {#if error}
    <div class="error-message">
      <CircleX size={18} />
      {error}
    </div>
  {/if}

  <div class="generator-layout">
    <section class="settings-panel">
      <h2>Settings</h2>

      <FormGroup label="Data to encode" id="qr-data">
        <input
          id="qr-data"
          type="text"
          bind:value={qrData}
          placeholder="https://example.com"
        />
      </FormGroup>

      <FormGroup label="Error Correction" id="error-correction">
        <select id="error-correction" bind:value={errorCorrection}>
          <option value="L">Low (7%)</option>
          <option value="M">Medium (15%)</option>
          <option value="Q">Quartile (25%)</option>
          <option value="H">High (30%) - recommended for logo</option>
        </select>
      </FormGroup>

      <ModeToggle
        {useStyledImage}
        onToggle={(advanced) => {
          useStyledImage = advanced;
        }}
      />

      {#if !useStyledImage}
        <QRBasicSettings bind:fillColor bind:backColor />
      {/if}

      {#if useStyledImage}
        <QRModuleSettings
          bind:moduleDrawerType
          bind:moduleDrawerSizeRatio
          bind:moduleDrawerRadiusRatio
        />

        <QREyeSettings bind:eyeDrawerType bind:eyeDrawerRadiusRatio />

        <QRColorMaskSettings
          bind:colorMaskType
          bind:colorMaskFrontColor
          bind:colorMaskCenterColor
          bind:colorMaskEdgeColor
          bind:colorMaskTopColor
          bind:colorMaskBottomColor
          bind:colorMaskLeftColor
          bind:colorMaskRightColor
          bind:colorMaskBackColor
          bind:colorMaskImagePreview
          onImageUpload={handleColorMaskImageUpload}
          onImageRemove={removeColorMaskImage}
          onError={(msg) => (error = msg)}
        />
      {/if}

      <SettingsSection h3="Embedded Logo" icon={ImageIcon}>
        <ImageUpload
          preview={embeddedImagePreview}
          label="Click to upload logo"
          hint="PNG, JPG, WEBP up to 3MB"
          onUpload={handleLogoUpload}
          onRemove={removeLogo}
          onError={(msg) => (error = msg)}
        />

        {#if embeddedImagePreview}
          <div class="info-banner">
            <span class="info-icon">ℹ️</span>
            <span
              >Logo embedding requires <strong>Advanced mode</strong> with
              <strong>High error correction</strong></span
            >
          </div>
        {/if}
      </SettingsSection>

      <Button fullWidth disabled={isLoading} onclick={handleGenerate}>
        {isLoading ? "Generating..." : "Generate QR Code"}
      </Button>
    </section>

    <QRResultPanel {generatedQR} {isLoading} onDownload={downloadQR} />
  </div>

  <Toast message={toastMessage} onClose={() => (toastMessage = null)} />
</div>

<style>
  .page-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
  }

  .generator-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }

  @media (max-width: 900px) {
    .generator-layout {
      grid-template-columns: 1fr;
    }
  }

  .settings-panel {
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

  input[type="text"],
  select {
    width: 100%;
    padding: 0.75rem;
    background: var(--md-sys-color-surface-container-high);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-small);
    color: var(--md-sys-color-on-surface);
    font-size: 0.95rem;
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

  .info-banner {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    background: var(--md-sys-color-tertiary-container);
    color: var(--md-sys-color-on-tertiary-container);
    border-radius: var(--md-sys-shape-corner-small);
    border-left: 3px solid var(--md-sys-color-tertiary);
    font-size: 0.9rem;
  }

  .info-icon {
    font-size: 1.25rem;
    flex-shrink: 0;
  }
</style>
