<!-- src/routes/+layout.svelte -->
<script lang="ts">
	import '../app.pcss';
	import { goto, invalidate } from '$app/navigation'
	import { onMount } from 'svelte'
  
	export let data;
	$: ({ supabase, session } = data);

  onMount(() => {
		const { data } = supabase.auth.onAuthStateChange((_, newSession) => {
			if (!newSession) {
				/**
				 * Queue this as a task so the navigation won't prevent the
				 * triggering function from completing
				 */
         console.debug(new Date().toLocaleString(), 'src/routes/+layout.svelte: OnAuthStateChange!', _, newSession);  // Log when action is called
				setTimeout(() => {
					goto('/', { invalidateAll: true });
				});
			}
			if (newSession?.expires_at !== session?.expires_at) {
				console.debug(new Date().toLocaleString(), 'src/routes/+layout.svelte: OnAuthStateChange!', _, newSession, session);  // Log when action is called
				invalidate('supabase:auth');
			}
		});

		return () => data.subscription.unsubscribe();
	});

</script>

<svelte:head>
	<title>Kotas: Kerala Election Prediction Leaderboard</title>
</svelte:head>

<slot />
