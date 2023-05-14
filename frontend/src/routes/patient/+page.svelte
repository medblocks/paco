<script lang="ts">
  import {
    TextInput,
    Button,
    Tile,
    Form,
    TextInputSkeleton,
  } from "carbon-components-svelte";
  import SendFilled from "carbon-icons-svelte/lib/SendFilled.svelte";
  import Monster from "carbon-icons-svelte/lib/Monster.svelte";
  import { DoctorSocket } from "../../types";
  import { onDestroy } from "svelte";
  import { MicrophoneFilled } from "carbon-icons-svelte";

  let value = "";
  let renderAudioText = "";
  let audioData: any[] = [];
  let streamingMedia = false;

  let x: {
    message?: string;
    type: "patient" | "bot";
    audio?: HTMLAudioElement;
  }[] = [
    {
      message:
        "Hello I'm Paco, your medical knowledge assistant ask me any questions about your prescription or your condition",
      type: "bot",
    },
  ];

  DoctorSocket.connect();
  DoctorSocket.emit("patient_mode", true);

  interface IContent {
    text: string;
    done: boolean;
    audio: any;
  }

  DoctorSocket.on("patient_message", (content: IContent) => {
    console.log(content);
    if (x[x.length - 1].type === "bot") {
      x = [...x.slice(0, x.length - 1), { message: content.text, type: "bot" }];
    } else {
      x = [...x, { message: content.text, type: "bot" }];
    }

    if (content.done) {
      streamingMedia = true;
      audioData.push(content.audio);
      const audioBlob = new Blob(audioData, { type: "audio/mp3" });
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      x = [
        ...x.slice(0, x.length - 1),
        { message: content.text, type: "bot", audio: audio },
      ];
      streamingMedia = false;
      audioData = [];
    }
  });

  DoctorSocket.on("patient_transcript", (text) => {
    console.log(text);
    // x = [...x, { message: text, type: "patient" }];
    // DoctorSocket.emit("patient_message", text);
    value = value + " " + text;
  });

  const postMessage = () => {
    x = [...x, { message: value, type: "patient" }];
    DoctorSocket.emit("patient_message", value);
    value = "";
  };

  let recording = false;

  const toggleRecording = () => {
    if (recording) {
      recording = false;
      DoctorSocket.emit("patient_recording", false);
    } else {
      recording = true;
      DoctorSocket.emit("patient_recording", true);
    }
  };

  onDestroy(() => {
    DoctorSocket.emit("patient_mode", false);
    DoctorSocket.disconnect();
  });
</script>

<div class="h-[93vh] flex flex-col bg-repeat bg-x relative">
  <div class="flex flex-col gap-y-3 mb-22 lg:w-[60%] mx-auto overflow-y-scroll">
    {#each x as y}
      <div
        class="flex {y.type === 'patient' ? 'flex-row-reverse' : 'flex-row'}"
      >
        {#if y.type !== "patient"}
          <div class="rounded-full bg-dark-400">
            <Monster size={32} class="block m-auto" />
          </div>
        {/if}
        <Tile
          class="w-[60%] rounded-md shadow-sm {y.type === 'patient'
            ? 'ml-auto'
            : 'mr-auto'}"
        >
          {#if y.audio}
            <audio controls src={y.audio.src} />
          {/if}
          {#if y.message}
            <p>{y.message}</p>
          {/if}
        </Tile>
      </div>
    {/each}
  </div>

  <div class="flex absolute bottom-1 w-full px-6 py-3 bg-dark-600">
    <Button
      type="submit"
      on:click={toggleRecording}
      kind={recording ? "danger" : "ghost"}
      icon={MicrophoneFilled}
      size="xl"
    />
    <Form on:submit={postMessage} class=" w-full flex">
      {#if !streamingMedia}
        <TextInput
          size="xl"
          hideLabel
          labelText="User name"
          placeholder="Ask your questions here"
          bind:value
          autofocus
        />
      {:else}
        <TextInputSkeleton hideLabel />
      {/if}
      <Button type="submit" kind="ghost" icon={SendFilled} size="xl" />
    </Form>
  </div>
</div>

<style>
  .bg-x {
    background-image: url("/bg.svg");
  }
</style>
