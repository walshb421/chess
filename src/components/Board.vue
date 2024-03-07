<script setup>
import Piece from './Piece.vue';


const source = defineModel('source');
const destination = defineModel('destination');
var counter = 0;

const props = defineProps(['board']);

const horizontal = ["a", "b", "c", "d", "e", "f", "g", "h"];
const vertical = ["8", "7", "6", "5", "4", "3", "2", "1"];


function click_board(letter, number) {
    if(counter == 0 ) {
        if(props.board[letter + number] != '.') {
            source.value = letter + number;
            destination.value = null;
            counter++
        }
        
    }
    else {
        destination.value = letter + number;
        counter = 0;
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
                @click="click_board(letter, num)"
            >

                <!-- Logic For Pieces -->
                <Piece
                    v-if="props.board[letter + num] != '.'"
                    :piece="props.board[letter + num]"
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