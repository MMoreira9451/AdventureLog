<script lang="ts">
	import type { Map } from 'maplibre-gl';
	import { onMount } from 'svelte';

	import ThreeDRotationIcon from '~icons/mdi/rotate-3d-variant';
	import CompassIcon from '~icons/mdi/compass';
	import TerrainIcon from '~icons/mdi/terrain';
	import ResetIcon from '~icons/mdi/refresh';

	export let map: Map | null = null;

	let pitch = 0; // 0-60 degrees
	let bearing = 0; // 0-360 degrees
	let terrainExaggeration = 1.5; // 1.0-3.0x
	let isExpanded = false;

	// Initialize values from map when available
	$: if (map) {
		pitch = map.getPitch();
		bearing = map.getBearing();
	}

	function updatePitch(value: number) {
		if (!map) return;
		pitch = value;
		map.setPitch(pitch);
	}

	function updateBearing(value: number) {
		if (!map) return;
		bearing = value;
		map.setBearing(bearing);
	}

	function updateTerrainExaggeration(value: number) {
		if (!map) return;
		terrainExaggeration = value;

		// Update terrain exaggeration if terrain is enabled
		const terrain = map.getTerrain();
		if (terrain) {
			map.setTerrain({
				source: 'terrain',
				exaggeration: terrainExaggeration
			});
		}
	}

	function resetTo2D() {
		if (!map) return;
		pitch = 0;
		bearing = 0;
		terrainExaggeration = 1.5;

		map.easeTo({
			pitch: 0,
			bearing: 0,
			duration: 1000
		});

		// Reset terrain exaggeration
		const terrain = map.getTerrain();
		if (terrain) {
			map.setTerrain({
				source: 'terrain',
				exaggeration: 1.5
			});
		}
	}

	function enable3DView() {
		if (!map) return;
		pitch = 60;
		bearing = 0;
		terrainExaggeration = 2.0;

		map.easeTo({
			pitch: 60,
			bearing: 0,
			duration: 1000
		});

		// Enable terrain if not already enabled
		const terrain = map.getTerrain();
		if (!terrain) {
			map.setTerrain({
				source: 'terrain',
				exaggeration: 2.0
			});
		} else {
			map.setTerrain({
				source: 'terrain',
				exaggeration: 2.0
			});
		}
	}
</script>

<div class="3d-controls bg-base-200 rounded-lg shadow-lg p-3">
	<!-- Toggle Button -->
	<button
		class="btn btn-sm btn-ghost w-full gap-2 justify-between"
		on:click={() => (isExpanded = !isExpanded)}
	>
		<div class="flex items-center gap-2">
			<ThreeDRotationIcon class="w-4 h-4" />
			<span class="text-xs font-medium">3D Controls</span>
		</div>
		<svg
			class="w-3 h-3 transition-transform {isExpanded ? 'rotate-180' : ''}"
			fill="none"
			stroke="currentColor"
			viewBox="0 0 24 24"
		>
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
		</svg>
	</button>

	{#if isExpanded}
		<div class="mt-3 space-y-4">
			<!-- Quick Actions -->
			<div class="flex gap-2">
				<button class="btn btn-xs btn-accent flex-1" on:click={enable3DView}>
					Enable 3D
				</button>
				<button class="btn btn-xs btn-ghost flex-1" on:click={resetTo2D}>
					<ResetIcon class="w-3 h-3 mr-1" />
					Reset 2D
				</button>
			</div>

			<!-- Pitch Slider -->
			<div class="form-control">
				<label class="label py-1">
					<span class="label-text text-xs flex items-center gap-1">
						<TerrainIcon class="w-3 h-3" />
						Pitch (Tilt): {pitch.toFixed(0)}°
					</span>
				</label>
				<input
					type="range"
					min="0"
					max="60"
					bind:value={pitch}
					on:input={(e) => updatePitch(Number(e.currentTarget.value))}
					class="range range-xs range-accent"
				/>
				<div class="flex justify-between text-xs opacity-50 px-1 mt-1">
					<span>0°</span>
					<span>60°</span>
				</div>
			</div>

			<!-- Bearing Slider -->
			<div class="form-control">
				<label class="label py-1">
					<span class="label-text text-xs flex items-center gap-1">
						<CompassIcon class="w-3 h-3" />
						Bearing (Rotation): {bearing.toFixed(0)}°
					</span>
				</label>
				<input
					type="range"
					min="0"
					max="360"
					bind:value={bearing}
					on:input={(e) => updateBearing(Number(e.currentTarget.value))}
					class="range range-xs range-accent"
				/>
				<div class="flex justify-between text-xs opacity-50 px-1 mt-1">
					<span>N (0°)</span>
					<span>S (180°)</span>
					<span>N (360°)</span>
				</div>
			</div>

			<!-- Terrain Exaggeration Slider -->
			<div class="form-control">
				<label class="label py-1">
					<span class="label-text text-xs flex items-center gap-1">
						<ThreeDRotationIcon class="w-3 h-3" />
						Terrain Height: {terrainExaggeration.toFixed(1)}x
					</span>
				</label>
				<input
					type="range"
					min="1"
					max="3"
					step="0.1"
					bind:value={terrainExaggeration}
					on:input={(e) => updateTerrainExaggeration(Number(e.currentTarget.value))}
					class="range range-xs range-accent"
				/>
				<div class="flex justify-between text-xs opacity-50 px-1 mt-1">
					<span>1.0x</span>
					<span>2.0x</span>
					<span>3.0x</span>
				</div>
			</div>

			<!-- Help Text -->
			<div class="text-xs opacity-60 px-1">
				<p>💡 Tip: Use pitch for 3D view and bearing to rotate the map</p>
			</div>
		</div>
	{/if}
</div>

<style>
	.3d-controls {
		min-width: 200px;
		max-width: 280px;
	}
</style>
