<script setup>
import Piece from './Piece.vue';

const props = defineProps(['board']);

const horizontal = ["A", "B", "C", "D", "E", "F", "G", "H"];
const vertical = ["8", "7", "6", "5", "4", "3", "2", "1"];

var indexes = {};


for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
       const label = horizontal[i] + vertical[j];
       indexes[label] = [j, i];
    }
}

function getPiece(board, letter, number) {
    var i, j;
    [i, j] = indexes[letter + number];
    return board[i][j];
}


</script>
<template>
    <div class="board">

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
            <div v-for="letter in horizontal" class="board-square">

                <!-- Logic For Pieces -->
                <Piece 
                    v-if="getPiece(props.board, letter, num) != '.'" 
                    :piece="getPiece(props.board, letter, num)"
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