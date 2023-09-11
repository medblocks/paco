<script lang="ts">
  import AiNotes from "$lib/AINotes.svelte";
  import Summary from "$lib/Summary.svelte";
  import Transcription from "../../lib/Transcription.svelte";

  
</script>

<div class="flex justify-around gap-x-2 h-[90vh] mx-15">
  <div class="w-2/3 h-full flex flex-col gap-y-3">
    <div class="h-2/3">
      <AiNotes />
    </div>
    <div class="h-1/3">
      <Transcription />
    </div>
  </div>
  <div class="w-1/3 h-full">
    <Summary />
  </div>
</div>
