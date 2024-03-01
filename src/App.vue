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


watch(data, (newData) => {
  // When data changes, update game info
  const parsedData = JSON.parse(newData)

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

  <!-- Chessboard Representation -->
  <table class="chessboard">
    <tr v-for="(row, rowIndex) in chessboard" :key="rowIndex">
      <!-- Show the row numbers -->
      <th>{{ 8 - rowIndex }}</th>
      <td v-for="(cell, cellIndex) in row" :key="cellIndex">
        {{ cell }}
      </td>
    </tr>
    <tr>
      <!-- Show the column letters -->
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

  
  <Board />
</template>
