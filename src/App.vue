<script setup>
import { ref } from 'vue';

import Splash from '@/components/Splash.vue';
import Board from '@/components/Board.vue';
import Debug from '@/components/Debug.vue';
import Chat from '@/components/Chat.vue'
import Jail from '@/components/Jail.vue'

import { useChess } from '@/composables/chess.js';


const turn = ref(-1);





const start_game = () => {
  turn.value = 0;
}

const { connect } = useChess();

const connection = connect();

</script>

<template>

  <Splash v-if="turn < 0" :start="start_game"/>
  <div v-else>
     <h1>Example Chess App</h1>

      <Board />

      <Chat />
      
      <Jail />

      <Debug />

    </div>
       
</template>
