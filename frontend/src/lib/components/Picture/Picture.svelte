<script lang="ts">
	import { PUBLIC_STORAGE_BASE_URL } from '$env/static/public';
	import type { Image } from '$lib/types';

	export let image: Image;
	export let alt;
</script>

<div class="shadow-xl p-4">
	<img src="{PUBLIC_STORAGE_BASE_URL}/{image.id}" {alt} />
	<p class="text-right py-3">{new Date(image.created_at + 'Z').toLocaleString()}</p>
</div>
