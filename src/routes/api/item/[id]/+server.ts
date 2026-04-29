import { itemNameMap } from '$lib/data/item';

export function entries() {
    return Object.keys(itemNameMap).map((id) => ({ id }));
}

export const prerender = true;

export async function GET({ params }: any) {
    const { id } = params;
    const name = itemNameMap[Number(id)];
    
    if (!name) {
        return new Response('Not found', { status: 404 });
    }

    const data = {
        id: Number(id),
        name
    };

    return new Response(JSON.stringify(data), {
        headers: {
            'Content-Type': 'text/plain'
        }
    });
}
