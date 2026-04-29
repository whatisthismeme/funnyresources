import { skillNameMap } from '$lib/data/skill';
import { base } from '$app/paths';

export function entries() {
    return Object.keys(skillNameMap).map((id) => ({ id }));
}

export const prerender = true;

export async function GET({ params }: any) {
    const { id } = params;
    const name = skillNameMap[Number(id)];
    
    if (!name) {
        return new Response('Not found', { status: 404 });
    }

    const data = {
        id: Number(id),
        name,
        imageUrl: `${base}/res/skillimage/us/${id}.png`
    };

    return new Response(JSON.stringify(data), {
        headers: {
            'Content-Type': 'text/plain'
        }
    });
}
