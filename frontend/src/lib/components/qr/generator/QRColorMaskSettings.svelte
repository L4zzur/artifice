<script lang="ts">
  import type { ColorMaskType } from "$lib/api/qr";
  import ColorPicker from "$lib/components/ui/ColorPicker.svelte";
  import FormGroup from "$lib/components/ui/FormGroup.svelte";
  import FormRow from "$lib/components/ui/FormRow.svelte";
  import ImageUpload from "$lib/components/ui/ImageUpload.svelte";
  import SettingsSection from "$lib/components/ui/SettingsSection.svelte";

  interface Props {
    colorMaskType: ColorMaskType;
    colorMaskFrontColor: string;
    colorMaskBackColor: string;
    colorMaskCenterColor: string;
    colorMaskEdgeColor: string;
    colorMaskLeftColor: string;
    colorMaskRightColor: string;
    colorMaskTopColor: string;
    colorMaskBottomColor: string;
    colorMaskImagePreview: string | null;
    onImageUpload: (base64: string) => void;
    onImageRemove: () => void;
    onError?: (message: string) => void;
  }

  let {
    colorMaskType = $bindable(),
    colorMaskFrontColor = $bindable(),
    colorMaskBackColor = $bindable(),
    colorMaskCenterColor = $bindable(),
    colorMaskEdgeColor = $bindable(),
    colorMaskLeftColor = $bindable(),
    colorMaskRightColor = $bindable(),
    colorMaskTopColor = $bindable(),
    colorMaskBottomColor = $bindable(),
    colorMaskImagePreview = $bindable(),
    onImageUpload,
    onImageRemove,
    onError,
  }: Props = $props();
</script>

<SettingsSection h3="Color Style">
  <FormGroup label="Type" id="color-mask">
    <select id="color-mask" bind:value={colorMaskType}>
      <option value="solid">Solid</option>
      <option value="radial_gradient">Radial Gradient</option>
      <option value="square_gradient">Square Gradient</option>
      <option value="vertical_gradient">Vertical Gradient</option>
      <option value="horizontal_gradient">Horizontal Gradient</option>
      <option value="image">Image Pattern</option>
    </select>
  </FormGroup>

  {#if colorMaskType === "solid"}
    <FormRow>
      <FormGroup label="Fill Color" id="cm-front">
        <ColorPicker id="cm-front" bind:value={colorMaskFrontColor} />
      </FormGroup>
      <FormGroup label="Background Color" id="cm-back">
        <ColorPicker id="cm-back" bind:value={colorMaskBackColor} />
      </FormGroup>
    </FormRow>
  {/if}

  {#if colorMaskType === "radial_gradient" || colorMaskType === "square_gradient"}
    <FormRow>
      <FormGroup label="Fill Color" id="cm-center">
        <ColorPicker id="cm-center" bind:value={colorMaskCenterColor} />
      </FormGroup>
      <FormGroup label="Edge Color" id="cm-edge">
        <ColorPicker id="cm-edge" bind:value={colorMaskEdgeColor} />
      </FormGroup>
    </FormRow>
  {/if}

  {#if colorMaskType === "vertical_gradient"}
    <FormRow>
      <FormGroup label="Top Color" id="cm-top">
        <ColorPicker id="cm-top" bind:value={colorMaskTopColor} />
      </FormGroup>
      <FormGroup label="Bottom Color" id="cm-bottom">
        <ColorPicker id="cm-bottom" bind:value={colorMaskBottomColor} />
      </FormGroup>
    </FormRow>
  {/if}

  {#if colorMaskType === "horizontal_gradient"}
    <FormRow>
      <FormGroup label="Left Color" id="cm-left">
        <ColorPicker id="cm-left" bind:value={colorMaskLeftColor} />
      </FormGroup>
      <FormGroup label="Right Color" id="cm-right">
        <ColorPicker id="cm-right" bind:value={colorMaskRightColor} />
      </FormGroup>
    </FormRow>
  {/if}

  {#if colorMaskType === "image"}
    <FormGroup label="Pattern Image" id="cm-image">
      <ImageUpload
        preview={colorMaskImagePreview}
        label="Upload pattern image"
        hint="This image will be used as QR code fill pattern\nPNG, JPG, WEBP up to 3MB"
        onUpload={onImageUpload}
        onRemove={onImageRemove}
        {onError}
      />
    </FormGroup>

    <FormGroup label="Background Color" id="cm-back-image">
      <ColorPicker id="cm-back-image" bind:value={colorMaskBackColor} />
      {#if colorMaskBackColor === "#000000"}
        <div class="warning-message">
          ⚠️ Pure black background may result in invisible QR code
        </div>
      {/if}
    </FormGroup>
  {/if}
</SettingsSection>

<style>
  select {
    width: 100%;
    padding: 0.75rem;
    background: var(--md-sys-color-surface-container-high);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-small);
    color: var(--md-sys-color-on-surface);
    font-size: 0.95rem;
  }

  .warning-message {
    margin-top: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: var(--md-sys-color-tertiary-container);
    color: var(--md-sys-color-on-tertiary-container);
    border-radius: var(--md-sys-shape-corner-small);
    border-left: 3px solid var(--md-sys-color-tertiary);
    font-size: 0.875rem;
  }
</style>
