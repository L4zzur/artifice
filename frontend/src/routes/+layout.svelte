<script lang="ts">
  import { page } from "$app/stores";
  import favicon from "$lib/assets/favicon.svg";
  import Sidebar from "$lib/components/Sidebar.svelte";
  import "$lib/styles/theme.css";

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />

  {#if $page.data.meta}
    <title>{$page.data.meta.title}</title>
    <meta name="description" content={$page.data.meta.description} />
  {/if}
</svelte:head>

<div class="app-layout">
  <Sidebar />

  <main>
    {@render children()}
  </main>
</div>

<style>
  .app-layout {
    display: flex;
    min-height: 100vh;
    background:
      radial-gradient(
        circle at 20% 30%,
        rgba(106, 90, 205, 0.15),
        transparent 50%
      ),
      radial-gradient(
        circle at 70% 70%,
        rgba(168, 84, 194, 0.1),
        transparent 50%
      ),
      var(--md-sys-color-background);
  }

  main {
    flex: 1;
    padding: 2rem;
  }
</style>
