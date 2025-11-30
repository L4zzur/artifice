<script lang="ts">
  import { page } from "$app/state";
  import {
    House,
    QrCode,
    ChevronDown,
    ChevronRight,
    CirclePlus,
    Scan,
    KeyRound,
    ShieldPlus,
    ShieldCheck,
    CircleCheckBig,
    Sparkles,
    Fingerprint,
  } from "lucide-svelte";

  interface MenuItem {
    name: string;
    href: string;
    icon: any;
    children?: ChildMenuItem[];
  }

  interface ChildMenuItem {
    name: string;
    path: string;
    icon: any;
  }

  const menuItems: MenuItem[] = [
    {
      name: "Home",
      href: "/",
      icon: House,
    },
    {
      name: "QR Code",
      icon: QrCode,
      href: "/qr",
      children: [
        { name: "Generator", path: "generate", icon: CirclePlus },
        { name: "Scanner", path: "scan", icon: Scan },
      ],
    },
    {
      name: "Password",
      icon: KeyRound,
      href: "/password",
      children: [
        { name: "Generator", path: "generate", icon: ShieldPlus },
        { name: "Analyzer", path: "analyze", icon: ShieldCheck },
      ],
    },
    {
      name: "Hash",
      icon: Fingerprint,
      href: "/hash",
      children: [
        { name: "Generator", path: "generate", icon: Sparkles },
        { name: "Verifier", path: "verify", icon: CircleCheckBig },
      ],
    },
  ];

  let openFolders = $state<Set<number>>(new Set());

  function toggleFolder(index: number) {
    const newSet = new Set(openFolders);
    if (newSet.has(index)) {
      newSet.delete(index);
    } else {
      newSet.add(index);
    }
    openFolders = newSet;
  }

  function getChildHref(parentHref: string, childPath: string): string {
    return `${parentHref}/${childPath}`;
  }

  function isFolderActive(parentHref: string): boolean {
    return (
      page.url.pathname.startsWith(parentHref) &&
      page.url.pathname !== parentHref
    );
  }
</script>

<nav class="sidebar">
  <div class="sidebar-header">
    <h2>Artifice</h2>
  </div>

  <ul class="sidebar-menu">
    {#each menuItems as item, index}
      {#if item.children}
        <li class="sidebar-folder">
          <!-- Папка -->
          <div class="sidebar-folder-header">
            <!-- Сссылка на папку-->
            <a
              href={item.href}
              class="sidebar-item sidebar-folder-link {page.url.pathname ===
                item.href || isFolderActive(item.href)
                ? 'active'
                : ''}"
            >
              <span class="sidebar-icon">
                <item.icon size={20} strokeWidth={2} />
              </span>
              <span class="sidebar-name">{item.name}</span>
            </a>

            <button
              class="sidebar-folder-toggle"
              onclick={() => toggleFolder(index)}
              aria-label="Toggle folder"
            >
              {#if openFolders.has(index)}
                <ChevronDown size={16} strokeWidth={2} />
              {:else}
                <ChevronRight size={16} strokeWidth={2} />
              {/if}
            </button>
          </div>

          <!-- Содержимое папки -->
          {#if openFolders.has(index)}
            <ul class="sidebar-submenu">
              {#each item.children as child}
                {@const childHref = getChildHref(item.href, child.path)}
                {@const ChildIcon = child.icon}

                <li>
                  <a
                    href={childHref}
                    class="sidebar-item sidebar-submenu-item {page.url
                      .pathname === childHref
                      ? 'active'
                      : ''}"
                  >
                    {#if ChildIcon}
                      <!-- Рендерим только если иконка существует -->
                      <span class="sidebar-icon">
                        <ChildIcon size={18} strokeWidth={2}></ChildIcon>
                      </span>
                    {:else}
                      <!-- Пустой placeholder для сохранения отступа -->
                      <span class="sidebar-icon"></span>
                    {/if}
                    <span class="sidebar-name">{child.name}</span>
                  </a>
                </li>
              {/each}
            </ul>
          {/if}
        </li>
      {:else}
        <li>
          <a
            href={item.href}
            class="sidebar-item {page.url.pathname === item.href
              ? 'active'
              : ''}"
          >
            <span class="sidebar-icon">
              <item.icon size={20} strokeWidth={2} />
            </span>
            <span class="sidebar-name">{item.name}</span>
          </a>
        </li>
      {/if}
    {/each}
  </ul>
</nav>

<style>
  .sidebar {
    width: 280px;
    background: rgba(30, 30, 41, 0.6);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-right: 1px solid var(--md-sys-color-outline-variant);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    padding: 1.5rem 0;
  }

  .sidebar-header {
    padding: 0 1.5rem 1.5rem;
    border-bottom: 1px solid var(--md-sys-color-outline-variant);
  }

  .sidebar-header h2 {
    font-size: 1.5rem;
    color: var(--md-sys-color-primary);
    font-weight: 600;
    letter-spacing: 0.5px;
  }

  .sidebar-menu {
    list-style: none;
    padding: 1rem 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .sidebar-folder {
    display: flex;
    flex-direction: column;
  }

  .sidebar-folder-header {
    display: flex;
    align-items: center;
    position: relative;
  }

  .sidebar-folder-link {
    flex: 1;
    padding-right: 2.5rem;
  }

  .sidebar-folder-toggle {
    position: absolute;
    right: 0.5rem;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    color: var(--md-sys-color-on-surface-variant);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--md-sys-shape-corner-small);
    transition: all var(--md-sys-animation-standard);
    z-index: 1;
  }

  .sidebar-folder-toggle:hover {
    background: rgba(176, 196, 222, 0.15);
    color: var(--md-sys-color-primary);
  }

  .sidebar-submenu {
    list-style: none;
    padding: 0;
    margin: 0.25rem 0 0.5rem 0;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .sidebar-submenu-item {
    margin-left: 1rem;
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }

  .sidebar-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.875rem 1rem;
    border-radius: var(--md-sys-shape-corner-medium);
    color: var(--md-sys-color-on-surface-variant);
    text-decoration: none;
    transition: all var(--md-sys-animation-standard);
    position: relative;
    border: 1px solid transparent;
  }

  .sidebar-item:hover {
    background: rgba(176, 196, 222, 0.1);
    color: var(--md-sys-color-primary);
    transform: translateX(4px);
    border: 1px solid rgba(176, 196, 222, 0.2);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  .sidebar-item.active {
    background: rgba(176, 196, 222, 0.18);
    color: var(--md-sys-color-primary);
    border: 1px solid rgba(176, 196, 222, 0.33);
    box-shadow: 0 2px 12px rgba(176, 196, 222, 0.18);
    font-weight: 600;
    transform: none;
  }

  .sidebar-icon {
    font-size: 1.25rem;
    width: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .sidebar-name {
    font-size: 0.95rem;
    font-weight: 500;
  }
</style>
