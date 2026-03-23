<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

import Splash from '@/components/Splash.vue';
import Board from '@/components/Board.vue';
import Debug from '@/components/Debug.vue';
import Chat from '@/components/Chat.vue'
import Jail from '@/components/Jail.vue'
import DebugPanel from '@/components/DebugPanel.vue'

import { useChess } from '@/composables/chess.js';


const turn = ref(-1);
const showDebugPanel = ref(false);

const start_game = () => {
  turn.value = 0;
}

const { connect } = useChess();

const connection = connect();

// Toggle debug panel with 'D' key
const handleKeydown = (event) => {
  if (event.key === 'd' || event.key === 'D') {
    // Don't toggle if user is typing in an input
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
      return;
    }
    showDebugPanel.value = !showDebugPanel.value;
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
});
</script>

<template>

  <Splash v-if="turn < 0" :start="start_game"/>
  <div v-else class="game-container">
    <h1>Example Chess App</h1>
    
    <div class="game-layout">
      <div class="main-content">
        <Board />
        <Chat />
        <Jail />
        <Debug />
      </div>
      
      <div class="debug-sidebar" v-if="showDebugPanel">
        <DebugPanel />
      </div>
    </div>
    
    <p class="debug-hint">Press 'D' to toggle debug panel</p>
  </div>
       
</template>

<style scoped>
.game-container {
  padding: 20px;
}

.game-layout {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.main-content {
  flex: 1;
}

.debug-sidebar {
  flex-shrink: 0;
}

.debug-hint {
  margin-top: 20px;
  font-size: 12px;
  color: #666;
  text-align: center;
}
</style>
