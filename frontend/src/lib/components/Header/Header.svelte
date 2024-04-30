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
			<span class="flex gap-2 items-center align-middle">
				Request in progress
				<svg
					width="24"
					height="24"
					stroke="#000"
					viewBox="0 0 24 24"
					xmlns="http://www.w3.org/2000/svg"
					><style>
						.spinner_V8m1 {
							transform-origin: center;
							animation: spinner_zKoa 2s linear infinite;
						}
						.spinner_V8m1 circle {
							stroke-linecap: round;
							animation: spinner_YpZS 1.5s ease-in-out infinite;
						}
						@keyframes spinner_zKoa {
							100% {
								transform: rotate(360deg);
							}
						}
						@keyframes spinner_YpZS {
							0% {
								stroke-dasharray: 0 150;
								stroke-dashoffset: 0;
							}
							47.5% {
								stroke-dasharray: 42 150;
								stroke-dashoffset: -16;
							}
							95%,
							100% {
								stroke-dasharray: 42 150;
								stroke-dashoffset: -59;
							}
						}
					</style><g class="spinner_V8m1"
						><circle cx="12" cy="12" r="9.5" fill="none" stroke-width="3"></circle></g
					></svg
				>
			</span>
		{:else}
			{nextRequestIn > 0 ? `Next request in ${nextRequestIn} seconds` : 'Requesting...'}
		{/if}
	</div>
	<div class="text-md">Total images retrieved: {totalImages}</div>
</header>
