<script lang="ts">
  import { TextInput, Button, Tile, Form } from "carbon-components-svelte";
  import SendFilled from "carbon-icons-svelte/lib/SendFilled.svelte";
  import Monster from "carbon-icons-svelte/lib/Monster.svelte";
  import { DoctorSocket } from "../../types";
  import { onDestroy } from "svelte";

  let value = "";
  let x = [
    {
      message: "Hello, I am a message",
      type: "patient",
    },
    {
      message:
        "Hello I'm Paco, your medical knowledge assistant ask me any questions about your prescription or your condition",
      type: "bot",
    },
  ];

  DoctorSocket.connect();

  interface IContent {
    text: string;
    done: boolean;
  }

  DoctorSocket.on("patient_message", (content: IContent) => {
    if(x[x.length - 1].type === "bot"){
      x = [...x.slice(0, x.length - 1), { message: content.text, type: "bot" }];
    }else{
      x = [...x, { message: content.text, type: "bot" }];
    };
  });

  DoctorSocket.on("patient_transcript", (text)=>{
    value = text
  })

  const postMessage = () => {
    x = [...x, { message: value, type: "patient" }];
    DoctorSocket.emit("patient_message", value);
    value = "";
  };

  let recording = false
  
  const toggleRecording = () => {
    recording = !recording
    DoctorSocket.emit('patient_mode', recording)
  }

  onDestroy(() => {
    DoctorSocket.disconnect();
  });

</script>

<div class="h-[93vh] flex flex-col bg-repeat bg-x relative">
  <div class="flex flex-col gap-y-3 mb-22 lg:w-[60%] mx-auto">
    {#each x as y}
      <div
        class="flex {y.type === 'patient' ? 'flex-row-reverse' : 'flex-row'}"
      >
        {#if y.type !== "patient"}
        <div class="rounded-full bg-dark-400" >
          <Monster size={32} class="block m-auto" />
        </div>
        {/if}
        <Tile
          class="max-w-[80%] min-w-[45%] rounded-md shadow-sm {y.type === 'patient'
            ? 'ml-auto'
            : 'mr-auto'}"
        >
          <p>{y.message}</p>
        </Tile>
      </div>
    {/each}
  </div>

  <Form class="px-6 py-3 bg-dark-600 w-full absolute bottom-1 flex">
    <TextInput
      size="xl"
      hideLabel
      labelText="User name"
      placeholder="Ask your questions here"
      bind:value
      autofocus
    />
    <Button
      type="submit"
      on:click={postMessage}
      kind="ghost"
      icon={SendFilled}
      size="xl"
    />
    <Button
      type="submit"
      on:click={toggleRecording}
      kind="ghost"
      icon={SendFilled}
      size="xl"
    />
  </Form>
</div>

<style>
  .bg-x {
    background-image: url("/bg.svg");
  }
</style>
