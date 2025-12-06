<script lang="ts">
  import { CircleX } from "lucide-svelte";

  interface Props {
    message: string | null;
    onDismiss?: () => void;
  }

  let { message, onDismiss }: Props = $props();
</script>

{#if message}
  <div class="error-banner">
    <div class="error-content">
      <CircleX size={18} />
      <span class="error-text">{message}</span>
    </div>
    {#if onDismiss}
      <button
        class="dismiss-button"
        onclick={onDismiss}
        aria-label="Dismiss error"
      >
        ×
      </button>
    {/if}
  </div>
{/if}

<style>
  .error-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: var(--md-sys-color-error-container);
    color: var(--md-sys-color-on-error-container);
    border-radius: var(--md-sys-shape-corner-medium);
    font-size: 0.9rem;
    margin-bottom: 1rem;
    animation: slideDown 0.2s ease-out;
  }

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .error-content {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
    min-width: 0;
  }

  .error-text {
    flex: 1;
    word-break: break-word;
  }

  .dismiss-button {
    background: none;
    border: none;
    color: var(--md-sys-color-on-error-container);
    font-size: 1.5rem;
    line-height: 1;
    cursor: pointer;
    padding: 0.25rem 0.5rem;
    border-radius: var(--md-sys-shape-corner-small);
    transition: background 0.2s ease;
    flex-shrink: 0;
  }

  .dismiss-button:hover {
    background: rgba(0, 0, 0, 0.1);
  }
</style>
