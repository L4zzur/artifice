<script lang="ts">
  import type { PasswordStrengthInfo } from "$lib/api/generated";
  import PasswordStrength from "../PasswordStrength.svelte";

  interface Props {
    strengthInfo: PasswordStrengthInfo | null;
    hasPassword: boolean;
  }

  let { strengthInfo, hasPassword }: Props = $props();
</script>

<section class="analysis-panel">
  <h2>Strength Analysis</h2>

  {#if !hasPassword}
    <div class="empty-state">
      <p>Enter a password to analyze its strength</p>
    </div>
  {:else if strengthInfo}
    <PasswordStrength {strengthInfo} />
  {:else}
    <div class="empty-state">
      <p>Analyzing password...</p>
    </div>
  {/if}
</section>

<style>
  .analysis-panel {
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

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem;
    text-align: center;
  }

  .empty-state p {
    margin: 0;
    color: var(--md-sys-color-on-surface-variant);
    font-size: 0.9375rem;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
