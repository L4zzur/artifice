<script lang="ts">
  import type { HashAlgorithm } from "$lib/api/generated";
  import Button from "$lib/components/ui/Button.svelte";
  import Spinner from "$lib/components/ui/Spinner.svelte";
  import { CircleCheck, CircleX, ShieldQuestionMark } from "lucide-svelte";

  interface Props {
    isValid: boolean | null;
    isLoading: boolean;
    verifiedAlgorithm: HashAlgorithm | null;
    onVerify: () => void;
  }

  let { isValid, isLoading, verifiedAlgorithm, onVerify }: Props = $props();
</script>

<section class="result-panel">
  <h2>Verification Result</h2>

  <div class="content">
    {#if isLoading}
      <div class="state state-loading">
        <Spinner />
        <p>Verifying...</p>
      </div>
    {:else if isValid === true}
      <div class="state state-valid">
        <CircleCheck size={32} />
        <h3>Hash is valid</h3>
        {#if verifiedAlgorithm}
          <p>
            Algorithm:
            <strong>{verifiedAlgorithm}</strong>
          </p>
        {/if}
      </div>
    {:else if isValid === false}
      <div class="state state-invalid">
        <CircleX size={32} />
        <h3>Hash does not match</h3>
        {#if verifiedAlgorithm}
          <p>
            Checked with algorithm:
            <strong>{verifiedAlgorithm}</strong>
          </p>
        {/if}
      </div>
    {:else}
      <div class="state state-idle">
        <ShieldQuestionMark size={32} />
        <h3>No verification yet</h3>
        <p>Enter data and expected hash, then run verification.</p>
      </div>
    {/if}
  </div>

  <div class="actions">
    <Button onclick={onVerify} fullWidth disabled={isLoading}>
      Verify Hash
    </Button>
  </div>
</section>

<style>
  .result-panel {
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

  .content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .state {
    text-align: center;
    padding: 2rem 1rem;
    margin: 0 0 1rem 0;
    border-radius: var(--md-sys-shape-corner-medium);
    border: 1px solid transparent;
  }

  .state h3 {
    margin: 0.75rem 0 0.25rem 0;
    font-size: 1.1rem;
  }

  .state p {
    margin: 0;
    font-size: 0.9rem;
    color: var(--md-sys-color-on-surface-variant);
  }

  .state-valid {
    color: var(--md-sys-color-primary);
    border-color: rgba(0, 200, 120, 0.3);
    background: rgba(0, 200, 120, 0.06);
  }

  .state-invalid {
    color: var(--md-sys-color-error);
    border-color: rgba(220, 20, 60, 0.4);
    background: rgba(220, 20, 60, 0.06);
  }

  .state-idle {
    color: var(--md-sys-color-on-surface-variant);
    border-color: var(--md-sys-color-outline-variant);
    background: var(--md-sys-color-surface-container-high);
  }

  .state-loading {
    color: var(--md-sys-color-on-surface-variant);
    border-color: var(--md-sys-color-outline-variant);
    background: var(--md-sys-color-surface-container-high);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }

  .actions {
    display: flex;
  }
</style>
