<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import Spinner from '$lib/components/Spinner/Spinner.svelte';

	export let initialNextRequestIn: number; // Initial countdown time for next request, passed from parent component
	export let nextRequestChange: boolean; // Flag to trigger countdown reset, bound to parent's state
	export let requestInProgress: boolean; // Indicates if an API request is currently active, for UI feedback
	export let totalImages: number; // Total number of images fetched, displayed in the UI

	let nextRequestIn = initialNextRequestIn;
	let countdownInterval: number;

	// Starts the countdown timer for the next request
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

	// Reactive statement to handle changes in initialNextRequestIn and reset the countdown accordingly
	$: if (initialNextRequestIn && nextRequestChange) {
		nextRequestChange = false;
		nextRequestIn = initialNextRequestIn;
		if (countdownInterval) {
			clearInterval(countdownInterval);
		}
		startCountdown();
	}
</script>

<header class="sticky top-0 z-10 flex justify-center p-2 gap-3 bg-blue-100 text-gray-800">
	<div class="container grid grid-cols-3">
		<h1 class="text-3xl font-bold">CatDog🐾</h1>
		<div class="flex items-center text-md justify-center">
			{#if requestInProgress}
				<span class="flex gap-2 items-center align-middle"> Request in progress <Spinner /></span>
			{:else}
				{nextRequestIn > 0 ? `Next request in ${nextRequestIn} seconds` : 'Requesting...'}
			{/if}
		</div>
		<div class="flex items-center justify-end text-xl font-bold">
			Total generated: {totalImages}
		</div>
	</div>
</header>
