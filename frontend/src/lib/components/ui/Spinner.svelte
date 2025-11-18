<script lang="ts">
  interface Props {
    size?: number;
    message?: string;
  }

  let { size = 48, message }: Props = $props();
</script>

<div class="loading-state">
  <div class="spinner" style="width: {size}px; height: {size}px;"></div>
  {#if message}
    <p>{message}</p>
  {/if}
</div>

<style>
  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
  }

  .spinner {
    border: 4px solid var(--md-sys-color-outline-variant);
    border-top-color: var(--md-sys-color-primary);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  p {
    margin-top: 1rem;
    color: var(--md-sys-color-on-surface-variant);
  }
</style>
