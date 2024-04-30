<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { PUBLIC_API_URL, PUBLIC_STORAGE_BASE_URL } from '$env/static/public';
	import Header from '$lib/components/Header/Header.svelte';

	interface Image {
		id: string;
		created_at: string; // This is also assumed to be in UTC
	}

	interface ImagesResponse {
		cat_images: Image[];
		dog_images: Image[];
		total_images: number;
		last_retrieve_at: string; // UTC timestamp
	}

	let cat_images: Image[] = [];
	let dog_images: Image[] = [];
	let totalImages: number = 0;
	let errorMessage = writable('');
	let nextRequestIn = 0;
	let nextRequestChange = true;
	let requestInProgress = true;

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
			scheduleNextFetch(''); // Still keep trying to fetch images
		}
		requestInProgress = false;
	}

	function scheduleNextFetch(lastRetrieveAt: string) {
		let delay = 10000; // 10,000 milliseconds = 10 seconds
		if (lastRetrieveAt) {
			const lastRetrieveDate = new Date(lastRetrieveAt + 'Z'); // Append 'Z' to specify UTC
			const now = new Date();
			delay = lastRetrieveDate.getTime() + 60000 - now.getTime(); // 60,000 milliseconds = 1 minute
		}
		nextRequestIn = Math.ceil(delay / 1000);
		nextRequestChange = true;
		setTimeout(fetchImages, delay > 0 ? delay : 10000);
	}

	onMount(() => {
		fetchImages();
	});
</script>

<Header
	initialNextRequestIn={nextRequestIn}
	bind:nextRequestChange
	bind:requestInProgress
	{totalImages}
/>

{#if $errorMessage}
	<div class="flex justify-center">
		<p class="error">{$errorMessage}</p>
	</div>
{/if}

<div class="flex justify-center overflow-auto">
	<div class="container grid grid-cols-2 gap-2">
		<div class="flex flex-col gap-2">
			<p class="text-lg text-center">Cats</p>
			{#each cat_images as image, index}
				<div>
					<img src="{PUBLIC_STORAGE_BASE_URL}/{image.id}" alt="Cat image {index}" class="image" />
					<p>{new Date(image.created_at + 'Z').toLocaleString()}</p>
				</div>
			{/each}
		</div>
		<div class="flex flex-col gap-2">
			<p class="text-lg text-center">Dogs</p>
			{#each dog_images as image, index}
				<div>
					<img src="{PUBLIC_STORAGE_BASE_URL}/{image.id}" alt="Dog image {index}" class="image" />
					<p>{new Date(image.created_at + 'Z').toLocaleString()}</p>
				</div>
			{/each}
		</div>
	</div>
</div>
