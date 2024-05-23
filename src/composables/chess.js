import { ref, watch, onMounted } from 'vue';
import { useWebSocket } from '@vueuse/core'


const { status, data, send, open, close } = useWebSocket('ws://' + window.location.hostname + ':9090');

const board = ref({}); 
const captured_white = ref([]);
const captured_black = ref([]);


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

export function useChess() {
  return {
    board,
    captured_white,
    captured_black,
    status,
    connect,
    move, 
    reset
  }
}