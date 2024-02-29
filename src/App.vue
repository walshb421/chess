<script setup>
import { ref } from 'vue';
import { useWebSocket } from '@vueuse/core'

const { status, data, send, open, close } = useWebSocket('ws://localhost:9090')

// Make structure to send move
const startMove = ref('');
const endMove = ref('');

// method that constructs a string 
const sendMove = () => {
  const move = `${startMove.value} to ${endMove.value}`
  send(move)
  startMove.value = '' // resets value
  endMove.value = '' // reset value
}

</script>

<template>
  <h1>Example Chess App</h1>
  <p>Status: {{ status }}</p>
  <p>Data: {{ data }}</p>
  <div>
    <input v-model="startMove" placeholder="Start Move (e.g., e2)">
    <input v-model="endMove" placeholder="End Move (e.g., e6)">
    <button @click="sendMove">Send Move</button>
  </div>
  <button @click="send('hello world')">Hello World</button>
</template>
