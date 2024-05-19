<!-- src/routes/account/+page.svelte -->
<script lang="ts">
	export let data

	let { session, supabase, electionData, candidatePartyLookup } = data
	$: ({ session, supabase, electionData, candidatePartyLookup } = data)
  
</script>

{#if electionData}
<div class="max-w-full mx-auto p-6 bg-white rounded-lg shadow-md">
  <div class="flex flex-wrap gap-8 p-2 place-content-center">
    {#each electionData as places}
      <!-- Constituency -->
      <div class="flex bg-white shadow rounded-lg p-4 place-content-center">
        <div class="flex flex-col space-y-3">
          <p class="px-6 py-4 font-bold text-center">{places.id}. {places.constituency}</p>
          <!-- UDF candidate -->
          <div class="flex flex-row items-center space-x-3 space-y-3">
            <img class="inline-block h-12 rounded-full ring-2 ring-white" src="{candidatePartyLookup?.[places.udf_candidate].photo_url}" alt="{places.udf_candidate}">
            <div class="font-semibold text-gray-900">{places.udf_candidate}</div>
            <svg viewBox="0 0 2 2" width="3" height="3" aria-hidden="true" class="fill-gray-900"><circle cx="1" cy="1" r="1" /></svg>
            <div class="text-gray-600">UDF</div>
            <svg viewBox="0 0 2 2" width="3" height="3" aria-hidden="true" class="fill-gray-900"><circle cx="1" cy="1" r="1" /></svg>
            <div class="text-gray-600 bg-green-100 rounded-full px-2 py-1 text-center">{candidatePartyLookup?.[places.udf_candidate].party}</div>
          </div>
          <!-- LDF candidate -->
          <div class="flex flex-row items-center space-x-3 space-y-3">
            <img class="inline-block h-12 rounded-full ring-2 ring-white" src="{candidatePartyLookup?.[places.ldf_candidate].photo_url}" alt="{places.ldf_candidate}">
            <div class="font-semibold  text-gray-900">{places.ldf_candidate}</div>
            <svg viewBox="0 0 2 2" width="3" height="3" aria-hidden="true" class="fill-gray-900"><circle cx="1" cy="1" r="1" /></svg>
            <div class="text-gray-600">LDF</div>
            <svg viewBox="0 0 2 2" width="3" height="3" aria-hidden="true" class="fill-gray-900"><circle cx="1" cy="1" r="1" /></svg>
            <div class="text-gray-600 bg-green-100 rounded-full px-2 py-1 text-center">{candidatePartyLookup?.[places.ldf_candidate].party}</div>
          </div>
          <!-- NDA candidate -->
          <div class="flex flex-row items-center space-x-3 space-y-3">
            <img class="inline-block h-12 rounded-full ring-2 ring-white" src="{candidatePartyLookup?.[places.nda_candidate].photo_url}" alt="{places.nda_candidate}">
            <div class="font-semibold text-gray-900">{places.nda_candidate}</div>
            <svg viewBox="0 0 2 2" width="3" height="3" aria-hidden="true" class="fill-gray-900"><circle cx="1" cy="1" r="1" /></svg>
            <div class="text-gray-600">NDA</div>
            <svg viewBox="0 0 2 2" width="3" height="3" aria-hidden="true" class="fill-gray-900"><circle cx="1" cy="1" r="1" /></svg>
            <div class="text-gray-600 bg-green-100 rounded-full px-2 py-1 text-center">{candidatePartyLookup?.[places.nda_candidate].party}</div>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>
{:else}
  <p>No data available.</p>
{/if}