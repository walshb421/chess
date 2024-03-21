<script setup>

import { ref, watch, onMounted } from 'vue';
import { useWebSocket } from '@vueuse/core'
import Board from './components/Board.vue';


const { status, data, send, open, close } = useWebSocket('ws://localhost:9090')

// Different chess data
const startMove = ref('');
const endMove = ref('');
const chessboard = ref(null);
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
  const message = {
    "move": {
      source: startMove.value,
      destination: endMove.value
    }
  }
  send(JSON.stringify(message));
  startMove.value = null // resets value
  endMove.value = null // reset value

}

watch(endMove, (square) => {
  if(square) {
    sendMove()
  }
})

onMounted(() => {
  send(JSON.stringify({"connect": {}}))
});

</script>

<template>
  <h1>Example Chess App</h1>
  
  <p>Status: {{ status }}</p>

  <Board :board="chessboard" v-model:source="startMove" v-model:destination="endMove"/>

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
