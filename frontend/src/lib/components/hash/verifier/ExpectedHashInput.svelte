<script lang="ts">
  interface Props {
    expectedHash: string;
  }

  let { expectedHash = $bindable() }: Props = $props();
</script>

<section class="input-panel">
  <h2>Expected Hash</h2>

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
</section>

<style>
  .input-panel {
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-large);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  h2 {
    font-size: 1.125rem;
    font-weight: 600;
    margin: 0 0 0.3rem 0;
    color: var(--md-sys-color-on-surface);
  }

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
