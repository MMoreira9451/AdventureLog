<script lang="ts">
	import LocationCard from '$lib/components/LocationCard.svelte';
	import type { PageData } from './$types';
	import { t } from 'svelte-i18n';
	import { getDifficultyBadgeClass } from '$lib/index';

	// Icons
	import MapMarkerDistance from '~icons/mdi/map-marker-distance';
	import TrendingUp from '~icons/mdi/trending-up';
	import MountainIcon from '~icons/mdi/image-filter-hdr';
	import RouteIcon from '~icons/mdi/routes';
	import CalendarClock from '~icons/mdi/calendar-clock';
	import Plus from '~icons/mdi/plus';

	export let data: PageData;

	const user = data.user;
	const recentAdventures = data.props.adventures;
	const stats = data.props.stats;

	// Extract trekking stats
	const trekkingStats = stats?.trekking || {};

	// Legacy stats for world travel section
	const legacyStats = {
		visited_country_count: stats?.visited_country_count || 0,
		visited_region_count: stats?.visited_region_count || 0,
		visited_city_count: stats?.visited_city_count || 0
	};
</script>

<svelte:head>
	<title>Dashboard | AdventureLog</title>
	<meta name="description" content="{$t('dashboard.meta_description')}" />
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-base-200 via-base-100 to-base-200">
	<div class="container mx-auto px-6 py-8">
		<!-- Welcome Section -->
		<div class="welcome-section mb-12">
			<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
				<div>
					<div class="flex items-center gap-4 mb-4">
						<div>
							<h1 class="text-4xl lg:text-5xl font-bold bg-clip-text text-primary">
								{$t('dashboard.welcome_back')}, {user?.first_name
									? `${user.first_name}`
									: user?.username}!
							</h1>
							<p class="text-lg text-base-content/60 mt-2">
								{#if trekkingStats.total_km_hiked > 0}
									{$t('dashboard.welcome_text_1')} <span class="font-semibold text-primary"
										>{trekkingStats.total_km_hiked || 0} {$t('dashboard.welcome_text_2')}</span
									>
									<span class="font-semibold text-primary"
										>{trekkingStats.summits_reached || 0}</span
									> {$t('dashboard.welcome_text_3')}
								{:else}
									{$t('dashboard.start_trekking_today')}
								{/if}
							</p>
						</div>
					</div>
				</div>

				<!-- Quick Action -->
				<div class="flex flex-col sm:flex-row gap-3">
					<a
						href="/locations"
						class="btn btn-primary btn-lg gap-2 shadow-lg hover:shadow-xl transition-all duration-300"
					>
						<Plus class="w-5 h-5" />
						{$t('map.add_location')}
					</a>
					<a href="/worldtravel" class="btn btn-outline btn-lg gap-2">
						<MapMarkerDistance class="w-5 h-5" />
						{$t('home.explore_world')}
					</a>
				</div>
			</div>
		</div>

		<!-- Main Trekking Stats Grid -->
		<div
			class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
		>
			<!-- Total Distance -->
			<div
				class="stat-card card bg-gradient-to-br from-primary/10 to-primary/5 shadow-xl border border-primary/20 hover:shadow-2xl transition-all duration-300"
			>
				<div class="card-body p-6">
					<div class="flex items-center justify-between">
						<div class="flex-1">
							<div class="stat-title text-primary/70 font-medium">
								{$t('dashboard.total_distance')}
							</div>
							<div class="stat-value text-3xl font-bold text-primary">
								{trekkingStats.total_km_hiked || 0} km
							</div>
							<div class="stat-desc text-primary/60 mt-2">{$t('dashboard.km_hiked')}</div>
						</div>
						<div class="p-4 bg-primary/20 rounded-2xl">
							<MapMarkerDistance class="w-8 h-8 text-primary" />
						</div>
					</div>
				</div>
			</div>

			<!-- Elevation Gain -->
			<div
				class="stat-card card bg-gradient-to-br from-success/10 to-success/5 shadow-xl border border-success/20 hover:shadow-2xl transition-all duration-300"
			>
				<div class="card-body p-6">
					<div class="flex items-center justify-between">
						<div class="flex-1">
							<div class="stat-title text-success/70 font-medium">
								{$t('dashboard.elevation_gain')}
							</div>
							<div class="stat-value text-3xl font-bold text-success">
								{Math.round(trekkingStats.total_elevation_gain || 0)} m
							</div>
							<div class="stat-desc text-success/60 mt-2">{$t('dashboard.meters_climbed')}</div>
						</div>
						<div class="p-4 bg-success/20 rounded-2xl">
							<TrendingUp class="w-8 h-8 text-success" />
						</div>
					</div>
				</div>
			</div>

			<!-- Summits Reached -->
			<div
				class="stat-card card bg-gradient-to-br from-info/10 to-info/5 shadow-xl border border-info/20 hover:shadow-2xl transition-all duration-300"
			>
				<div class="card-body p-6">
					<div class="flex items-center justify-between">
						<div class="flex-1">
							<div class="stat-title text-info/70 font-medium">{$t('dashboard.summits_reached')}</div>
							<div class="stat-value text-3xl font-bold text-info">
								{trekkingStats.summits_reached || 0}
							</div>
							<div class="stat-desc text-info/60 mt-2">{$t('dashboard.peaks_conquered')}</div>
						</div>
						<div class="p-4 bg-info/20 rounded-2xl">
							<MountainIcon class="w-8 h-8 text-info" />
						</div>
					</div>
				</div>
			</div>

			<!-- Routes Completed -->
			<div
				class="stat-card card bg-gradient-to-br from-warning/10 to-warning/5 shadow-xl border border-warning/20 hover:shadow-2xl transition-all duration-300"
			>
				<div class="card-body p-6">
					<div class="flex items-center justify-between">
						<div class="flex-1">
							<div class="stat-title text-warning/70 font-medium">
								{$t('dashboard.routes_completed')}
							</div>
							<div class="stat-value text-3xl font-bold text-warning">
								{trekkingStats.routes_completed || 0}
							</div>
							<div class="stat-desc text-warning/60 mt-2">
								{$t('dashboard.of_total', { values: { total: trekkingStats.total_routes || 0 } })}
							</div>
						</div>
						<div class="p-4 bg-warning/20 rounded-2xl">
							<RouteIcon class="w-8 h-8 text-warning" />
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Difficulty Breakdown -->
		{#if Object.keys(trekkingStats.difficulty_breakdown || {}).length > 0}
			<div class="mb-12">
				<div class="card bg-base-100 shadow-xl">
					<div class="card-body">
						<h2 class="card-title text-2xl mb-4">{$t('dashboard.routes_by_difficulty')}</h2>
						<div class="flex gap-3 flex-wrap">
							{#each Object.entries(trekkingStats.difficulty_breakdown) as [difficulty, count]}
								<div class="stat bg-base-200 rounded-lg p-4">
									<div class="stat-title text-xs">{$t(`difficulty.${difficulty}`)}</div>
									<div class="stat-value text-2xl {getDifficultyBadgeClass(difficulty).replace('badge-', 'text-')}">{count}</div>
								</div>
							{/each}
						</div>
					</div>
				</div>
			</div>
		{/if}

		<!-- Recent Trails Section -->
		{#if recentAdventures.length > 0}
			<div class="mb-8">
				<div class="flex items-center justify-between mb-6">
					<div class="flex items-center gap-3">
						<div class="p-2 bg-primary/10 rounded-xl">
							<CalendarClock class="w-6 h-6 text-primary" />
						</div>
						<div>
							<h2 class="text-3xl font-bold">{$t('dashboard.recent_trails')}</h2>
							<p class="text-base-content/60">{$t('dashboard.latest_trail_points')}</p>
						</div>
					</div>
					<a href="/locations" class="btn btn-ghost gap-2">
						{$t('dashboard.view_all')}
						<span class="badge badge-primary">{trekkingStats.total_trails || 0}</span>
					</a>
				</div>

				<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
					{#each recentAdventures as adventure}
						<div class="adventure-card">
							<LocationCard {adventure} user={data.user} readOnly />
						</div>
					{/each}
				</div>
			</div>
		{/if}

		<!-- Empty State / Inspiration -->
		{#if recentAdventures.length === 0}
			<div
				class="empty-state card bg-gradient-to-br from-base-100 to-base-200 shadow-2xl border border-base-300"
			>
				<div class="card-body p-12 text-center">
					<div class="flex justify-center mb-6">
						<div class="p-6 bg-primary/10 rounded-3xl">
							<MountainIcon class="w-16 h-16 text-primary" />
						</div>
					</div>

					<h2
						class="text-3xl font-bold mb-4 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent"
					>
						{$t('dashboard.no_trails_yet')}
					</h2>
					<p class="text-lg text-base-content/60 mb-8 max-w-md mx-auto leading-relaxed">
						{$t('dashboard.start_trekking_journey')}
					</p>

					<div class="flex flex-col sm:flex-row gap-4 justify-center">
						<a
							href="/locations"
							class="btn btn-primary btn-lg gap-2 shadow-lg hover:shadow-xl transition-all duration-300"
						>
							<Plus class="w-5 h-5" />
							{$t('map.add_location')}
						</a>
						<a href="/worldtravel" class="btn btn-outline btn-lg gap-2">
							<MapMarkerDistance class="w-5 h-5" />
							{$t('home.explore_world')}
						</a>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>
