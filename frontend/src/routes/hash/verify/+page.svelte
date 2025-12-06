<script lang="ts">
  import {
    type SchemasHashOutputFormat,
    type HashAlgorithm,
    type HashVerifyRequest,
  } from "$lib/api/generated";
  import { verifyHash, hashFile } from "$lib/api/hash";
  import type { HashFileRequest } from "$lib/api/generated";
  import HashSettingsPanel from "$lib/components/hash/HashSettingsPanel.svelte";
  import HashInputPanel from "$lib/components/hash/HashInputPanel.svelte";
  import HashVerifyResultPanel from "$lib/components/hash/verifier/HashVerifyResultPanel.svelte";
  import PageHeader from "$lib/components/ui/PageHeader.svelte";
  import Toast from "$lib/components/ui/Toast.svelte";
  import { CircleCheckBig, CircleX } from "lucide-svelte";
  import ExpectedHashInput from "$lib/components/hash/verifier/ExpectedHashInput.svelte";
  import ErrorBanner from "$lib/components/ui/ErrorBanner.svelte";

  type InputMode = "text" | "file";

  let inputMode = $state<InputMode>("text");
  let inputData = $state("");
  let uploadedFile = $state<File | null>(null);
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

  function fileToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        resolve(result);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  async function handleVerifyFromText() {
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
        algorithm,
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

  async function handleVerifyFromFile() {
    if (!uploadedFile) {
      isValid = null;
      verifiedAlgorithm = null;
      error = "Please upload a file and enter expected hash";
      return;
    }

    const hashTrimmed = expectedHash.trim();
    if (!hashTrimmed) {
      isValid = null;
      verifiedAlgorithm = null;
      error = "Please enter expected hash";
      return;
    }

    isLoading = true;
    error = null;
    isValid = null;
    verifiedAlgorithm = null;

    try {
      const base64 = await fileToBase64(uploadedFile);

      const fileReq: HashFileRequest = {
        file_base64: base64,
        algorithm,
        output_format: outputFormat,
      };

      const fileHashResult = await hashFile(fileReq);

      const verifyReq: HashVerifyRequest = {
        data: "",
        expected_hash: hashTrimmed,
        algorithm,
        hmac_key: hmacKey || null,
        output_format: outputFormat,
      };

      const valid = fileHashResult.hash === hashTrimmed;
      isValid = valid;
      verifiedAlgorithm = algorithm;
    } catch (e) {
      if (e instanceof Error) {
        error = e.message;
      } else {
        error = "An unexpected error occurred";
      }
      console.error("File verify error:", e);
    } finally {
      isLoading = false;
    }
  }

  async function handleVerify() {
    if (inputMode === "text") {
      await handleVerifyFromText();
    } else {
      await handleVerifyFromFile();
    }
  }

  function handleModeChange(mode: InputMode) {
    inputMode = mode;
    isValid = null;
    error = null;
  }

  function handleFileSelect(file: File | null) {
    uploadedFile = file;
    isValid = null;
    error = null;
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

  <ErrorBanner message={error} onDismiss={() => (error = null)} />

  <div class="verifier-layout">
    <div class="left-column">
      <HashInputPanel
        bind:inputData
        bind:uploadedFile
        bind:inputMode
        onModeChange={handleModeChange}
        onFileSelect={handleFileSelect}
        onError={handleFileError}
        textLabel={inputMode === "text" ? "Data to verify" : "File to verify"}
        textPlaceholder="Original data to verify..."
        textRows={2}
        maxFileSizeMB={15}
      />

      <ExpectedHashInput bind:expectedHash />

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
    gap: 1rem;
  }

  @media (max-width: 900px) {
    .verifier-layout {
      grid-template-columns: 1fr;
    }
  }
</style>
