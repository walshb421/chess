<script setup>
import Piece from './Piece.vue';
</script>
<template>
<div class="horizontal-bars">
<div class="horizontal-bar-1"></div>
<div class="horizontal-bar-2"></div>
</div>

<div class="vertical-bars">
<div class="veritcal-bar-1"></div>
<div class="veritcal-bar-2"></div>
</div>

<div>
<h1 class="welcome">We<span class="hidden">l</span>come to chess</h1>
</div>
<div class="logo-pawn">
<Piece :piece="{type: 'Pawn', team: ''}">
</Piece>
</div>

<div>
<a class="start">Start a game</a>
</div>

<div class="button-start">
</div>

<div>
<a class="settings">Settings</a>
</div>

<div class="button-settings"></div>

</template>