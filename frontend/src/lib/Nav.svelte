<script>
  import { page } from "$app/stores";
  import { Header, HeaderNav, HeaderNavItem } from "carbon-components-svelte";

  let isSideNavOpen = false;
</script>

<Header company="Paco" platformName="Doc" bind:isSideNavOpen>
  <HeaderNav>
    <HeaderNavItem
      isSelected={$page.url.pathname === "/doctor" ? true : false}
      href="/doctor"
      text="Doctor companion"
    />
    <HeaderNavItem
      isSelected={$page.url.pathname === "/patient" ? true : false}
      href="/patient"
      text="Patient companion"
    />
  </HeaderNav>
</Header>
