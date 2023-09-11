<script lang="ts">
  import { page } from "$app/stores";
  import { Button, Header, HeaderNav, HeaderNavItem } from "carbon-components-svelte";
  import { DoctorSocket, connected } from "../types";
  let isSideNavOpen = false;

  let running = false

  const stopMic = ()=>{
    DoctorSocket.emit("stop_recording", undefined, (value: boolean)=>{
      if (value) {
        running = false
      }
    })
  }

  const startMic = ()=> {
    DoctorSocket.emit("start_recording", undefined, (value: boolean)=>{
      if (value) {
        running = true
      }
    })
  }
</script>

<Header company="Paco" platformName="Doc" bind:isSideNavOpen>
  {#if $connected}
    {#if running}
    <Button on:click={stopMic} kind="danger">Stop</Button>  
    {:else}
    <Button on:click={startMic}>Start</Button>  
    {/if}
  {:else}
  <Button on:click={stopMic} disabled>Not connected</Button>  
  {/if}
  
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
