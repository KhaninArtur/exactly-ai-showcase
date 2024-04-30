export interface Image {
	id: string;
	created_at: string; // UTC timestamp
}

export interface ImagesResponse {
	cat_images: Image[];
	dog_images: Image[];
	total_images: number;
	last_retrieve_at: string; // UTC timestamp
}
