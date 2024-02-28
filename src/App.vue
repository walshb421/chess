<script setup>
import { useWebSocket } from '@vueuse/core'

const { status, data, send, open, close } = useWebSocket('ws://localhost:9090')

</script>

<template>
  <h1>Example Chess App</h1>
  <p>Status: {{ status }}</p>
  <p>Data: {{ data }}</p>
  <button @click="send('hello world')">Hello World</button>
</template>
