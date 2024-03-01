<script setup>

const horizontal = ["A", "B", "C", "D", "E", "F", "G", "H"];
const vertical = ["8", "7", "6", "5", "4", "3", "2", "1"];

</script>
<template>
    <div class="board">
        <div class="board-row">
            <div v-for="letter in horizontal" class="board-column-label">
                <p>{{ letter }}</p>
            </div>
        </div>
        <div v-for="num in vertical" class="board-row">
            <div class="board-row-label">
                <p>{{ num }}</p>
            </div>
            <div v-for="letter in horizontal" class="board-square">
                <p class="board-square-label">{{ letter + num }}</p>
            </div>
            <div class="board-row-label">
                <p>{{ num }}</p>
            </div>
        </div>
        <div class="board-row">
            <div v-for="letter in horizontal" class="board-column-label">
                <p>{{ letter }}</p>
            </div>
        </div>
    </div>
</template>