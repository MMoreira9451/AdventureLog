<script lang="ts">
	import { t } from 'svelte-i18n';
	import { addToast } from '$lib/toasts';

	export let itemId: string; // location ID
	export let onTrailCreated: (trail: any) => void;
	export let onCancel: () => void;

	let trailName: string = '';
	let trailLink: string = '';
	let trailWandererId: string = '';
	let trailType: 'external' | 'wanderer' = 'external';
	let trailError: string = '';
	let isLoading: boolean = false;

	async function createTrail() {
		isLoading = true;
		trailError = '';

		// Validate based on selected trail type
		if (trailType === 'external' && !trailLink.trim()) {
			trailError = $t('adventures.trail_link_required');
			isLoading = false;
			return;
		} else if (trailType === 'wanderer' && !trailWandererId.trim()) {
			trailError = 'Wanderer trail ID required';
			isLoading = false;
			return;
		}

		const trailData = {
			name: trailName.trim(),
			location: itemId,
			link: trailType === 'external' ? trailLink.trim() : null,
			wanderer_id: trailType === 'wanderer' ? trailWandererId.trim() : null
		};

		try {
			const res = await fetch('/api/trails/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(trailData)
			});

			if (res.ok) {
				const newTrail = await res.json();
				addToast('success', $t('adventures.trail_created_successfully'));
				onTrailCreated(newTrail);
				resetForm();
			} else {
				const errorData = await res.json();
				// Extract specific error message from backend
				let errorMessage = 'Failed to create trail';
				if (errorData.detail) {
					errorMessage = errorData.detail;
				} else if (errorData.non_field_errors && errorData.non_field_errors.length > 0) {
					errorMessage = errorData.non_field_errors[0];
				} else if (errorData.link && errorData.link.length > 0) {
					errorMessage = errorData.link[0];
				} else if (errorData.wanderer_id && errorData.wanderer_id.length > 0) {
					errorMessage = errorData.wanderer_id[0];
				}
				throw new Error(errorMessage);
			}
		} catch (error) {
			console.error('Trail creation error:', error);
			trailError = error instanceof Error ? error.message : 'Failed to create trail';
			addToast('error', $t('adventures.trail_creation_failed'));
		} finally {
			isLoading = false;
		}
	}

	function resetForm() {
		trailName = '';
		trailLink = '';
		trailWandererId = '';
		trailType = 'external';
		trailError = '';
	}

	function handleCancel() {
		resetForm();
		onCancel();
	}
</script>

<div class="bg-accent/5 p-4 rounded-lg border border-accent/20 mb-6">
	<h4 class="font-medium mb-3 text-accent">{$t('adventures.add_new_trail')}</h4>
	<div class="grid gap-3">
		<!-- Trail Name -->
		<input
			type="text"
			bind:value={trailName}
			class="input input-bordered"
			placeholder="Trail name"
			disabled={isLoading}
		/>

		<!-- Trail Type Selector -->
		<div class="form-control">
			<label class="label cursor-pointer justify-start gap-3">
				<input
					type="radio"
					bind:group={trailType}
					value="external"
					class="radio radio-accent"
					disabled={isLoading}
				/>
				<span class="label-text">{$t('adventures.external_link')}</span>
			</label>
			<label class="label cursor-pointer justify-start gap-3">
				<input
					type="radio"
					bind:group={trailType}
					value="wanderer"
					class="radio radio-accent"
					disabled={isLoading}
				/>
				<span class="label-text">Wanderer Trail</span>
			</label>
		</div>

		<!-- External Link Input -->
		{#if trailType === 'external'}
			<input
				type="url"
				bind:value={trailLink}
				class="input input-bordered"
				placeholder={$t('adventures.external_link') + ' (AllTrails, Trailforks, etc.)'}
				disabled={isLoading}
			/>
		{/if}

		<!-- Wanderer ID Input -->
		{#if trailType === 'wanderer'}
			<input
				type="text"
				bind:value={trailWandererId}
				class="input input-bordered"
				placeholder="Wanderer Trail ID"
				disabled={isLoading}
			/>
		{/if}

		{#if trailError}
			<div class="alert alert-error py-2">
				<span class="text-sm">{trailError}</span>
			</div>
		{/if}
		<div class="flex gap-2 justify-end">
			<button class="btn btn-ghost btn-sm" disabled={isLoading} on:click={handleCancel}>
				{$t('adventures.cancel')}
			</button>
			<button
				class="btn btn-accent btn-sm"
				class:loading={isLoading}
				disabled={isLoading ||
					!trailName.trim() ||
					(trailType === 'external' && !trailLink.trim()) ||
					(trailType === 'wanderer' && !trailWandererId.trim())}
				on:click={createTrail}
			>
				{$t('adventures.create_trail')}
			</button>
		</div>
	</div>
</div>
