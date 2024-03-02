<script setup>

import { ref, watch } from 'vue';
import { useWebSocket } from '@vueuse/core'
import Board from './components/Board.vue';


const { status, data, send, open, close } = useWebSocket('ws://localhost:9090')

// Different chess data
const startMove = ref('');
const endMove = ref('');
const chessboard = ref([]);
const capturedWhite = ref([]);
const capturedBlack = ref([]);


chessboard.value = new Array(8).fill(
  new Array(8).fill(".")
);

watch(data, (newData) => {
  // When data changes, update game info
  const parsedData = JSON.parse(newData)
  console.log(parsedData);
  chessboard.value = parsedData.board;
  capturedWhite.value = parsedData.captured_white;
  capturedBlack.value = parsedData.captured_black;
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

  
  <div>
    <input v-model="startMove" placeholder="Start Move (e.g., e2)">
    <input v-model="endMove" placeholder="End Move (e.g., e6)">
    <button @click="sendMove">Send Move</button>
  </div>
  
  <Board :board="chessboard"/>

  <!-- Captured Black Pieces -->
  <div class="captured-pieces">
      <h2>Captured Black Pieces</h2>
      <ul>
        <li v-for="(piece, index) in capturedBlack" :key="index">
          {{ piece }}
        </li>
      </ul>
  </div>
  
  <!-- Captured White Pieces -->
    <div class="captured-pieces">
      <h2>Captured White Pieces</h2>
      <ul>
        <li v-for="(piece, index) in capturedWhite" :key="index">
          {{ piece }}
        </li>
      </ul>
    </div>
</template>
