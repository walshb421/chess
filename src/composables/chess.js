import { ref, watch, onMounted } from 'vue';
import { useWebSocket } from '@vueuse/core'


const { status, data, send, open, close } = useWebSocket('ws://' + window.location.hostname + ':9090');


const state = {
  source: ref(null),
  destination: ref(null),
  board: ref({}),
  captured_white: ref([]),
  captured_black: ref([]),
  connection: status
}

const horizontal = ["a", "b", "c", "d", "e", "f", "g", "h"];
const vertical = ["8", "7", "6", "5", "4", "3", "2", "1"];

for(const letter of horizontal) {
  for(const number of vertical) {
    state.board.value[letter + number] = ".";
  }
}


watch(data, (newData) => {
  const parsedData = JSON.parse(newData)
  for(const key in state) {

    if(parsedData[key]) {
      state[key].value = parsedData[key]
    }
  }
})



// method that constructs the move string 
const sendMove = (source, destination) => {
  const message = {
    "move": {
      source: source,
      destination: destination
    }
  }
  send(JSON.stringify(message));

  state.source.value  = null;
  state.destination.value  = null;

}

const reset = () => send(JSON.stringify({"reset": {}}))

watch(state.destination, (newDestination) => {
  if(state.source && state.destination) {
    sendMove(state.source, state.destination)
  }
})


export function useChess() {
  onMounted(() => send(JSON.stringify({"connect": {}})));
  return {
    reset: reset,
    state: state,
  }
}