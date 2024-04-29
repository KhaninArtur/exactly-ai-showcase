<script lang="ts">
	import { onDestroy, onMount } from 'svelte';

	export let initialNextRequestIn: number; // Time in seconds to the next request
	export let nextRequestChange: boolean;
	export let requestInProgress: boolean; // Is a request currently being made
	export let totalImages: number;

	let nextRequestIn = initialNextRequestIn;
	let countdownInterval: number;

	// Initialize and update countdown every second
	function startCountdown() {
		countdownInterval = setInterval(() => {
			if (nextRequestIn > 0) {
				nextRequestIn -= 1;
			}
		}, 1000);
	}

	onMount(() => {
		startCountdown();
	});

	onDestroy(() => {
		if (countdownInterval) {
			clearInterval(countdownInterval);
		}
	});

	// Watch for external changes to initialNextRequestIn
	$: if (initialNextRequestIn && nextRequestChange) {
		nextRequestChange = false;
		nextRequestIn = initialNextRequestIn;
		if (countdownInterval) {
			clearInterval(countdownInterval);
		}
		startCountdown();
	}
</script>

<header
	class="sticky top-0 z-10 flex justify-around items-center p-2 gap-3 bg-gray-200 text-gray-800 text-center"
>
	<div class="text-lg font-bold">CatDog</div>
	<div class="text-md">
		{#if requestInProgress}
			Request in progress
		{:else}
			{nextRequestIn > 0 ? `Next request in ${nextRequestIn} seconds` : 'Requesting...'}
		{/if}
	</div>
	<div class="text-md">Total images retrieved: {totalImages}</div>
</header>
