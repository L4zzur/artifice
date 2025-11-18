<script lang="ts">
  import type { ModuleDrawerType } from "$lib/api/qr";
  import FormGroup from "$lib/components/ui/FormGroup.svelte";
  import SettingsSection from "$lib/components/ui/SettingsSection.svelte";

  interface Props {
    moduleDrawerType: ModuleDrawerType;
    moduleDrawerSizeRatio: number;
    moduleDrawerRadiusRatio: number;
  }

  let {
    moduleDrawerType = $bindable(),
    moduleDrawerSizeRatio = $bindable(),
    moduleDrawerRadiusRatio = $bindable(),
  }: Props = $props();
</script>

<SettingsSection h3="Module Style">
  <FormGroup label="Shape" id="module-drawer">
    <select id="module-drawer" bind:value={moduleDrawerType}>
      <option value="square">Square</option>
      <option value="gapped_square">Gapped Square</option>
      <option value="circle">Circle</option>
      <option value="rounded">Rounded</option>
      <option value="vertical_bars">Vertical Bars</option>
      <option value="horizontal_bars">Horizontal Bars</option>
    </select>
  </FormGroup>

  {#if moduleDrawerType === "gapped_square"}
    <FormGroup
      label="Gap Size: {moduleDrawerSizeRatio.toFixed(2)}"
      id="size-ratio"
    >
      <input
        id="size-ratio"
        type="range"
        min="0.1"
        max="1.0"
        step="0.05"
        bind:value={moduleDrawerSizeRatio}
      />
    </FormGroup>
  {/if}

  {#if moduleDrawerType === "rounded"}
    <FormGroup
      label="Corner Radius: {moduleDrawerRadiusRatio.toFixed(2)}"
      id="size-ratio"
    >
      <input
        id="size-ratio"
        type="range"
        min="0"
        max="1.0"
        step="0.05"
        bind:value={moduleDrawerRadiusRatio}
      />
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

  input[type="range"] {
    width: 100%;
    accent-color: var(--md-sys-color-primary);
  }
</style>
