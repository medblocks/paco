<script lang="ts">
  import { Tile, Content } from "carbon-components-svelte";
  import SvelteMarkdown from "svelte-markdown";
  import CircleDash from "carbon-icons-svelte/lib/CircleDash.svelte";

  import { DoctorSocket, type TranscriptMessage } from "../types";
  import { onDestroy, onMount } from "svelte";

  let live =
    "**lorem ipsum**:  dolor sit amet, consectetur adipiscing elit. sed ut tellusut nisl aliquam aliquam.";
  let loading = false;

  onMount(async () => {
    DoctorSocket.on("connect", () => {
      console.log("connected to socket");
    });

    DoctorSocket.on("transcript", (x) => {
      console.log(x);
      loading = true;
      live = x.replaceAll("\n", "\n\n");
    });
  });

</script>

<div
  class="h-full border-2 border-gray-600 border-solid flex flex-col overflow-x-hidden"
>
  <Tile class="w-full flex justify-between">
    <p class="text-lg">Your conversation with [Patient Name]</p>
    <CircleDash
      class="w-6 h-6 block  {loading && 'animate-duration-[1s] animate-pulse'}"
    />
  </Tile>

  <Content class="overflow-y-scroll" >
    <SvelteMarkdown source={live} />
  </Content>
</div>
