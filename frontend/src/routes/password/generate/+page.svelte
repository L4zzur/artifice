<script lang="ts">
  import type {
    PasswordGenerateRequest,
    PasswordStrengthInfo,
  } from "$lib/api/generated";
  import { generatePassword } from "$lib/api/password";
  import PasswordResultPanel from "$lib/components/password/generator/PasswordResultPanel.svelte";
  import PasswordSettingsPanel from "$lib/components/password/generator/PasswordSettingsPanel.svelte";
  import PageHeader from "$lib/components/ui/PageHeader.svelte";
  import Toast from "$lib/components/ui/Toast.svelte";
  import { ShieldPlus } from "lucide-svelte";

  let length = $state(16);
  let includeUppercase = $state(true);
  let includeLowercase = $state(true);
  let includeNumbers = $state(true);
  let includeSymbols = $state(true);
  let includeSimilar = $state(false);

  let generatedPassword = $state<string | null>(null);
  let strengthInfo = $state<PasswordStrengthInfo | null>(null);

  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let toastMessage = $state<string | null>(null);
  let toastTimeout: ReturnType<typeof setTimeout> | null = null;

  let debounceTimer: ReturnType<typeof setTimeout> | null = null;

  async function handleGenerate() {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }

    debounceTimer = setTimeout(async () => {
      if (generatedPassword) {
        isLoading = true;
      }

      error = null;

      try {
        const request: PasswordGenerateRequest = {
          length: length,
          include_uppercase: includeUppercase,
          include_lowercase: includeLowercase,
          include_numbers: includeNumbers,
          include_symbols: includeSymbols,
          include_similar: includeSimilar,
        };

        const result = await generatePassword(request);
        generatedPassword = result.password;
        strengthInfo = result.strength;
      } catch (e) {
        if (e instanceof Error) {
          error = e.message;
        } else {
          error = "An unexpected error occurred";
        }
        console.error("Password generation error:", e);
      } finally {
        isLoading = false;
      }
    }, 300);
  }

  async function handleCopy() {
    if (!generatedPassword) return;

    try {
      await navigator.clipboard.writeText(generatedPassword);
      showToast("Password copied to clipboard");
    } catch (e) {
      console.error("Failed to copy password.");
      showToast("Failed to copy password");
    }
  }

  function showToast(message: string, duration: number = 4000) {
    toastMessage = message;

    if (toastTimeout) {
      clearTimeout(toastTimeout);
    }

    toastTimeout = setTimeout(() => {
      toastMessage = null;
    }, duration);
  }

  $effect(() => {
    length;
    includeUppercase;
    includeLowercase;
    includeNumbers;
    includeSymbols;
    includeSimilar;
    handleGenerate();
  });
</script>

<div class="page-container">
  <PageHeader
    title="Password Generator"
    description="Generate strong and secure passwords with strength meter"
    backLink={{ href: "/password", label: "Back to Password Tools" }}
  >
    {#snippet icon()}
      <ShieldPlus size={48} strokeWidth={1.7} />
    {/snippet}
  </PageHeader>

  <div class="generator-layout">
    <PasswordSettingsPanel
      bind:length
      bind:includeUppercase
      bind:includeLowercase
      bind:includeNumbers
      bind:includeSymbols
      bind:includeSimilar
    />

    <PasswordResultPanel
      password={generatedPassword}
      {strengthInfo}
      onCopy={handleCopy}
      onGenerate={handleGenerate}
    />
  </div>

  {#if error}
    <div class="error-message">{error}</div>
  {/if}

  <Toast message={toastMessage} onClose={() => (toastMessage = null)} />
</div>

<style>
  .page-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
  }

  .generator-layout {
    display: grid;
    grid-template-columns: 0.7fr 1.3fr;
    gap: 2rem;
    margin-top: 2rem;
    align-items: start;
  }

  @media (max-width: 900px) {
    .generator-layout {
      grid-template-columns: 1fr;
    }
  }

  .error-message {
    margin-top: 1rem;
    padding: 1rem;
    background: var(--md-sys-color-error-container);
    color: var(--md-sys-color-on-error-container);
    border-radius: var(--md-sys-shape-corner-medium);
  }
</style>
