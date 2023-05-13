<script lang="ts">
  import AiNotes from "$lib/AINotes.svelte";
  import Summary from "$lib/Summary.svelte";
  import { onDestroy } from "svelte";
  import Transcription from "../../lib/Transcription.svelte";
  import { DoctorSocket } from "../../types";

  DoctorSocket.connect();

  onDestroy(() => {
    DoctorSocket.disconnect();
  });
</script>

<div class="flex justify-around gap-x-2 h-[90vh] mx-15">
  <div class="w-1/2 h-full flex flex-col gap-y-3">
    <div class="h-1/2">
      <AiNotes />
    </div>
    <div class="h-1/2">
      <Transcription />
    </div>
  </div>
  <div class="w-1/2 h-full">
    <Summary />
  </div>
</div>
