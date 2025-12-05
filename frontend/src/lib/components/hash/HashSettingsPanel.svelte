<script lang="ts">
  import { onMount } from "svelte";
  import FormGroup from "$lib/components/ui/FormGroup.svelte";
  import {
    type HashAlgorithmSchema,
    type HashAlgorithm,
    type SchemasHashOutputFormat,
  } from "$lib/api/generated";
  import { listHashAlgorithms } from "$lib/api/hash";

  interface Props {
    algorithm: HashAlgorithm;
    outputFormat: SchemasHashOutputFormat;
    hmacKey: string;
  }

  let {
    algorithm = $bindable(),
    outputFormat = $bindable(),
    hmacKey = $bindable(),
  }: Props = $props();

  let algorithms = $state<HashAlgorithmSchema[]>([]);
  let isLoadingAlgorithms = $state(true);
  let algorithmError = $state<string | null>(null);

  onMount(async () => {
    try {
      algorithms = await listHashAlgorithms();
    } catch (e) {
      algorithmError = "Failed to load algorithms";
      console.error("Failed to load hash algorithms:", e);
      algorithms = [
        {
          name: "md5",
          label: "MD5 (128-bit)",
          output_bits: 128,
          output_hex_length: 32,
          output_base64_length: 24,
          security: "Legacy",
          description: "Fast but cryptographically broken",
          recommended: false,
        },
        {
          name: "sha256",
          label: "SHA-256 (256-bit)",
          output_bits: 256,
          output_hex_length: 64,
          output_base64_length: 44,
          security: "Strong",
          description: "Industry standard",
          recommended: true,
        },
        {
          name: "sha512",
          label: "SHA-512 (512-bit)",
          output_bits: 512,
          output_hex_length: 128,
          output_base64_length: 88,
          security: "Very Strong",
          description: "High security",
          recommended: true,
        },
      ] as HashAlgorithmSchema[];
    } finally {
      isLoadingAlgorithms = false;
    }
  });
</script>

<section class="settings-panel">
  <h2>Settings</h2>

  <div class="settings-grid">
    <div class="settings-row">
      <FormGroup label="Hash Algorithm">
        {#if isLoadingAlgorithms}
          <div class="loading-select">Loading algorithms...</div>
        {:else if algorithmError}
          <div class="error-select">{algorithmError}</div>
        {:else}
          <select bind:value={algorithm} class="select-input">
            {#each algorithms as algo}
              <option value={algo.name} title={algo.description}>
                {algo.label}
                {#if algo.recommended}
                  ⭐
                {/if}
                - {algo.security}
              </option>
            {/each}
          </select>
        {/if}
      </FormGroup>

      <FormGroup label="Output Format">
        <select bind:value={outputFormat} class="select-input">
          <option value="hex">Hex</option>
          <option value="base64">Base64</option>
        </select>
      </FormGroup>
    </div>
    <FormGroup label="HMAC Key (optional)">
      <input
        type="text"
        bind:value={hmacKey}
        placeholder="Enter HMAC key..."
        class="text-input"
      />
    </FormGroup>
  </div>
</section>

<style>
  .settings-panel {
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-large);
    padding: 1.5rem;
  }

  h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
    color: var(--md-sys-color-on-surface);
  }

  .settings-grid {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .settings-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  .select-input,
  .text-input {
    width: 100%;
    padding: 0.75rem;
    background: var(--md-sys-color-surface-container-high);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-small);
    font-size: 0.9375rem;
    color: var(--md-sys-color-on-surface);
    transition: border-color 0.2s ease;
  }

  .select-input:focus,
  .text-input:focus {
    outline: none;
    border-color: var(--md-sys-color-primary);
  }
</style>
