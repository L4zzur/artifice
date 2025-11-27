<script lang="ts">
  import type { PasswordStrengthInfo } from "$lib/api/generated";

  interface Props {
    strengthInfo: PasswordStrengthInfo;
  }

  let { strengthInfo }: Props = $props();

  const strengthConfig: Record<
    number,
    { color: string; label: string; percentage: number }
  > = {
    0: {
      color: "var(--md-sys-color-error-container)",
      label: "Very Weak",
      percentage: 10,
    },
    1: {
      color: "var(--md-sys-color-error)",
      label: "Weak",
      percentage: 25,
    },
    2: {
      color: "var(--md-sys-color-secondary)",
      label: "Fair",
      percentage: 50,
    },
    3: {
      color: "var(--md-sys-color-tertiary)",
      label: "Strong",
      percentage: 75,
    },
    4: {
      color: "var(--md-sys-color-primary-container)",
      label: "Very Strong",
      percentage: 100,
    },
  };

  const config = $derived(strengthConfig[strengthInfo.score]);
</script>

<div class="strength-meter">
  <div class="strength-header">
    <span class="strength-label">Your password strength</span>
    <span class="strength-value" style="color: {config.color}">
      {config.label}
    </span>
  </div>

  <div class="strength-bar">
    <div
      class="strength-fill"
      style="width: {config.percentage}%; background-color: {config.color}"
    ></div>
  </div>

  <div class="strength-details">
    <p class="detail-item">
      <span class="detail-label">Estimated time to crack:</span>
      <span class="detail-value">
        {strengthInfo.crack_times.offline_slow_hashing}
      </span>
    </p>

    {#if strengthInfo.feedback.suggestions && strengthInfo.feedback.suggestions.length > 0}
      <div class="suggestions">
        <p class="suggestions-label">Suggestions:</p>
        <ul>
          {#each strengthInfo.feedback.suggestions as suggestion}
            <li>{suggestion}</li>
          {/each}
        </ul>
      </div>
    {/if}

    {#if strengthInfo.feedback.warning}
      <p class="warning">⚠️ {strengthInfo.feedback.warning}</p>
    {/if}
  </div>
</div>

<style>
  .strength-meter {
    margin-top: 1.5rem;
  }

  .strength-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .strength-label {
    font-size: 0.875rem;
    color: var(--md-sys-color-on-surface-variant);
  }

  .strength-value {
    font-size: 0.875rem;
    font-weight: 600;
  }

  .strength-bar {
    width: 100%;
    height: 8px;
    background: var(--md-sys-color-surface-container-high);
    border-radius: var(--md-sys-shape-corner-full);
    overflow: hidden;
  }

  .strength-fill {
    height: 100%;
    transition:
      width 0.3s ease,
      background-color 0.3s ease;
    border-radius: var(--md-sys-shape-corner-full);
  }

  .strength-details {
    margin-top: 1rem;
    padding: 1rem;
    background: var(--md-sys-color-surface-container-low);
    border-radius: var(--md-sys-shape-corner-medium);
  }

  .detail-item {
    display: flex;
    justify-content: space-between;
    margin: 0 0 0.5rem 0;
  }

  .detail-label {
    font-size: 0.875rem;
    color: var(--md-sys-color-on-surface-variant);
  }

  .detail-value {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface);
  }

  .suggestions {
    margin-top: 0.75rem;
  }

  .suggestions-label {
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: var(--md-sys-color-on-surface);
  }

  .suggestions ul {
    margin: 0;
    padding-left: 1.25rem;
  }

  .suggestions li {
    font-size: 0.875rem;
    color: var(--md-sys-color-on-surface-variant);
    margin-bottom: 0.25rem;
  }

  .warning {
    margin-top: 0.75rem;
    padding: 0.75rem;
    background: var(--md-sys-color-error-container);
    color: var(--md-sys-color-on-error-container);
    border-radius: var(--md-sys-shape-corner-small);
    font-size: 0.875rem;
  }
</style>
