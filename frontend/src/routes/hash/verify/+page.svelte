<script lang="ts">
  import {
    type SchemasHashOutputFormat,
    type HashAlgorithm,
    type HashVerifyRequest,
  } from "$lib/api/generated";
  import { verifyHash } from "$lib/api/hash";
  import HashSettingsPanel from "$lib/components/hash/generator/HashSettingsPanel.svelte";
  import HashVerifyInputPanel from "$lib/components/hash/verifier/HashVerifyInputPanel.svelte";
  import HashVerifyResultPanel from "$lib/components/hash/verifier/HashVerifyResultPanel.svelte";
  import PageHeader from "$lib/components/ui/PageHeader.svelte";
  import Toast from "$lib/components/ui/Toast.svelte";
  import { CircleCheckBig, CircleX, Sparkles } from "lucide-svelte";

  let inputData = $state("");
  let expectedHash = $state("");
  let algorithm = $state<HashAlgorithm>("sha256");
  let outputFormat = $state<SchemasHashOutputFormat>("hex");
  let hmacKey = $state("");

  let isValid = $state<boolean | null>(null);
  let verifiedAlgorithm = $state<HashAlgorithm | null>(null);

  let isLoading = $state(false);
  let error = $state<string | null>(null);

  let toastMessage = $state<string | null>(null);
  let toastTimeout: ReturnType<typeof setTimeout> | null = null;

  async function handleVerify() {
    const dataTrimmed = inputData.trim();
    const hashTrimmed = expectedHash.trim();

    if (!dataTrimmed || !hashTrimmed) {
      isValid = null;
      verifiedAlgorithm = null;
      error = "Please enter both data and expected hash";
      return;
    }

    isLoading = true;
    error = null;
    isValid = null;
    verifiedAlgorithm = null;

    try {
      const request: HashVerifyRequest = {
        data: dataTrimmed,
        expected_hash: hashTrimmed,
        algorithm: algorithm,
        hmac_key: hmacKey || null,
      };

      const result = await verifyHash(request);
      isValid = result.valid;
      verifiedAlgorithm = result.algorithm;
    } catch (e) {
      if (e instanceof Error) {
        error = e.message;
      } else {
        error = "An unexpected error occurred";
      }
      console.error("Hash verify error:", e);
    } finally {
      isLoading = false;
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
</script>

<div class="page-container">
  <PageHeader
    title="Hash Verifier"
    description="Verify data integrity by comparing hashes with optional HMAC"
    backLink={{ href: "/hash", label: "Back to Hash Tools" }}
  >
    {#snippet icon()}
      <CircleCheckBig size={48} strokeWidth={1.7} />
    {/snippet}
  </PageHeader>

  {#if error}
    <div class="error-message">
      <CircleX size={18} />
      {error}
    </div>
  {/if}

  <div class="verifier-layout">
    <div class="left-column">
      <HashVerifyInputPanel bind:inputData bind:expectedHash />

      <HashSettingsPanel bind:algorithm bind:outputFormat bind:hmacKey />
    </div>

    <HashVerifyResultPanel
      {isValid}
      {isLoading}
      {verifiedAlgorithm}
      onVerify={handleVerify}
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

  .verifier-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-top: 2rem;
    align-items: start;
  }

  .left-column {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  @media (max-width: 900px) {
    .verifier-layout {
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
