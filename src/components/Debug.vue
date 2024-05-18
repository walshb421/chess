<script setup>
import { useChess } from '@/composables/chess';

const { reset, status } = useChess();
</script>
<template>
    <h3>Debug Tools</h3>
    <p>Status: {{ status }}</p>
    <button @click="reset()">Reset</button>

</template>