<script lang="ts">
  import { Tile, Content } from "carbon-components-svelte";
  import { onMount } from "svelte";
  import { DoctorSocket } from "../types";
  import SvelteMarkdown from "svelte-markdown";

  let live = "";

  onMount(async () => {

    DoctorSocket.on("connect", () => {
      console.log("connected to socket");
    });

    DoctorSocket.on("ai_note", (x) => {
      console.log(x);
      live = x.replaceAll("\n", "\n\n");
    });
  });
</script>

<div class="h-full w-full flex flex-col border-2 border-gray-600 border-solid">
  <Tile>
    <p class="text-lg">AI Helper</p>
  </Tile>
  <Content class="overflow-y-scroll">
    <SvelteMarkdown source={live} />
  </Content>
</div>
