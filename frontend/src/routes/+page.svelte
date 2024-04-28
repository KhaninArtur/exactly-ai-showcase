<script lang="ts">
  import {onMount} from 'svelte';
  import {writable} from 'svelte/store';
  import {PUBLIC_API_URL, PUBLIC_STORAGE_BASE_URL} from '$env/static/public';

  interface Image {
    id: string;
    created_at: string;  // This is also assumed to be in UTC
  }

  interface ImagesResponse {
    images: Image[];
    total_images: number;
    last_retrieve_at: string;  // UTC timestamp
  }

  let images: Image[] = [];
  let errorMessage = writable('');

  async function fetchImages(): Promise<void> {
    try {
      const response = await fetch(`${PUBLIC_API_URL}/images`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data: ImagesResponse = await response.json();
      images = data.images;
      errorMessage.set(''); // Clear error message on successful fetch
      scheduleNextFetch(data.last_retrieve_at);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
      errorMessage.set('Failed to load images. Please try reloading the page.');
    }
  }

  function scheduleNextFetch(lastRetrieveAt: string) {
    const lastRetrieveDate = new Date(lastRetrieveAt + 'Z');  // Append 'Z' to specify UTC
    const now = new Date();
    const delay = lastRetrieveDate.getTime() + 60000 - now.getTime(); // 60,000 milliseconds = 1 minute
    setTimeout(fetchImages, delay > 0 ? delay : 0);
  }

  onMount(() => {
    fetchImages();
  });
</script>

{#if $errorMessage}
  <p class="error">{$errorMessage}</p>
{/if}

<div class="grid grid-cols-2">
  {#each images as image}
    <div>
      <img src="{PUBLIC_STORAGE_BASE_URL}/{image.id}" alt="Image {image.id}" class="image"/>
      <p>{new Date(image.created_at + 'Z').toLocaleString()}</p>
    </div>
  {/each}
</div>