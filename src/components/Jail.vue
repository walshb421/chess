<script setup>
import Piece from '@/components/Piece.vue';
import { useChess } from '@/composables/chess';

const { captured_black, captured_white } = useChess();

</script>
<template>

<h2>Jail</h2>
<div v-for="team in [captured_white, captured_black]" class="captured-pieces">
    <div class="jail">
        <Piece v-for="piece in team"
            :piece="piece"
        /> 
    </div>
</div>

</template>