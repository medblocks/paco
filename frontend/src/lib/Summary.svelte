<script lang="ts">
  import { page } from "$app/stores";
  import { Tile, TextArea, Button, ButtonSet } from "carbon-components-svelte";
  import ArrowRight from "carbon-icons-svelte/lib/ArrowRight.svelte";
</script>

<div class="w-full flex flex-col justify-start">
  <Tile class="block">
    <p class="text-lg">Clinical Notes</p>
  </Tile>

  <TextArea
    hideLabel
    placeholder="Fever since 3 days....."
    class="mt-2 block"
    rows={30}
  />
  <ButtonSet class="flex justify-end">
    <Button
      on:click={() => {
        location.reload();
      }}
      kind="danger"
      class="mt-2 block">Reset</Button
    >
    <Button icon={ArrowRight} class="mt-2 block">Save</Button>
  </ButtonSet>

  <div />
</div>
