<!-- src/routes/account/+page.svelte -->
<script lang="ts">
	import { enhance } from '$app/forms';
	import type { SubmitFunction } from '@sveltejs/kit';

	export let data
	export let form

	let { session, supabase, electionData, candidatePartyLookup } = data
	$: ({ session, supabase, electionData, candidatePartyLookup } = data)

  let electionPrediction: HTMLFormElement
	let loading = false

	const handleSubmit: SubmitFunction = () => {
		loading = true
		return async () => {
			loading = false
		}
	}

	const handleSignOut: SubmitFunction = () => {
		loading = true
		return async ({ update }) => {
			loading = false
			update()
		}
	}
</script>

{#if electionData}
<div class="max-w-full mx-auto p-6 bg-white rounded-lg shadow-md">
  <div class="overflow-auto">
    <table class="w-full text-sm text-left text-gray-500">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50">
            <tr>
                <th scope="col" class="px-3 py-3">#</th>
                <th scope="col" class="px-6 py-3">Constituency</th>
                <th scope="col" class="px-6 py-3">UDF</th>
                <th scope="col" class="px-6 py-3">LDF</th>
                <th scope="col" class="px-6 py-3">NDA</th>
            </tr>
        </thead>
        <tbody>
          {#each electionData as places}
            <tr class="bg-white border-b">
              <td class="px-6 py-4">{places.id}</td>
              <td class="px-6 py-4">{places.constituency}</td>
              <td class="px-6 py-4">{places.udf_candidate} - {candidatePartyLookup?.[places.udf_candidate]}</td>
              <td class="px-6 py-4">{places.ldf_candidate} - {candidatePartyLookup?.[places.ldf_candidate]}</td>
              <td class="px-6 py-4">{places.nda_candidate} - {candidatePartyLookup?.[places.nda_candidate]}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
{:else}
  <p>No data available.</p>
{/if}