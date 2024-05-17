<script setup>
import { useChess } from '@/composables/chess.js';
import Piece from './Piece.vue';
import { ref } from 'vue';


const { board, move } = useChess();

const source = ref(null);
const destination = ref(null);

const horizontal = ["a", "b", "c", "d", "e", "f", "g", "h"];
const vertical = ["8", "7", "6", "5", "4", "3", "2", "1"];

let count = 0;
function click_board(square) {
    if(!count) {
        source.value = square;
        count++;
    }
    else {
        destination.value = square;
        move(source.value, destination.value);
        source.value = null;
        destination.value = null;
        count = 0;
    }
}

</script>
<template>
    <div class="board" v-if="board">

        <!-- Column Labels (Letters)-->
        <div class="board-row">
            <div v-for="letter in horizontal" class="board-column-label">
                <p>{{ letter }}</p>
            </div>
        </div>

        <div v-for="num in vertical" class="board-row">

            <!-- Row Labels (Numbers)-->
            <div class="board-row-label">
                <p>{{ num }}</p>
            </div>

            <!-- Core Squares of the Board -->
            <div 
                v-for="letter in horizontal" 
                class="board-square"
                :class="{'selected': source == (letter + num) || destination == (letter + num)}"
                @click="click_board(letter + num)"
            >

                <!-- Logic For Pieces -->
                <Piece
                    v-if="board[letter + num] != '.'"
                    :piece="board[letter + num]"
                    class="board-piece"
                />
                <p class="board-square-label">{{ letter + num }}</p>
                               
            </div>

            <!-- Row Labels (Numbers)-->
            <div class="board-row-label">
                <p>{{ num }}</p>
            </div>
        </div>

        <!-- Column Labels (Letters)-->
        <div class="board-row">
            <div v-for="letter in horizontal" class="board-column-label">
                <p>{{ letter }}</p>
            </div>
        </div>
    </div>

</template>