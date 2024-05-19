<!-- src/routes/+page.svelte -->
<script lang="ts">
  import type { LayoutData } from './$types';

  export let data: LayoutData;

  let { avatar_url } = data
	$: ({ avatar_url } = data)

</script>
<div class="relative isolate max-w-7xl px-6 pt-4 lg:px-8">
  <div class="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80" aria-hidden="true">
    <div class="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"></div>
  </div>
  <div class="mx-auto max-w-2xl py-32 sm:py-12 lg:py-20">
    <div class="hidden sm:mb-8 sm:flex sm:justify-center">
      <div class="relative rounded-full px-3 py-1 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
        Winners will be announced on 4th July.
      </div>
    </div>
    <div class="text-center">
      <img class="inline-block h-16 w-16 rounded-full ring-2 ring-white" src="{avatar_url}" alt="">
      <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">Forecast your predictions!</h1>
      <p class="mt-6 text-lg leading-8 text-gray-600">Kerala Election 2024</p>
      <div class="mt-10 flex items-center justify-center gap-x-6">
        <a href="/private/predict" class="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Predict</a>
        <a href="/private/candidate" class="text-sm font-semibold leading-6 text-gray-900">View candidates <span aria-hidden="true">→</span></a>
      </div>
    </div>    
  </div>  
  <div class="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]" aria-hidden="true">
    <div class="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"></div>
  </div>
</div>

<div class="bg-white py-12 sm:py-16">
  <div class="mx-auto max-w-7xl px-6 lg:px-8">
    <div class="mx-auto max-w-2xl lg:text-center">
      <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Participants</h2>
			<ul class="pt-6 grid gap-x-8 gap-y-12 sm:grid-cols-2 sm:gap-y-16 xl:col-span-2">
				<li>
					<div class="flex items-center gap-x-6">
						<img class="h-16 w-16 rounded-full" src="/images/avatars/Anoob.webp" alt="">
						<div>
							<h3 class="text-base font-semibold leading-7 tracking-tight text-gray-900">Anoob Backer</h3>
							<p class="text-sm font-semibold leading-6 text-indigo-600">Bangalore</p>
						</div>
					</div>
				</li>
	
				<li>
					<div class="flex items-center gap-x-6">
						<img class="h-16 w-16 rounded-full" src="/images/avatars/Baiju.webp" alt="">
						<div>
							<h3 class="text-base font-semibold leading-7 tracking-tight text-gray-900">Baiju Muthukadan</h3>
							<p class="text-sm font-semibold leading-6 text-indigo-600">Kozhikode</p>
						</div>
					</div>
				</li>
	
				<li>
					<div class="flex items-center gap-x-6">
						<img class="h-16 w-16 rounded-full" src="/images/avatars/Ranish.webp" alt="">
						<div>
							<h3 class="text-base font-semibold leading-7 tracking-tight text-gray-900">Ranish George</h3>
							<p class="text-sm font-semibold leading-6 text-indigo-600">Sweden</p>
						</div>
					</div>
				</li>
	
				<li>
					<div class="flex items-center gap-x-6">
						<img class="h-16 w-16 rounded-full" src="/images/avatars/Shanavas.webp" alt="">
						<div>
							<h3 class="text-base font-semibold leading-7 tracking-tight text-gray-900">Shanavas Kodakadan</h3>
							<p class="text-sm font-semibold leading-6 text-indigo-600">Finland</p>
						</div>
					</div>
				</li>

        <li>
					<div class="flex items-center gap-x-6">
						<img class="h-16 w-16 rounded-full" src="/images/avatars/Shibu.webp" alt="">
						<div>
							<h3 class="text-base font-semibold leading-7 tracking-tight text-gray-900">Shibu Skaria</h3>
							<p class="text-sm font-semibold leading-6 text-indigo-600">Kochi</p>
						</div>
					</div>
				</li>

				<li>
					<div class="flex items-center gap-x-6">
						<img class="h-16 w-16 rounded-full" src="/images/avatars/Shiju.webp" alt="">
						<div>
							<h3 class="text-base font-semibold leading-7 tracking-tight text-gray-900">Shiju Aravindakshan</h3>
							<p class="text-sm font-semibold leading-6 text-indigo-600">Bangalore / Trissur</p>
						</div>
					</div>
				</li>

				<li>
					<div class="flex items-center gap-x-6">
						<img class="h-16 w-16 rounded-full" src="/images/avatars/Swami.webp" alt="">
						<div>
							<h3 class="text-base font-semibold leading-7 tracking-tight text-gray-900">Sumesh Sukumaran</h3>
							<p class="text-sm font-semibold leading-6 text-indigo-600">Palakkad</p>
						</div>
					</div>
				</li>
			</ul>
    </div>
  </div>
</div>