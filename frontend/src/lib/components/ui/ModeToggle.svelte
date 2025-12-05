<script lang="ts" generics="T extends string">
  interface Props {
    options: { value: T; label: string }[];
    selected: T;
    onChange: (value: T) => void;
  }

  let { options, selected, onChange }: Props = $props();
</script>

<div class="mode-toggle">
  {#each options as option}
    <button
      class="mode-button {selected === option.value ? 'active' : ''}"
      onclick={() => onChange(option.value)}
      aria-label="Switch to {option.label} mode"
    >
      {option.label}
    </button>
  {/each}
</div>

<style>
  .mode-toggle {
    display: flex;
    gap: 0.25rem;
    padding: 0.25rem;
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    width: fit-content;
  }

  .mode-button {
    padding: 0.375rem 1rem;
    background: none;
    border: none;
    border-radius: var(--md-sys-shape-corner-small);
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface-variant);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .mode-button:hover {
    background: var(--md-sys-color-surface-container-high);
    color: var(--md-sys-color-on-surface);
  }

  .mode-button.active {
    background: var(--md-sys-color-primary);
    color: var(--md-sys-color-on-primary);
  }
</style>
