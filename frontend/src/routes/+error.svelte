<script lang="ts">
  import { page } from "$app/stores";
  import { AlertTriangle } from "lucide-svelte";
</script>

<div class="error-page">
  <div class="error-content">
    <AlertTriangle size={64} />
    <h1>Oops! Something went wrong</h1>
    <p>{$page.error?.message || "An unexpected error occurred"}</p>
    <a href="/" class="button">Go back home</a>
  </div>
</div>

<style>
  .error-page {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 2rem;
  }

  .error-content {
    text-align: center;
    max-width: 500px;
  }

  h1 {
    margin: 1rem 0;
    color: var(--md-sys-color-error);
  }

  .button {
    display: inline-block;
    margin-top: 2rem;
    padding: 0.875rem 1.5rem;
    background: var(--md-sys-color-primary);
    color: var(--md-sys-color-on-primary);
    text-decoration: none;
    border-radius: var(--md-sys-shape-corner-medium);
  }
</style>
