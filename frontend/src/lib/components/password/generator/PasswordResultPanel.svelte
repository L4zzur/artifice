<script lang="ts">
  import type { PasswordStrengthInfo } from "$lib/api/generated";
  import { Copy, RefreshCcw } from "lucide-svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import PasswordStrength from "../PasswordStrength.svelte";

  interface Props {
    password: string | null;
    strengthInfo: PasswordStrengthInfo | null;
    onCopy: () => void;
    onGenerate: () => void;
  }

  let { password, strengthInfo, onCopy, onGenerate }: Props = $props();
</script>

<section class="result-panel">
  <h2>Generated Password</h2>

  {#if password}
    <div class="password-display">
      <div class="password-value">{password}</div>

      <div class="password-actions">
        <Button onclick={onCopy} fullWidth>
          <Copy size={16} />Copy
        </Button>
        <Button onclick={onGenerate} variant="secondary" fullWidth>
          <RefreshCcw size={16} />
          Generate New
        </Button>
      </div>
    </div>

    {#if strengthInfo}
      <PasswordStrength {strengthInfo} />
    {/if}
  {/if}
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

  .password-display {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .password-value {
    padding: 1.5rem;
    background: var(--md-sys-color-surface-container-high);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    font-family: "Courier New", Consolas, Monaco, monospace;
    font-size: 1.125rem;
    word-break: break-all;
    color: var(--md-sys-color-on-surface);
    line-height: 1.6;
  }

  .password-actions {
    display: flex;
    gap: 0.75rem;
  }
</style>
