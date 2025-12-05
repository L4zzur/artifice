<script lang="ts">
  import Panel from "$lib/components/ui/Panel.svelte";

  interface Props {
    expectedHash: string;
  }

  let { expectedHash = $bindable() }: Props = $props();
</script>

<Panel title="Expected Hash">
  <div class="input-group">
    <label for="expected-hash" class="input-label">Hash to compare</label>

    <textarea
      id="expected-hash"
      bind:value={expectedHash}
      placeholder="Paste expected hash here..."
      class="input-data"
      rows="2"
      spellcheck="false"
    ></textarea>

    {#if expectedHash.length > 0}
      <p class="input-length">
        {expectedHash.length} character{expectedHash.length === 1 ? "" : "s"}
      </p>
    {/if}
  </div>
</Panel>

<style>
  .input-group {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
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
    flex-shrink: 0;
  }
</style>
