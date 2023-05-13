<script lang="ts">
  import AiNotes from "$lib/AINotes.svelte";
  import Summary from "$lib/Summary.svelte";
  import Transcription from "../../lib/Transcription.svelte";
</script>

<div class="flex justify-around gap-x-2 h-[90vh]">
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
