import { ref, watch, onMounted } from 'vue';
import { useWebSocket } from '@vueuse/core'


const { status, data, send, open, close } = useWebSocket('ws://' + window.location.hostname + ':9090');

const board = ref({}); 
const captured_white = ref([]);
const captured_black = ref([]);
const turn = ref(0);
const currentFen = ref('');
const fixtures = ref({ positions: {}, categories: {} });
const inCheck = ref(null);

const horizontal = ["a", "b", "c", "d", "e", "f", "g", "h"];
const vertical = ["8", "7", "6", "5", "4", "3", "2", "1"];

for(const letter of horizontal) {
  for(const number of vertical) {
    board.value[letter + number] = ".";
  }
}

watch(data, (newData) => {
  const parsedData = JSON.parse(newData)
  if(parsedData.board) board.value = parsedData.board;
  if(parsedData.captured_black) captured_black.value = parsedData.captured_black;
  if(parsedData.captured_white) captured_white.value = parsedData.captured_white;
  if(parsedData.turn !== undefined) turn.value = parsedData.turn;
  if(parsedData.fen) currentFen.value = parsedData.fen;
  if(parsedData.fixtures) fixtures.value = parsedData.fixtures;
  if(parsedData.in_check !== undefined) inCheck.value = parsedData.in_check;
})

const move = (source, destination) => {
  const message = {
    move: {
      source: source,
      destination: destination
    }
  }
  send(JSON.stringify(message));
}

const connect = () => {
  onMounted(() => send(JSON.stringify({"connect": {}})));
  return status
}

const reset = () => send(JSON.stringify({"reset": {}}));

const loadFen = (fen) => {
  send(JSON.stringify({ load_fen: { fen } }));
};

const loadFixture = (name) => {
  send(JSON.stringify({ load_fixture: { name } }));
};

const getFixtures = () => {
  send(JSON.stringify({ get_fixtures: {} }));
};

export function useChess() {
  return {
    board,
    captured_white,
    captured_black,
    turn,
    currentFen,
    fixtures,
    inCheck,
    status,
    connect,
    move, 
    reset,
    loadFen,
    loadFixture,
    getFixtures
  }
}
