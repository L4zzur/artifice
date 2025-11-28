<script lang="ts">
  import { Eye, EyeOff } from "lucide-svelte";

  interface Props {
    password: string;
  }

  let { password = $bindable() }: Props = $props();
  let showPassword = $state(false);

  function togglePasswordVisibility() {
    showPassword = !showPassword;
  }
</script>

<section class="input-panel">
  <h2>Analyze Password Strength</h2>

  <div class="input-group">
    <label for="password-input" class="input-label">
      Enter your password to analyze its strength
    </label>

    <div class="password-input-wrapper">
      <input
        id="password-input"
        type={showPassword ? "text" : "password"}
        bind:value={password}
        placeholder="Enter password..."
        class="password-input"
        autocomplete="off"
        spellcheck="false"
      />

      <button
        type="button"
        class="toggle-visibility"
        onclick={togglePasswordVisibility}
        aria-label={showPassword ? "Hide password" : "Show password"}
      >
        {#if showPassword}
          <Eye size={16} strokeWidth={2} />
        {:else}
          <EyeOff size={16} strokeWidth={2} />
        {/if}
      </button>
    </div>

    {#if password.length > 0}
      <p class="character-count">
        {password.length} character{password.length === 1 ? "" : "s"}
      </p>
    {/if}
  </div>
</section>

<style>
  .input-panel {
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

  .input-group {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .input-label {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface-variant);
  }

  .password-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }

  .password-input {
    width: 100%;
    padding: 1rem 3rem 1rem 1rem;
    background: var(--md-sys-color-surface-container-high);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    font-family: "Courier New", Consolas, Monaco, monospace;
    font-size: 1rem;
    color: var(--md-sys-color-on-surface);
    transition: border-color 0.2s ease;
  }

  .password-input:focus {
    outline: none;
    border-color: var(--md-sys-color-primary);
  }

  .password-input::placeholder {
    color: var(--md-sys-color-on-surface-variant);
    opacity: 0.5;
    font-family:
      system-ui,
      -apple-system,
      sans-serif;
  }

  .toggle-visibility {
    position: absolute;
    right: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem;
    background: transparent;
    border: none;
    border-radius: var(--md-sys-shape-corner-small);
    color: var(--md-sys-color-on-surface-variant);
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .toggle-visibility:hover {
    background: var(--md-sys-color-surface-container-highest);
  }

  .toggle-visibility:active {
    background: var(--md-sys-color-surface-container);
  }

  .character-count {
    margin: 0;
    font-size: 0.75rem;
    color: var(--md-sys-color-on-surface-variant);
    opacity: 0.7;
  }
</style>
