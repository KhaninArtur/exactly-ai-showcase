# CatDog🐾 Image Gallery

This project is built with SvelteKit, leveraging [`create-svelte`](https://github.com/sveltejs/kit/tree/main/packages/create-svelte) to streamline the setup. It showcases a dynamic image gallery of cats and dogs, fetched from an API.

## Project Setup

This application was scaffolded using the following command, which sets up the necessary SvelteKit environment:

```bash
npm create svelte@latest frontend
```

## Development Environment

After cloning the project and installing dependencies, start the local development server with:

```bash
npm install # Install dependencies
npm run dev # Starts the development server

# Optionally, automatically open the app in a new browser tab
npm run dev -- --open
```

Set the required environment variables — mentioned in [API Integration](#api-integration).

## Project Structure

- `src/routes`: Contains the Svelte pages and layouts.
- `src/lib/components`: Includes reusable components like Header and Picture.
- `src/lib/types`: Type definitions used across the project.
- `+page.svelte`: The main page that interacts with the API to fetch images.


## API Integration

The application fetches images from a defined API set in the environment variables ($env/static/public).
The images are stored in Google Cloud Storage bucket, which name is also set in the environment variables.

Ensure these are correctly set in `.env` for proper functionality.
You can use [`template.env`](template.env) as a template.

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.

## Deployment

The app is deployed as static files served by the backend. For more information, check the [parent folder](../).
