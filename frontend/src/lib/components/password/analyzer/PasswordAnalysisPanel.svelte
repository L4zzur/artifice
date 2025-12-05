<script lang="ts">
  import type { PasswordStrengthInfo } from "$lib/api/generated";
  import Panel from "$lib/components/ui/Panel.svelte";
  import PasswordStrength from "../PasswordStrength.svelte";

  interface Props {
    strengthInfo: PasswordStrengthInfo | null;
    hasPassword: boolean;
  }

  let { strengthInfo, hasPassword }: Props = $props();
</script>

<Panel title="Strength Analysis">
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
</Panel>

<style>
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
