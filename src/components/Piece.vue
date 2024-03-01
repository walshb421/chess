<script setup>
const props = defineProps(['piece']);
</script>

<template>
    <p v-if="props.piece && props.piece != '.'">{{ props.piece }}</p>
</template>