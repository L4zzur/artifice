<script lang="ts">
  import type { EyeDrawerType } from "$lib/api/qr";
  import FormGroup from "$lib/components/ui/FormGroup.svelte";
  import SettingsSection from "$lib/components/ui/SettingsSection.svelte";

  interface Props {
    eyeDrawerType: EyeDrawerType;
    eyeDrawerRadiusRatio: number;
  }

  let {
    eyeDrawerType = $bindable(),
    eyeDrawerRadiusRatio = $bindable(),
  }: Props = $props();
</script>

<SettingsSection h3="Eye Style (Position Markers)">
  <FormGroup label="Shape" id="eye-drawer">
    <select id="eye-drawer" bind:value={eyeDrawerType}>
      <option value="square">Square</option>
      <option value="circle">Circle</option>
      <option value="rounded">Rounded</option>
    </select>
  </FormGroup>

  {#if eyeDrawerType === "rounded"}
    <FormGroup
      label="Corner Radius: {eyeDrawerRadiusRatio.toFixed(2)}"
      id="eye-radius"
    >
      <input
        id="eye-radius"
        type="range"
        min="0"
        max="1.0"
        step="0.05"
        bind:value={eyeDrawerRadiusRatio}
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
