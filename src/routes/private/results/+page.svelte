<!-- src/routes/private/leaderboard/+page.svelte -->
<script lang="ts">
  export let data;

	let { allianceSummary, partylookup, partySummary, avatar_url, username, resultsReady, electionResults } = data;
	$: ({ allianceSummary, partylookup, partySummary, avatar_url, username, resultsReady, electionResults } = data);
	
  let loading = false;

  let partiesData = [
    { party: 'BJP', voteSharePercentage: '16.68%', totalVotes: 3296354, color: '#ff944d' },
    { party: 'BSP', voteSharePercentage: '0.25%', totalVotes: 48963, color: '#000078' },
    { party: 'CPI', voteSharePercentage: '6.14%', totalVotes: 1212197, color: '#e70d21' },
    { party: 'CPI(M)', voteSharePercentage: '25.82%', totalVotes: 5100964, color: '#FF1D15' },
    { party: 'INC', voteSharePercentage: '35.06%', totalVotes: 6927111, color: '#4e82f7' },
    { party: 'IUML', voteSharePercentage: '6.07%', totalVotes: 1199839, color: '#4e82f7' },
    { party: 'KEC', voteSharePercentage: '1.38%', totalVotes: 272418, color: '#A209D6' },
    { party: 'NOTA', voteSharePercentage: '0.79%', totalVotes: 156585, color: '#ff6384' },
    { party: 'Others', voteSharePercentage: '7.81%', totalVotes: 1543974, color: '#b3b3b3' }
  ];

  partiesData = partiesData.sort((a, b) => b.totalVotes - a.totalVotes);


	function formatDate(dateString: string) {
		const date = new Date(dateString);
		const options: Intl.DateTimeFormatOptions = {
			weekday: 'short',
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		};
		return date.toLocaleDateString(undefined, options);
	}

  function formatNumberWithSeparator(num: number, locale: string = 'en-US'): string {
    return num.toLocaleString(locale);
  }
</script>


<div class="relative isolate max-w-7xl px-6 pt-4 lg:px-8">
	<div class="absolute inset-x-0 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
		<div
			class="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
			style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"
		></div>
	</div>
	<div class="mx-auto max-w-2xl py-32 sm:py-12 lg:py-20">
		<div class="hidden sm:mb-8 sm:flex sm:justify-center">
			{#if resultsReady === false}
      <div class="relative rounded-full px-3 py-1 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
        Winners will be announced on 4<sup>th</sup> Jun.
      </div>
			{:else}
			<div class="relative rounded-full px-3 py-1 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
        🎉 The results got updated!
      </div>
			{/if}
		</div>
		<div class="text-center">
			<img class="inline-block h-16 w-16 rounded-full ring-2 ring-white" src={avatar_url} alt="" />
			<h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">Hello {username}!</h1>
			<p class="mt-6 text-lg leading-8 text-gray-600">
        {#if resultsReady === false}
				🕒 Stay tuned, scores will be updated after announcing election results!
        {:else}
        🎉 The wait is over, the election results are in – <i>check the results now</i>!
        <!-- 🚧 The election counting in progress – <i>check your scores now</i>! -->
        {/if}        
			</p>
		</div>
	</div>
	<div
		class="absolute inset-x-0 top-[calc(100%-5rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-10rem)]"
		aria-hidden="true"
	>
		<div
			class="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]"
			style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"
		></div>
	</div>
</div>


{#if electionResults && resultsReady !== false}
<!-- Show Kerala SVG Image -->
<div class="max-w-full mx-auto p-6 align-middle place-content-center shadow-md w-11/12">
  <div class="flex flex-row flex-wrap  place-content-center items-center">
  <div class="flex flex-col h-3/5 z-10 p-4">
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" pointer-events="none" width="100%" height="100%"
  viewBox="115 20 280 430" preserveAspectRatio="xMidYMid meet">
      <g>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M307 174L305 172L299 176L279 175L278 183L274 185L271 188L271 190L269 189L267 191L275 195L270 198L271 203L266 202L264 205L262 205L260 202L260 204L256 202L254 205L253 204L250 207L254 209L253 212L260 215L261 214L264 218L272 218L275 216L280 218L291 214L293 216L291 218L293 220L296 219L298 221L306 221L305 218L311 220L313 218L312 217L314 217L317 214L315 213L318 212L318 208L316 206L310 204L308 205L301 201L306 191L313 191L309 189L309 182L307 182L304 179L307 176L307 174z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M276 301L276 301zM276 301L276 301zM270 293L270 297L270 293zM264 289L263 290L267 306L267 300L269 300L269 298L268 295L267 298L265 294L269 296L269 294L266 293L264 289zM265 289L267 293L267 289L265 289zM264 288L264 288zM266 286L266 286zM264 285L265 288L264 285zM265 285L265 285zM266 289L266 289zM266 283L265 284L266 283zM266 283L265 284L266 283zM264 277L264 277zM262 268L258 270L260 272L257 269L262 288L263 289L264 286L262 278L261 279L261 273L263 279L264 278L262 274L266 278L264 282L266 282L265 285L266 288L265 283L267 285L266 288L268 292L270 292L269 293L271 297L273 297L272 294L274 294L277 301L276 294L274 294L272 289L275 286L275 282L273 282L273 280L270 281L272 277L270 275L271 272L269 270L266 271L264 268L262 268z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M348 254L343 258L339 259L335 264L333 264L330 267L315 260L303 263L299 272L293 275L292 281L290 285L287 287L287 289L290 290L290 292L296 300L301 302L302 301L307 305L309 304L314 306L322 314L326 322L322 322L321 330L323 330L327 334L330 334L334 342L337 341L338 337L340 336L347 336L350 339L352 339L354 344L352 352L358 354L357 352L359 350L358 349L361 348L362 346L362 341L365 337L366 338L368 336L369 333L363 327L364 324L363 326L361 326L361 324L354 326L347 322L350 316L350 312L352 312L352 306L354 306L351 296L357 289L355 289L355 285L350 279L350 277L356 275L358 267L357 265L355 266L354 260L352 258L353 256L349 254z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M353 415L352 414L349 418L342 422L343 427L340 428L340 430L337 431L337 433L335 433L332 430L333 421L329 421L325 417L325 415L322 418L321 415L319 417L321 423L330 432L330 434L341 443L343 441L347 441L347 439L345 439L345 436L347 436L349 431L352 430L350 425L351 424L353 426L357 421L354 415z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M313 393L311 393L313 395L310 398L303 398L304 401L319 420L320 415L322 417L324 417L324 415L326 419L330 421L331 420L333 422L332 429L334 433L336 431L338 433L338 431L342 427L343 428L342 422L349 418L351 414L353 414L347 405L349 401L345 397L336 393L332 397L334 400L329 399L325 401L324 398L314 393z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M184 106L184 106zM194 75L189 81L186 78L184 80L186 85L187 84L187 88L184 89L182 92L179 91L178 96L182 96L181 97L183 101L181 101L181 103L185 103L180 106L183 107L185 105L187 109L184 106L178 106L180 110L184 114L186 114L191 119L191 121L193 121L193 119L193 123L195 119L200 119L199 116L200 117L202 115L204 117L205 116L205 118L209 116L212 117L211 116L214 115L235 116L235 114L233 113L235 112L235 107L230 106L228 105L228 103L226 103L223 97L224 94L219 93L217 95L214 92L215 91L210 91L208 87L204 87L199 82L200 81L198 80L198 78L194 75zM184 106L184 106z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M297 252L294 247L278 254L272 252L271 253L269 251L267 253L267 255L269 255L269 259L264 259L264 261L262 261L261 258L259 258L259 260L256 259L255 252L253 249L252 256L256 268L264 268L266 270L270 270L270 276L272 276L270 280L272 280L275 283L273 289L277 293L279 293L279 295L282 292L284 292L288 286L290 286L290 282L292 282L294 274L299 273L304 262L310 262L314 260L319 261L323 264L320 261L320 259L316 259L317 257L315 255L310 256L310 254L307 252L298 252z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#FF1D15" fill-opacity="1"
          fill-rule="evenodd"
          d="M319 211L315 213L317 213L314 216L315 217L312 218L313 219L312 218L310 220L306 218L305 221L297 221L296 218L295 220L293 220L291 218L293 216L291 214L284 218L277 218L276 216L274 216L273 218L264 218L263 215L259 214L256 222L254 220L253 221L247 219L246 222L243 223L246 231L249 228L250 229L254 227L254 229L251 232L253 239L260 236L260 234L264 234L264 232L265 233L267 231L268 232L274 229L285 242L292 247L293 246L298 252L306 252L310 253L309 256L317 256L318 254L315 248L317 232L315 231L315 229L321 227L320 222L322 220L323 213L320 212z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#ff944d" fill-opacity="1"
          fill-rule="evenodd"
          d="M246 237L246 237zM246 236L246 236zM242 223L238 223L240 229L245 238L246 233L245 234L247 236L245 240L249 246L250 251L253 254L252 251L253 250L255 252L257 260L259 260L259 258L261 258L262 261L264 261L264 259L266 261L269 260L269 256L267 254L268 251L270 253L280 253L294 247L284 242L280 237L281 236L274 229L272 229L269 232L264 232L264 234L260 234L260 236L253 239L251 233L254 227L250 229L249 228L246 231L242 223z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M178 104L178 104zM178 104L178 104zM178 99L178 99zM177 102L177 104L177 102zM165 90L167 96L165 91zM168 90L168 90zM165 87L165 89L165 87zM180 96L178 98L180 100L181 99L175 99L175 101L176 100L180 106L185 103L181 103L181 101L183 101L180 96zM178 98L178 98zM163 83L164 86L163 83zM166 90L166 92L166 90zM163 82L162 83L163 82zM163 83L163 83zM150 27L148 29L147 28L141 31L139 30L140 35L141 34L140 35L145 44L148 55L156 67L161 82L162 81L165 86L165 90L167 92L168 89L169 90L166 93L167 92L171 94L167 94L168 99L171 100L171 98L178 105L175 98L178 99L177 98L179 96L179 91L182 92L185 89L187 89L187 85L184 80L186 78L189 81L191 77L195 74L189 74L189 66L187 66L184 63L184 59L188 59L189 56L188 54L185 55L185 57L181 58L181 55L179 55L178 52L176 52L175 50L177 47L181 47L177 44L175 44L172 48L170 47L169 42L164 42L165 39L160 36L158 36L159 38L156 39L155 34L152 35L152 33L149 33L151 31L151 28zM162 82L163 87L165 89L162 82z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M277 321L276 322L277 321zM271 302L271 304L271 302zM276 302L276 302zM276 308L275 309L276 308zM268 300L268 300zM274 298L273 301L276 302L274 298zM269 296L267 308L271 336L282 363L284 365L281 360L281 356L284 365L286 363L286 367L284 367L289 378L290 375L291 374L291 376L293 374L292 373L295 372L295 368L290 368L290 366L294 364L292 360L289 361L289 357L286 354L286 352L284 350L282 352L283 349L281 347L279 348L276 346L278 344L274 338L274 334L276 331L274 329L274 325L277 316L275 314L275 302L274 303L271 298L272 307L274 311L273 312L273 308L271 306L271 298L269 296zM275 302L275 302z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M284 330L278 330L276 332L276 330L274 333L274 337L276 343L278 343L277 346L279 348L283 348L282 351L283 352L283 350L289 357L289 361L292 360L294 364L290 366L291 369L294 369L294 367L295 368L295 372L292 373L294 378L296 378L294 380L297 382L299 379L303 379L307 387L312 388L312 386L315 385L318 388L317 384L322 380L322 378L323 379L323 377L320 376L328 376L326 374L333 373L334 368L325 363L327 367L326 368L320 367L316 370L312 369L310 370L310 372L301 372L302 369L298 367L302 365L302 363L303 364L300 360L299 361L300 356L302 354L299 348L293 346L289 350L284 348L288 346L287 341L295 341L294 338L297 337L297 333L294 332L294 334L292 334L288 331L285 332L284 330zM278 328L278 329zM281 328L279 328L279 330L281 330L281 328zM281 328L281 330L284 329L281 328zM279 326L276 329L278 329L280 327L279 326z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M335 368L334 367L332 373L326 374L328 376L320 376L323 377L323 379L322 378L322 380L317 383L317 388L314 385L311 388L307 388L304 384L305 381L300 379L296 382L294 381L295 378L291 376L291 374L289 378L291 384L290 385L293 390L295 390L293 390L294 389L305 399L306 397L311 397L313 395L311 393L315 392L319 397L323 397L323 400L325 401L329 399L334 400L332 397L335 393L345 397L350 401L355 394L354 390L351 387L352 386L349 385L345 378L346 375L350 373L335 368z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M284 329L285 330L284 329zM276 312L276 312zM273 287L272 288L274 293L276 293L276 301L278 303L277 302L275 306L277 308L277 314L279 314L278 317L280 317L278 319L280 319L281 322L280 327L284 327L284 329L287 330L285 330L285 332L288 331L291 332L291 334L293 334L297 332L296 331L298 329L301 330L303 327L301 323L306 324L306 326L308 326L310 320L307 315L311 313L315 315L317 313L321 315L321 313L314 306L309 304L308 305L301 301L296 301L294 295L290 292L290 290L287 289L279 295L279 293L277 293L273 289L273 287z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M319 315L317 313L315 315L311 313L307 315L310 320L309 325L306 326L306 324L301 323L303 327L302 330L298 330L296 332L297 337L294 338L295 341L288 341L288 345L284 348L291 349L291 347L293 346L299 348L300 353L302 353L300 355L301 356L299 360L303 363L299 365L298 368L300 368L302 372L310 372L310 370L312 369L316 371L320 367L326 368L328 367L325 365L325 363L329 366L350 373L350 371L356 365L355 362L357 359L357 355L352 352L354 344L352 339L350 339L347 336L341 336L337 338L336 341L333 342L332 338L329 336L329 333L328 332L327 334L321 330L321 322L326 322L322 314L321 313L321 315L319 315z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M240 170L239 169L237 171L232 172L228 176L231 178L229 178L229 181L228 180L226 184L230 188L230 190L235 189L240 194L243 195L245 191L246 194L249 195L247 198L249 198L254 205L256 202L258 204L260 204L260 202L263 205L266 202L271 203L270 198L275 195L267 191L269 189L270 190L272 186L266 186L267 182L265 180L263 182L259 182L258 177L256 179L254 177L250 177L250 179L245 177L240 180L239 177L241 177L244 174L240 171z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M228 186L227 187L229 193L230 192L229 195L231 199L233 213L235 215L236 220L239 223L246 222L247 219L256 222L256 220L259 217L258 214L255 213L253 211L254 210L250 207L253 204L251 201L252 200L250 200L247 197L249 196L249 194L247 194L245 190L245 194L239 194L238 191L237 192L234 189L231 190L231 188L228 186z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M252 103L241 108L235 107L235 112L233 113L235 115L234 116L223 115L221 120L223 125L228 129L233 130L232 136L235 140L237 140L239 144L237 147L238 150L236 152L239 155L240 152L241 155L237 164L239 169L244 174L241 177L239 177L239 179L240 180L245 177L249 179L249 177L252 176L254 178L255 177L255 179L257 177L259 182L263 182L265 180L267 182L266 185L268 185L269 187L276 185L279 182L278 175L282 176L282 172L291 166L291 161L280 156L279 153L277 154L273 151L271 152L267 150L264 151L264 144L262 142L263 140L267 139L269 141L280 136L281 133L278 130L278 128L280 127L279 125L271 125L267 119L262 119L258 113L253 115L251 112L252 107z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M203 115L199 117L199 120L195 120L194 123L195 122L196 123L194 123L199 128L198 127L200 123L201 127L199 129L201 131L207 149L209 151L210 150L215 155L217 161L219 159L219 156L217 154L217 148L219 146L221 147L224 142L229 143L232 137L232 132L234 130L228 129L222 124L222 115L214 115L211 116L212 117L209 116L205 118L205 116L204 117L203 115z"></path>
        <path class="leaflet-interactive" stroke="#fff" stroke-opacity="1" stroke-width="1"
          stroke-linecap="butt" stroke-linejoin="miter" fill="#4e82f7" fill-opacity="1"
          fill-rule="evenodd"
          d="M227 181L226 182L227 181zM237 142L237 140L235 140L232 137L229 143L224 142L221 147L217 147L217 153L219 155L217 163L220 166L223 177L225 177L224 180L226 182L231 177L229 176L230 174L239 169L237 163L240 159L241 154L240 152L239 155L236 152L238 150L237 147L240 144L238 143zM225 179L225 179z"></path>
      </g>
    </svg>
  </div>
  <!-- Summary by local alliances -->
  <div class="flex flex-col">
    <ul role="list" class="divide-y divide-gray-100rounded-lg p-4 w-fit">
      {#each Object.entries(allianceSummary ?? {}) as [alliance, count]}
      <li class="flex justify-between gap-x-6 py-5">
        <div class="flex min-w-0 gap-x-4">
          <!-- Colored Circle for Alliance -->
          <div class="h-12 w-12 flex-none rounded-full
            {alliance === 'UDF' ? 'bg-blue-500' : ''}
            {alliance === 'LDF' ? 'bg-red-500' : ''}
            {alliance === 'NDA' ? 'bg-orange-500' : ''}">
          </div>
          <div class="min-w-0 flex-auto">
            <p class="text-sm font-semibold leading-6 text-gray-900">{alliance}</p>
            <!-- <p class="mt-1 truncate text-xs leading-5 text-gray-500">leslie.alexander@example.com</p> -->
          </div>
        </div>
        <div class="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
          <p class="text-sm leading-6 text-gray-900">{count}</p>
          <p class="mt-1 text-xs leading-5 text-gray-500">Seats</p>
        </div>
      </li>
      {/each}
    </ul>    
  </div>
</div>
</div>

<!-- Results summary -->
<div class="max-w-full mx-auto p-6 z-0">
  <h1 class="p-8 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Results summary</h1>
  <div class="flex flex-row flex-wrap  place-content-center">
    <!-- Summary by elected party -->
    <div class="flex flex-col flex-wrap min-w-full gap-8 p-2">
      <ul role="list" class="divide-y divide-gray-100rounded-lg p-4 shadow-md">
        {#each Object.entries(partySummary?? {}) as [party, count]}
        <li class="flex justify-between gap-x-6 py-5">
          <div class="flex min-w-0 gap-x-4">
            <img class="h-12 w-12 flex-none rounded-full bg-gray-50" src="/images/party/{party}.webp" alt="{party}">
            <div class="min-w-0 flex-auto">
              <p class="text-sm font-semibold leading-6 text-gray-900">{party}</p>
              <!-- <p class="mt-1 truncate text-xs leading-5 text-gray-500">leslie.alexander@example.com</p> -->
            </div>
          </div>
          <div class="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
            <p class="text-sm leading-6 text-gray-900">{count}</p>
            <p class="mt-1 text-xs leading-5 text-gray-500">Seats</p>
          </div>
        </li>
        {/each}
      </ul>    
    </div>

    <!-- Summary by vote share -->
    <div class="flex flex-col flex-wrap min-w-full gap-8 p-2">
      <ul role="list" class="divide-y divide-gray-100rounded-lg p-4 shadow-md">
        {#each partiesData as { party, voteSharePercentage, totalVotes, color }}
        <li class="flex justify-between gap-x-6 py-5">
          <div class="flex min-w-0 gap-x-4">
            {#if party === 'BSP'}
            <div class="h-12 w-12 flex-none rounded-full bg-blue-900"></div>
            {:else if party === 'Others'}
            <div class="h-12 w-12 flex-none rounded-full bg-gray-500"></div>
            {:else}
            <img class="h-12 w-12 flex-none rounded-full bg-gray-50" src="/images/party/{party}.webp" alt="{party}">
            {/if}
                          
            <div class="min-w-0 flex-auto">
              <p class="text-sm font-semibold leading-6 text-gray-900">{party}</p>
              <!-- <p class="mt-1 truncate text-xs leading-5 text-gray-500">leslie.alexander@example.com</p> -->
            </div>
          </div>
          <div class="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
            <p class="text-sm leading-6 text-gray-900">{voteSharePercentage}</p>
            <p class="mt-1 text-xs leading-5 text-gray-500">{formatNumberWithSeparator(totalVotes)} votes</p>
          </div>
        </li>
        {/each}
      </ul>
    </div>
  </div>
</div>

<div class="max-w-full mx-auto p-6">
  <h1 class="p-8 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Detailed scorecard</h1>
  <div class="flex flex-wrap gap-8 p-2">
      {#each electionResults as constituency}
        <!-- Constituency -->
        <div class="flex shadow rounded-lg p-4 max-w-fill place-content-center">
          <div class="flex flex-col">
            <p class="mt-4 mb-4 font-bold text-center w-48 overflow-hidden text-ellipsis whitespace-nowrap">{constituency.constituency_name}</p>
            <!-- Winning candidate -->
            <div class="flex flex-row items-center p-4">
              <!-- Winner Details -->
              <div class="flex flex-row place-content-center gap-2">
                <!-- Canidate image -->
                <img class="inline-block h-32 rounded-full ring-2 ring-white" src="{partylookup?.[constituency.elected_member].photo_url}" alt="{constituency.elected_member}">                  
                <!-- Details  -->
                <div class="flex flex-col gap-2">
                  <div class="text-left">
                    <p class="font-semibold text-gray-900 w-32 overflow-hidden text-ellipsis whitespace-nowrap">{constituency.elected_member}</p>
                    <img class="inline-block h-6 rounded-full ring-2 ring-white" src="/images/party/{constituency.elected_party}.webp" alt="{constituency.elected_party}">
                  </div>
                  <div class="text-left">
                    <p class="font-semibold text-gray-600">Party:</p>
                    <p class="text-gray-600">{constituency.elected_party}</p>                      
                  </div>
                  <div class="text-left">
                    <p class="font-semibold text-gray-600">Vote Share:</p>
                    <p class="text-gray-600">{constituency.vote_share_percentage}%</p>                      
                  </div>
                  
                  <div class="text-left">
                    <p class="font-semibold text-gray-600">Winning votes:</p>
                    <p class="text-gray-600">{formatNumberWithSeparator(constituency.margin)}</p>
                  </div>
                </div>
              </div>            
            </div>
          </div>            
        </div>
      {/each}
  </div>
</div>
{/if}

