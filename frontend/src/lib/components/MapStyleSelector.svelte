<script lang="ts">
	import { basemapOptions, getBasemapLabel } from '$lib';
	import { onMount } from 'svelte';

	import MapIcon from '~icons/mdi/map';
	import ChevronDownIcon from '~icons/mdi/chevron-down';
	import ChevronUpIcon from '~icons/mdi/chevron-up';
	import MagnifyIcon from '~icons/mdi/magnify';

	export let basemapType: string = 'default';

	let showAdvanced = false;
	let searchQuery = '';
	let dropdownOpen = false;

	// Load saved preference from localStorage
	onMount(() => {
		const saved = localStorage.getItem('preferredBasemap');
		if (saved && basemapOptions.some((opt) => opt.value === saved)) {
			basemapType = saved;
		}
	});

	// Save basemap selection to localStorage
	function selectBasemap(value: string) {
		basemapType = value;
		localStorage.setItem('preferredBasemap', value);
		dropdownOpen = false;
	}

	// Filter basemaps
	$: essentialMaps = basemapOptions.filter((opt) => opt.category === 'essential');
	$: advancedMaps = basemapOptions.filter((opt) => opt.category === 'advanced');

	// Filter advanced maps by search query
	$: filteredAdvancedMaps = advancedMaps.filter((opt) =>
		opt.label.toLowerCase().includes(searchQuery.toLowerCase())
	);
</script>

<div class="dropdown dropdown-left">
	<div
		tabindex="0"
		role="button"
		aria-haspopup="menu"
		aria-expanded={dropdownOpen}
		class="btn btn-sm btn-ghost gap-2 min-h-0 h-8 px-3"
		on:click={() => (dropdownOpen = !dropdownOpen)}
	>
		<MapIcon class="w-4 h-4" />
		<span class="text-xs font-medium">{getBasemapLabel(basemapType)}</span>
		<svg class="w-3 h-3 fill-none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
		</svg>
	</div>
	<ul
		class="dropdown-content z-20 menu p-2 shadow-lg bg-base-200 rounded-box w-56 max-h-96 overflow-y-auto"
	>
		<!-- Essential Maps -->
		<li class="menu-title">
			<span class="text-xs font-semibold opacity-60">Essential Maps</span>
		</li>
		{#each essentialMaps as option}
			<li>
				<button
					class="flex items-center gap-3 px-3 py-2 text-sm rounded-md transition-colors {basemapType ===
					option.value
						? 'bg-primary/10 font-medium'
						: ''}"
					on:pointerdown={(e) => {
						e.preventDefault();
						e.stopPropagation();
						selectBasemap(option.value);
					}}
					on:click={() => selectBasemap(option.value)}
					role="menuitem"
				>
					<span class="text-lg">{option.icon}</span>
					<span>{option.label}</span>
					{#if basemapType === option.value}
						<svg class="w-4 h-4 ml-auto text-primary" fill="currentColor" viewBox="0 0 20 20">
							<path
								fill-rule="evenodd"
								d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
								clip-rule="evenodd"
							/>
						</svg>
					{/if}
				</button>
			</li>
		{/each}

		<!-- Show Advanced Toggle -->
		<li class="mt-2">
			<button
				class="flex items-center gap-2 px-3 py-2 text-sm rounded-md transition-colors justify-center font-medium"
				on:click={() => (showAdvanced = !showAdvanced)}
			>
				{#if showAdvanced}
					<ChevronUpIcon class="w-4 h-4" />
					<span>Hide Advanced Maps</span>
				{:else}
					<ChevronDownIcon class="w-4 h-4" />
					<span>Show More Maps ({advancedMaps.length})</span>
				{/if}
			</button>
		</li>

		<!-- Advanced Maps Section -->
		{#if showAdvanced}
			<!-- Search Input -->
			<li class="mt-2 px-2">
				<div class="relative">
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search maps..."
						class="input input-sm input-bordered w-full pl-8"
					/>
					<MagnifyIcon class="w-4 h-4 absolute left-2 top-1/2 -translate-y-1/2 opacity-50" />
				</div>
			</li>

			<!-- Advanced Maps Title -->
			<li class="menu-title mt-2">
				<span class="text-xs font-semibold opacity-60">Advanced Maps</span>
			</li>

			<!-- Advanced Maps List -->
			{#if filteredAdvancedMaps.length === 0}
				<li class="px-3 py-2 text-sm text-center opacity-60">No maps found</li>
			{:else}
				{#each filteredAdvancedMaps as option}
					<li>
						<button
							class="flex items-center gap-3 px-3 py-2 text-sm rounded-md transition-colors {basemapType ===
							option.value
								? 'bg-primary/10 font-medium'
								: ''}"
							on:pointerdown={(e) => {
								e.preventDefault();
								e.stopPropagation();
								selectBasemap(option.value);
							}}
							on:click={() => selectBasemap(option.value)}
							role="menuitem"
						>
							<span class="text-lg">{option.icon}</span>
							<span>{option.label}</span>
							{#if basemapType === option.value}
								<svg class="w-4 h-4 ml-auto text-primary" fill="currentColor" viewBox="0 0 20 20">
									<path
										fill-rule="evenodd"
										d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
										clip-rule="evenodd"
									/>
								</svg>
							{/if}
						</button>
					</li>
				{/each}
			{/if}
		{/if}
	</ul>
</div>
