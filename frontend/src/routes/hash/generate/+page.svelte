<script lang="ts">
  import {
    type SchemasHashOutputFormat,
    type HashAlgorithm,
    type HashGenerateRequest,
    type HashFileRequest,
  } from "$lib/api/generated";
  import { generateHash, hashFile } from "$lib/api/hash";
  import HashInputPanel from "$lib/components/hash/HashInputPanel.svelte";
  import HashResultPanel from "$lib/components/hash/generator/HashResultPanel.svelte";
  import HashSettingsPanel from "$lib/components/hash/HashSettingsPanel.svelte";
  import PageHeader from "$lib/components/ui/PageHeader.svelte";
  import Toast from "$lib/components/ui/Toast.svelte";
  import { CircleX, Sparkles } from "lucide-svelte";

  type InputMode = "text" | "file";

  let inputMode = $state<InputMode>("text");
  let inputData = $state("");
  let uploadedFile = $state<File | null>(null);

  let algorithm = $state<HashAlgorithm>("sha256");
  let outputFormat = $state<SchemasHashOutputFormat>("hex");
  let hmacKey = $state("");
  let generatedHash = $state<string | null>(null);

  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let toastMessage = $state<string | null>(null);
  let toastTimeout: ReturnType<typeof setTimeout> | null = null;

  let debounceTimer: ReturnType<typeof setTimeout> | null = null;

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

  async function handleGenerateFromText() {
    if (!inputData.trim()) {
      generatedHash = null;
      error = "Please enter data";
      return;
    }

    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }

    debounceTimer = setTimeout(async () => {
      if (generatedHash) {
        isLoading = true;
      }

      error = null;

      try {
        const request: HashGenerateRequest = {
          data: inputData,
          algorithm: algorithm,
          output_format: outputFormat,
          hmac_key: hmacKey || null,
        };

        const result = await generateHash(request);
        generatedHash = result.hash;
      } catch (e) {
        if (e instanceof Error) {
          error = e.message;
        } else {
          error = "An unexpected error occurred";
        }
        console.error("Hash generation error:", e);
      } finally {
        isLoading = false;
      }
    }, 300);
  }

  async function handleGenerateFromFile() {
    if (!uploadedFile) {
      generatedHash = null;
      error = null;
      return;
    }

    isLoading = true;
    error = null;

    try {
      const base64 = await fileToBase64(uploadedFile);

      const request: HashFileRequest = {
        file_base64: base64,
        algorithm: algorithm,
        output_format: outputFormat,
      };

      const result = await hashFile(request);
      generatedHash = result.hash;
    } catch (e) {
      if (e instanceof Error) {
        error = e.message;
      } else {
        error = "An unexpected error occurred";
      }
      console.error("File hash error:", e);
    } finally {
      isLoading = false;
    }
  }

  async function handleGenerate() {
    if (inputMode === "text") {
      await handleGenerateFromText();
    } else {
      await handleGenerateFromFile();
    }
  }

  function handleModeChange(mode: InputMode) {
    inputMode = mode;
    generatedHash = null;
    error = null;
  }

  function handleFileSelect(file: File | null) {
    uploadedFile = file;
    if (file) {
      handleGenerate();
    } else {
      generatedHash = null;
    }
  }

  async function handleCopy() {
    if (!generatedHash) return;

    try {
      await navigator.clipboard.writeText(generatedHash);
      showToast("Hash copied to clipboard");
    } catch (e) {
      console.error("Failed to copy hash.");
      showToast("Failed to copy hash");
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
    inputData;
    algorithm;
    outputFormat;
    hmacKey;

    if (inputData.trim()) {
      handleGenerate();
    } else {
      generatedHash = null;
      error = null;
    }
  });
</script>

<div class="page-container">
  <PageHeader
    title="Hash Generator"
    description="Generate cryptographic hashes with optional HMAC authentication"
    backLink={{ href: "/hash", label: "Back to Hash Tools" }}
  >
    {#snippet icon()}
      <Sparkles size={48} strokeWidth={1.7} />
    {/snippet}
  </PageHeader>

  {#if error}
    <div class="error-message">
      <CircleX size={18} />
      {error}
    </div>
  {/if}

  <div class="generator-layout">
    <div class="left-column">
      <HashInputPanel
        bind:inputData
        bind:uploadedFile
        bind:inputMode
        onModeChange={handleModeChange}
        onFileSelect={handleFileSelect}
        textLabel="Data to hash"
        textPlaceholder="Hello, World!"
        textRows={2}
        maxFileSizeMB={15}
      />

      <HashSettingsPanel bind:algorithm bind:outputFormat bind:hmacKey />
    </div>

    <HashResultPanel hash={generatedHash} onCopy={handleCopy} />
  </div>

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
    .generator-layout {
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
