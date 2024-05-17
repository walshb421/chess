<script setup>

import Splash from '@/components/Splash.vue';
import Board from './components/Board.vue';
import Piece from './components/Piece.vue';
import { useChess } from './composables/chess.js';

const turn = ref(-1);





const start_game = () => {
  turn.value = 0;
}

const { captured_black, captured_white, connect, reset} = useChess();
const connection = connect();

</script>

<template>
  <Splash v-if="turn < 0" :start="start_game"/>
  <div v-else>
     <h1>Example Chess App</h1>
  
  <p>Status: {{ connection }}</p>
  <button @click="reset()">Reset</button>

  <Board />
   
  <!-- Captured Black Pieces -->
  
  <h2>Captured Black Pieces</h2>
  <div class="captured-pieces">
      <Piece v-for="(piece, index) in captured_black"
          :piece="piece"
          class="board-piece"
      />
  </div>

  
  <!-- Captured White Pieces -->
    
  <h2>Captured White Pieces</h2>
  <div class="captured-pieces">
      <Piece v-for="(piece, index) in captured_white"
          :piece="piece"
          class="board-piece"
      />
  </div>
    
</template>
