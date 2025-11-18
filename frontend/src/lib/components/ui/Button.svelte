<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    variant?: "primary" | "secondary" | "error";
    disabled?: boolean;
    fullWidth?: boolean;
    onclick?: () => void;
    children: Snippet;
  }

  let {
    variant = "primary",
    disabled = false,
    fullWidth = false,
    onclick,
    children,
  }: Props = $props();
</script>

<button
  class="button"
  class:primary={variant === "primary"}
  class:secondary={variant === "secondary"}
  class:error={variant === "error"}
  class:full-width={fullWidth}
  {disabled}
  {onclick}
>
  {@render children()}
</button>

<style>
  .button {
    padding: 0.875rem 1.5rem;
    border: none;
    border-radius: var(--md-sys-shape-corner-medium);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--md-sys-animation-standard);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(176, 196, 222, 0.3);
  }

  .button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .button.primary {
    background: var(--md-sys-color-primary);
    color: var(--md-sys-color-on-primary);
  }

  .button.secondary {
    background: var(--md-sys-color-secondary);
    color: var(--md-sys-color-on-secondary);
  }

  .button.error {
    background: var(--md-sys-color-error);
    color: var(--md-sys-color-on-error);
  }

  .button.full-width {
    width: 100%;
  }
</style>
