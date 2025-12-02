<script lang="ts">
  import { Heart } from "lucide-svelte";

  const currentYear = new Date().getFullYear();
</script>

<footer class="footer">
  <div class="footer-content">
    <p class="copyright">
      {currentYear}
      <span class="separator">•</span>
      Artifice
    </p>

    <div class="credits">
      <span class="powered-by">
        Powered by <a
          href="https://svelte.dev/"
          target="_blank"
          rel="noreferrer">Svelte</a
        >
      </span>
      <span class="separator">•</span>
      <span class="inspired-by">
        Inspired by <a
          href="https://m3.material.io/"
          target="_blank"
          rel="noreferrer">Material You</a
        >
      </span>
    </div>
  </div>
</footer>

<style>
  .footer {
    margin-top: auto;
    padding: 2rem 1rem;
    border-top: 1px solid var(--md-sys-color-outline-variant);
    color: var(--md-sys-color-on-surface-variant);
    font-size: 0.875rem;
  }

  .footer-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin: 0 auto;
    max-width: 1200px;
    gap: 0.5rem;
  }

  .credits {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .separator {
    color: var(--md-sys-color-outline);
  }

  a {
    color: inherit;
    text-decoration: none;
    border-bottom: 1px dotted var(--md-sys-color-outline);
    transition:
      0.2s,
      border-color 0.2s;
  }

  a:hover {
    color: var(--md-sys-color-primary);
    border-color: var(--md-sys-color-primary);
  }

  @media (min-width: 600px) {
    .footer-content {
      flex-direction: row;
      justify-content: space-between;
      text-align: left;
    }
  }
</style>
