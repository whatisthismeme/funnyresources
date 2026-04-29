import { json } from '@sveltejs/kit';
import { statusNameMap } from '$lib/data/statuscondition';

export function entries() {
    return Object.keys(statusNameMap).map((id) => ({ id }));
}

export const prerender = true;

export async function GET({ params }: any) {
    const { id } = params;
    const name = statusNameMap[Number(id)];
    
    if (!name) {
        return new Response('Not found', { status: 404 });
    }

    return json({
        id: Number(id),
        name,
        imageUrl: `/res/status/${id}.png`
    });
}
