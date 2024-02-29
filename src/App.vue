<script setup>
import { ref, watch } from 'vue';
import { useWebSocket } from '@vueuse/core'

const { status, data, send, open, close } = useWebSocket('ws://localhost:9090')

// Make structure to send move
const startMove = ref('');
const endMove = ref('');
const chessboard = ref([])

watch(data, (newData) => {
  // When data changes, update chessboard
  chessboard.value = JSON.parse(newData)
})

// method that constructs the move string 
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
  <table class="chessboard">
    <tr v-for="(row, rowIndex) in chessboard" :key="rowIndex">
      <th>{{ 8 - rowIndex }}</th>
      <td v-for="(cell, cellIndex) in row" :key="cellIndex">
        {{ cell }}
      </td>
    </tr>
    <tr>
      <th></th> 
      <th v-for="colLabel in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']" :key="colLabel">
        {{ colLabel }}
      </th>
    </tr>
  </table>
  <div>
    <input v-model="startMove" placeholder="Start Move (e.g., e2)">
    <input v-model="endMove" placeholder="End Move (e.g., e6)">
    <button @click="sendMove">Send Move</button>
  </div>
</template>
