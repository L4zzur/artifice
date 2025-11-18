<script lang="ts">
  import { X } from "lucide-svelte";

  type Props = {
    message: string | null;
    onClose?: () => void;
  };

  let { message, onClose }: Props = $props();
</script>

{#if message}
  <div class="toast">
    <span>{message}</span>
    <div class="toast-close">
      <X size={18} strokeWidth={2} onclick={onClose} />
    </div>
  </div>
{/if}

<style>
  .toast {
    position: fixed;
    bottom: 90%;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1rem;
    background: var(--md-sys-color-tertiary-container);
    color: var(--md-sys-color-on-tertiary-container);
    border-radius: var(--md-sys-shape-corner-medium);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    z-index: 1000;
    max-width: 90%;
    animation: slideUp 0.3s ease-in-out;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateX(-50%) translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }

  .toast span {
    font-size: 0.95rem;
    line-height: 1.4;
  }

  .toast-close {
    background: none;
    border: none;
    color: inherit;
    font-size: 1.25rem;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background var(--md-sys-animation-standard);
  }

  .toast-close:hover {
    background: rgba(0, 0, 0, 0.1);
  }
</style>
