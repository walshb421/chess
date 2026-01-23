<script setup>
import { useChess } from '@/composables/chess.js';
import Piece from './Piece.vue';
import { ref, computed } from 'vue';


const { board, move, inCheck } = useChess();

const source = ref(null);
const destination = ref(null);

const horizontal = ["A", "B", "C", "D", "E", "F", "G", "H"];
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

function isKingInCheck(square) {
    if (!inCheck.value) return false;
    const piece = board.value[square];
    if (piece === '.') return false;
    return piece.type === 'King' && piece.team === inCheck.value;
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
                :class="{
                    'selected': source == (letter + num) || destination == (letter + num),
                    'in-check': isKingInCheck(letter + num)
                }"
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
