<script lang="ts">
  import "carbon-components-svelte/css/g80.css";
  import "virtual:uno.css";
  import Nav from "$lib/Nav.svelte";
  export const ssr = false;

</script>

<Nav />
<div class="mt-15" >
  <slot />
</div>

