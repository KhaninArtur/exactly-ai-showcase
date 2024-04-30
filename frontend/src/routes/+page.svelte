<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { PUBLIC_API_URL } from '$env/static/public';
	import Header from '$lib/components/Header/Header.svelte';
	import type { Image, ImagesResponse } from '$lib/types';
	import Picture from '$lib/components/Picture/Picture.svelte';

	const DEFAULT_DELAY = 10 * 1000; // Default delay for scheduling the next fetch, set to 10 seconds

	let cat_images: Image[] = [];
	let dog_images: Image[] = [];
	let totalImages: number = 0;
	let errorMessage = writable(''); // Svelte store to manage error messages displayed to the user
	let nextRequestIn = 0; // Time until the next fetch in seconds
	let nextRequestChange = true; // Flag to trigger updates when the next fetch time is reset
	let requestInProgress = true; // Flag indicating whether a fetch request is in progress

	// Asynchronously fetches images from the API and updates the state
	async function fetchImages(): Promise<void> {
		requestInProgress = true;
		try {
			const response = await fetch(`${PUBLIC_API_URL}/images`);
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			const data: ImagesResponse = await response.json();
			cat_images = data.cat_images;
			dog_images = data.dog_images;
			totalImages = data.total_images;
			errorMessage.set(''); // Clear error message on successful fetch
			scheduleNextFetch(data.last_retrieve_at);
		} catch (error) {
			console.error('There was a problem with the fetch operation:', error);
			errorMessage.set('Failed to load images. Please try reloading the page.');
			scheduleNextFetch(''); // Attempts to fetch images again even after failure
		}
		requestInProgress = false;
	}

	// Schedules the next fetch based on the last retrieval time or uses the default delay
	function scheduleNextFetch(lastRetrieveAt: string) {
		let delay = DEFAULT_DELAY;
		if (lastRetrieveAt) {
			const lastRetrieveDate = new Date(lastRetrieveAt + 'Z'); // Converts server time to UTC
			const now = new Date();
			delay = lastRetrieveDate.getTime() + 60000 - now.getTime(); // Calculates delay till the next minute
		}
		nextRequestIn = Math.ceil(delay / 1000);
		nextRequestChange = true;
		setTimeout(fetchImages, delay > 0 ? delay : DEFAULT_DELAY); // Ensures non-negative delay
	}

	onMount(() => {
		fetchImages(); // Initial fetch of images when the component mounts
	});
</script>

<Header
	initialNextRequestIn={nextRequestIn}
	bind:nextRequestChange
	bind:requestInProgress
	{totalImages}
/>

{#if $errorMessage}
	<div class="flex justify-center p-3 bg-red-300">
		<p class="error">{$errorMessage}</p>
	</div>
{/if}

{#if cat_images.length > 0 || dog_images.length > 0}
	<div class="flex justify-center overflow-auto">
		<div class="container grid grid-cols-2 gap-8 mt-4">
			<div class="flex flex-col gap-2">
				<h2 class="text-xl text-center my-5">Cats 🐈</h2>
				{#each cat_images as image, index}
					<Picture {image} alt={`Cat image ${index}`} />
				{/each}
			</div>
			<div class="flex flex-col gap-2">
				<h2 class="text-xl text-center my-5">Dogs 🐕</h2>
				{#each dog_images as image, index}
					<Picture {image} alt={`Dog image ${index}`} />
				{/each}
			</div>
		</div>
	</div>
{/if}
