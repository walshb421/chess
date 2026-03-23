<script setup>
import { ref, onMounted, computed } from 'vue';
import { useChess } from '@/composables/chess.js';

const { 
  turn, 
  currentFen, 
  fixtures,
  reset, 
  loadFen, 
  loadFixture,
  getFixtures 
} = useChess();

const fenInput = ref('');
const selectedFixture = ref('');
const copySuccess = ref(false);

// Request fixtures on mount
onMounted(() => {
  getFixtures();
});

// Computed property for organized fixture options
const fixtureCategories = computed(() => {
  return fixtures.value.categories || {};
});

const fixturePositions = computed(() => {
  return fixtures.value.positions || {};
});

const handleLoadFen = () => {
  if (fenInput.value.trim()) {
    loadFen(fenInput.value.trim());
    fenInput.value = '';
  }
};

const handleLoadFixture = () => {
  if (selectedFixture.value) {
    loadFixture(selectedFixture.value);
    selectedFixture.value = '';
  }
};

const copyCurrentFen = async () => {
  try {
    await navigator.clipboard.writeText(currentFen.value);
    copySuccess.value = true;
    setTimeout(() => {
      copySuccess.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy FEN:', err);
  }
};

const currentPlayer = computed(() => {
  return turn.value % 2 === 0 ? 'White' : 'Black';
});

const moveNumber = computed(() => {
  return Math.floor(turn.value / 2) + 1;
});

// Format fixture name for display
const formatFixtureName = (name) => {
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};
</script>

<template>
  <div class="debug-panel">
    <h3>Debug Panel</h3>
    
    <!-- Game State -->
    <div class="debug-section">
      <h4>Game State</h4>
      <p><strong>Turn:</strong> {{ currentPlayer }} (Move {{ moveNumber }})</p>
      <p><strong>Half-moves:</strong> {{ turn }}</p>
    </div>

    <!-- Current FEN -->
    <div class="debug-section">
      <h4>Current FEN</h4>
      <div class="fen-display">
        <code>{{ currentFen }}</code>
        <button @click="copyCurrentFen" class="btn-small">
          {{ copySuccess ? 'Copied!' : 'Copy' }}
        </button>
      </div>
    </div>

    <!-- Load FEN -->
    <div class="debug-section">
      <h4>Load FEN</h4>
      <div class="input-group">
        <input 
          v-model="fenInput" 
          type="text" 
          placeholder="Paste FEN string..."
          @keyup.enter="handleLoadFen"
        />
        <button @click="handleLoadFen" class="btn-primary">Load</button>
      </div>
    </div>

    <!-- Load Fixture -->
    <div class="debug-section">
      <h4>Load Test Fixture</h4>
      <div class="input-group">
        <select v-model="selectedFixture">
          <option value="">-- Select Position --</option>
          <optgroup 
            v-for="(fixtureNames, category) in fixtureCategories" 
            :key="category"
            :label="category"
          >
            <option 
              v-for="name in fixtureNames" 
              :key="name" 
              :value="name"
            >
              {{ formatFixtureName(name) }}
            </option>
          </optgroup>
        </select>
        <button @click="handleLoadFixture" class="btn-primary">Load</button>
      </div>
    </div>

    <!-- Actions -->
    <div class="debug-section">
      <h4>Actions</h4>
      <button @click="reset" class="btn-danger">Reset Board</button>
    </div>
  </div>
</template>

<style scoped>
.debug-panel {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  max-width: 400px;
  font-size: 14px;
}

.debug-panel h3 {
  margin: 0 0 16px 0;
  color: #fff;
  border-bottom: 1px solid #333;
  padding-bottom: 8px;
}

.debug-panel h4 {
  margin: 0 0 8px 0;
  color: #aaa;
  font-size: 12px;
  text-transform: uppercase;
}

.debug-section {
  margin-bottom: 16px;
}

.debug-section p {
  margin: 4px 0;
  color: #ccc;
}

.fen-display {
  display: flex;
  gap: 8px;
  align-items: center;
}

.fen-display code {
  flex: 1;
  background: #2a2a2a;
  padding: 8px;
  border-radius: 4px;
  font-size: 11px;
  color: #4fc3f7;
  word-break: break-all;
  max-width: 280px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.input-group {
  display: flex;
  gap: 8px;
}

.input-group input,
.input-group select {
  flex: 1;
  padding: 8px;
  border: 1px solid #333;
  border-radius: 4px;
  background: #2a2a2a;
  color: #fff;
  font-size: 13px;
}

.input-group input::placeholder {
  color: #666;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s;
}

.btn-primary {
  background: #4fc3f7;
  color: #000;
}

.btn-primary:hover {
  background: #29b6f6;
}

.btn-small {
  padding: 4px 12px;
  font-size: 12px;
  background: #333;
  color: #fff;
}

.btn-small:hover {
  background: #444;
}

.btn-danger {
  background: #ef5350;
  color: #fff;
}

.btn-danger:hover {
  background: #f44336;
}
</style>
