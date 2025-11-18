<script lang="ts">
  interface Props {
    value: string;
    id?: string;
  }

  let { value = $bindable(), id }: Props = $props();
</script>

<input {id} type="color" bind:value />

<style>
  input[type="color"] {
    width: 100%;
    height: 48px;
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-small);
    cursor: pointer;
    background: transparent;
    padding: 4px;
    transition: border-color var(--md-sys-animation-standard);
  }

  input[type="color"]:hover {
    border-color: var(--md-sys-color-primary);
  }

  input[type="color"]:focus {
    outline: 2px solid var(--md-sys-color-primary);
    outline-offset: 2px;
  }

  input[type="color"]::-webkit-color-swatch-wrapper {
    padding: 0;
    border-radius: calc(var(--md-sys-shape-corner-small) - 4px);
  }

  input[type="color"]::-webkit-color-swatch {
    border: none;
    border-radius: calc(var(--md-sys-shape-corner-small) - 4px);
  }

  input[type="color"]::-moz-color-swatch {
    border: none;
    border-radius: calc(var(--md-sys-shape-corner-small) - 4px);
  }
</style>
