<script setup>

const board = new Array(8).fill(
    new Array(8).fill(null) 
);

console.log(board);

</script>
<template>
    <div class="board">
        <div v-for="row in board" class="board-row">
            <div v-for="square in row" class="board-square">
                
            </div>
        </div>
    </div>
</template>