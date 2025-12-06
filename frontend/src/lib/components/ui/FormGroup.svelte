<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    label: string;
    id?: string;
    children: Snippet;
  }

  let { label, id, children }: Props = $props();
</script>

<div class="form-group">
  {#if id}
    <label for={id}>{label}</label>
  {:else}
    <!-- svelte-ignore a11y_label_has_associated_control -->
    <label>{label}</label>
  {/if}
  {@render children()}
</div>

<style>
  .form-group {
    margin: 0 0 0.5rem 0;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface-variant);
  }
</style>
