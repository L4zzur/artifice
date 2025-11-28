<script lang="ts">
  import FormGroup from "../../ui/FormGroup.svelte";

  interface Props {
    length: number;
    includeUppercase: boolean;
    includeLowercase: boolean;
    includeNumbers: boolean;
    includeSymbols: boolean;
    includeSimilar: boolean;
  }

  let {
    length = $bindable(),
    includeUppercase = $bindable(),
    includeLowercase = $bindable(),
    includeNumbers = $bindable(),
    includeSymbols = $bindable(),
    includeSimilar = $bindable(),
  }: Props = $props();
</script>

<section class="settings-panel">
  <h2>Settings</h2>
  <div class="settings-form">
    <FormGroup label="Length: {length}" id="length">
      <input id="length" type="range" min="4" max="64" bind:value={length} />
    </FormGroup>

    <div class="checkbox-group">
      <label class="checkbox-label">
        <input id="uppercase" type="checkbox" bind:checked={includeUppercase} />
        <span>Uppercase (A-Z)</span>
      </label>

      <label class="checkbox-label">
        <input id="lowercase" type="checkbox" bind:checked={includeLowercase} />
        <span>Lowercase (a-z)</span>
      </label>

      <label class="checkbox-label">
        <input id="numbers" type="checkbox" bind:checked={includeNumbers} />
        <span>Numbers (0-9)</span>
      </label>

      <label class="checkbox-label">
        <input id="symbols" type="checkbox" bind:checked={includeSymbols} />
        <span>Symbols (!@#$%^&*()_+-=[]?)</span>
      </label>

      <label class="checkbox-label">
        <input id="similar" type="checkbox" bind:checked={includeSimilar} />
        <span>Similar characters (i, l, 1, o, 0)</span>
      </label>
    </div>
  </div>
</section>

<style>
  .settings-panel {
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-large);
    padding: 2rem;
  }

  h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 1.5rem 0;
    color: var(--md-sys-color-on-surface);
  }

  .settings-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  input[type="range"] {
    width: 100%;
    height: 6px;
    border-radius: var(--md-sys-shape-corner-full);
    background: var(--md-sys-color-surface-container-high);
    outline: none;
    cursor: pointer;
    accent-color: var(--md-sys-color-primary);
  }

  .checkbox-group {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    cursor: pointer;
    user-select: none;
  }

  .checkbox-label input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
    accent-color: var(--md-sys-color-primary);
  }

  .checkbox-label span {
    font-size: 0.9375rem;
    color: var(--md-sys-color-on-surface);
  }
</style>
