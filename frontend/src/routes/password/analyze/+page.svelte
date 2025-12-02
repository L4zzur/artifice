<script lang="ts">
  import type { PasswordStrengthInfo } from "$lib/api/generated";
  import { analyzePassword } from "$lib/api/password";
  import PasswordAnalysisPanel from "$lib/components/password/analyzer/PasswordAnalysisPanel.svelte";
  import PasswordInputPanel from "$lib/components/password/analyzer/PasswordInputPanel.svelte";
  import PageHeader from "$lib/components/ui/PageHeader.svelte";
  import Toast from "$lib/components/ui/Toast.svelte";
  import { CircleX, ShieldCheck } from "lucide-svelte";

  let toastMessage = $state<string | null>(null);
  let toastTimeout: ReturnType<typeof setTimeout> | null = null;

  let password = $state("");
  let strengthInfo = $state<PasswordStrengthInfo | null>(null);
  let isAnalyzing = $state(false);
  let error = $state<string | null>(null);

  // Дебаунс для предотвращения частых запросов
  let debounceTimer: ReturnType<typeof setTimeout> | null = null;

  async function handleAnalyze() {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }

    if (password.trim().length === 0) {
      strengthInfo = null;
      error = null;
      return;
    }

    // Задержка перед анализом (500мс)
    debounceTimer = setTimeout(async () => {
      isAnalyzing = true;
      error = null;

      try {
        const result = await analyzePassword({ password });
        strengthInfo = result.info;
      } catch (e) {
        if (e instanceof Error) {
          error = e.message;
        } else {
          error = "An unexpected error occurred";
        }
        console.error("Password analysis error:", e);
        strengthInfo = null;
      } finally {
        isAnalyzing = false;
      }
    }, 500);
  }

  // Автоматический анализ при изменении пароля
  $effect(() => {
    // Триггер на изменение пароля
    password;
    handleAnalyze();
  });

  function showToast(message: string, duration: number = 4000) {
    toastMessage = message;

    if (toastTimeout) {
      clearTimeout(toastTimeout);
    }

    toastTimeout = setTimeout(() => {
      toastMessage = null;
    }, duration);
  }
</script>

<div class="page-container">
  <PageHeader
    title="Password Checker"
    description="Check the strength of a password"
    backLink={{ href: "/password", label: "Back to Password Tools" }}
  >
    {#snippet icon()}
      <ShieldCheck size={48} strokeWidth={1.7} />
    {/snippet}
  </PageHeader>

  {#if error}
    <div class="error-message">
      <CircleX size={18} />
      {error}
    </div>
  {/if}

  <div class="analyzer-layout">
    <PasswordInputPanel bind:password />

    <PasswordAnalysisPanel
      {strengthInfo}
      hasPassword={password.trim().length > 0}
    />
  </div>

  <Toast message={toastMessage} onClose={() => (toastMessage = null)} />
</div>

<style>
  .page-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
  }

  .analyzer-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-top: 2rem;
    align-items: start;
  }

  @media (max-width: 900px) {
    .analyzer-layout {
      grid-template-columns: 1fr;
    }
  }

  .error-message {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1rem;
    padding: 0.75rem;
    background: var(--md-sys-color-error-container);
    color: var(--md-sys-color-on-error-container);
    border-radius: var(--md-sys-shape-corner-medium);
    font-size: 0.9rem;
  }
</style>
