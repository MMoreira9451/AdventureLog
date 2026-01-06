import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
const PUBLIC_SERVER_URL = process.env['PUBLIC_SERVER_URL'];
import type { Location } from '$lib/types';

const serverEndpoint = PUBLIC_SERVER_URL || 'http://localhost:8000';

export const load = (async (event) => {
	if (!event.locals.user) {
		return redirect(302, '/login');
	} else {
		let recent_trails: Location[] = [];

		// Fetch recent trails (6 for dashboard display)
		let initialFetch = await event.fetch(
			`${serverEndpoint}/api/locations/?ordering=-created_at&limit=6`,
			{
				headers: {
					Cookie: `sessionid=${event.cookies.get('sessionid')}`
				},
				credentials: 'include'
			}
		);

		let stats = null;

		// Fetch trekking stats
		let res = await event.fetch(
			`${serverEndpoint}/api/stats/counts/${event.locals.user.username}/`,
			{
				headers: {
					Cookie: `sessionid=${event.cookies.get('sessionid')}`
				}
			}
		);
		if (!res.ok) {
			console.error('Failed to fetch user stats');
		} else {
			stats = await res.json();
		}

		if (!initialFetch.ok) {
			let error_message = await initialFetch.json();
			console.error(error_message);
			console.error('Failed to fetch recent trails');
			return redirect(302, '/login');
		} else {
			let res = await initialFetch.json();
			recent_trails = res.results as Location[];
		}

		return {
			props: {
				adventures: recent_trails, // Keep as 'adventures' for backward compatibility
				stats
			}
		};
	}
}) satisfies PageServerLoad;
