<script lang="ts">
    import { skillNameMap } from "$lib/data/skill";
    import { statusNameMap } from "$lib/data/statuscondition";
    import { itemNameMap } from "$lib/data/item";
    import { onMount } from "svelte";
    import { base } from "$app/paths";

    let activeTab: "skills" | "status" | "items" = $state("skills");
    let searchQuery = $state("");

    let filteredSkills = $derived(
        Object.entries(skillNameMap)
            .filter(
                ([id, name]) =>
                    name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                    id.includes(searchQuery),
            )
            .map(([id, name]) => ({ id, name })),
    );

    let filteredStatus = $derived(
        Object.entries(statusNameMap)
            .filter(
                ([id, name]) =>
                    name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                    id.includes(searchQuery),
            )
            .map(([id, name]) => ({ id, name })),
    );

    let filteredItems = $derived(
        Object.entries(itemNameMap)
            .filter(
                ([id, name]) =>
                    name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                    id.includes(searchQuery),
            )
            .slice(0, 100)
            .map(([id, name]) => ({ id, name })),
    );

    // Demo fetch request
    let demoData: any = $state(null);
    let demoLoading = $state(false);

    async function testFetch(type: "skill" | "status" | "item", id: string) {
        demoLoading = true;
        try {
            const res = await fetch(`${base}/api/${type}/${id}`);
            if (res.ok) {
                demoData = await res.json();
            } else {
                demoData = { error: "Not found" };
            }
        } catch (e) {
            demoData = { error: "Network error" };
        }
        demoLoading = false;
    }
</script>

<div
    class="min-h-screen bg-gray-900 text-gray-100 font-sans selection:bg-indigo-500 selection:text-white"
>
    <header
        class="bg-gray-800 border-b border-gray-700 p-6 sticky top-0 z-10 shadow-lg"
    >
        <div
            class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4"
        >
            <div class="flex items-center gap-3">
                <div
                    class="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center font-bold text-xl shadow-inner border border-indigo-400"
                >
                    F
                </div>
                <div>
                    <h1
                        class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400"
                    >
                        Funnychart Assets
                    </h1>
                    <p class="text-xs text-gray-400">
                        Skill & Status Condition Viewer
                    </p>
                </div>
            </div>

            <div
                class="flex gap-2 bg-gray-900 p-1 rounded-lg border border-gray-700"
            >
                <button
                    class="px-4 py-2 rounded-md font-medium transition-all {activeTab ===
                    'skills'
                        ? 'bg-indigo-600 text-white shadow'
                        : 'text-gray-400 hover:text-gray-200'}"
                    onclick={() => (activeTab = "skills")}
                >
                    Skills <span
                        class="ml-1 text-xs px-1.5 py-0.5 rounded-full bg-gray-800 text-gray-300"
                        >{Object.keys(skillNameMap).length}</span
                    >
                </button>
                <button
                    class="px-4 py-2 rounded-md font-medium transition-all {activeTab ===
                    'status'
                        ? 'bg-purple-600 text-white shadow'
                        : 'text-gray-400 hover:text-gray-200'}"
                    onclick={() => (activeTab = "status")}
                >
                    Status <span
                        class="ml-1 text-xs px-1.5 py-0.5 rounded-full bg-gray-800 text-gray-300"
                        >{Object.keys(statusNameMap).length}</span
                    >
                </button>
                <button
                    class="px-4 py-2 rounded-md font-medium transition-all {activeTab ===
                    'items'
                        ? 'bg-emerald-600 text-white shadow'
                        : 'text-gray-400 hover:text-gray-200'}"
                    onclick={() => (activeTab = "items")}
                >
                    Items <span
                        class="ml-1 text-xs px-1.5 py-0.5 rounded-full bg-gray-800 text-gray-300"
                        >{Object.keys(itemNameMap).length}</span
                    >
                </button>
            </div>

            <div class="relative w-full md:w-64">
                <div
                    class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                >
                    <svg
                        class="h-5 w-5 text-gray-500"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path
                            fill-rule="evenodd"
                            d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </div>
                <input
                    type="text"
                    bind:value={searchQuery}
                    placeholder="Search by name or ID..."
                    class="block w-full pl-10 pr-3 py-2 border border-gray-700 rounded-lg leading-5 bg-gray-800 text-gray-300 placeholder-gray-500 focus:outline-none focus:bg-gray-900 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors"
                />
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto p-6">
        <!-- API Demo Section -->
        <div
            class="mb-10 bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-md relative overflow-hidden"
        >
            <div
                class="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-indigo-500 to-purple-500"
            ></div>
            <h2 class="text-xl font-bold mb-2">API Endpoints (Prerendered)</h2>
            <p class="text-gray-400 mb-4 text-sm">
                Fetch JSON data using the generated static routes. Perfect for
                third-party tools!
            </p>

            <div class="flex flex-col md:flex-row gap-4">
                <div class="flex-1 space-y-3">
                    <div
                        class="flex items-center gap-2 bg-gray-900 p-3 rounded border border-gray-700 font-mono text-sm"
                    >
                        <span class="text-green-400 font-bold">GET</span>
                        <span class="text-gray-300">/api/skill/[id]</span>
                        <button
                            class="ml-auto bg-gray-800 hover:bg-gray-700 px-3 py-1 rounded text-xs transition"
                            onclick={() => testFetch("skill", "10001")}
                            >Test 10001</button
                        >
                    </div>
                    <div
                        class="flex items-center gap-2 bg-gray-900 p-3 rounded border border-gray-700 font-mono text-sm"
                    >
                        <span class="text-green-400 font-bold">GET</span>
                        <span class="text-gray-300">/api/status/[id]</span>
                        <button
                            class="ml-auto bg-gray-800 hover:bg-gray-700 px-3 py-1 rounded text-xs transition"
                            onclick={() => testFetch("status", "1")}
                            >Test 1</button
                        >
                    </div>
                    <div
                        class="flex items-center gap-2 bg-gray-900 p-3 rounded border border-gray-700 font-mono text-sm"
                    >
                        <span class="text-green-400 font-bold">GET</span>
                        <span class="text-gray-300">/api/item/[id]</span>
                        <button
                            class="ml-auto bg-gray-800 hover:bg-gray-700 px-3 py-1 rounded text-xs transition"
                            onclick={() => testFetch("item", "1000")}
                            >Test 1000</button
                        >
                    </div>
                </div>

                <div
                    class="flex-1 bg-black rounded-lg border border-gray-700 p-4 font-mono text-xs overflow-auto h-32 relative"
                >
                    <span class="absolute top-2 right-2 text-gray-600"
                        >Response</span
                    >
                    {#if demoLoading}
                        <div class="text-gray-500 animate-pulse">
                            Loading...
                        </div>
                    {:else if demoData}
                        <pre class="text-green-300">{JSON.stringify(
                                demoData,
                                null,
                                2,
                            )}</pre>
                    {:else}
                        <div class="text-gray-600 italic">
                            Click a test button to fetch data
                        </div>
                    {/if}
                </div>
            </div>
        </div>

        <!-- Grid View -->
        {#if activeTab === "skills"}
            <div
                class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4"
            >
                {#each filteredSkills as skill (skill.id)}
                    <div
                        class="group bg-gray-800 hover:bg-gray-750 border border-gray-700 hover:border-indigo-500 rounded-xl p-4 flex flex-col items-center text-center transition-all duration-300 hover:shadow-[0_0_15px_rgba(99,102,241,0.2)] hover:-translate-y-1"
                    >
                        <div
                            class="w-16 h-16 mb-3 rounded-lg bg-gray-900 shadow-inner flex items-center justify-center p-2 relative overflow-hidden group-hover:ring-2 ring-indigo-500/50 transition-all"
                        >
                            <img
                                src="{base}/res/skillimage/us/{skill.id}.png"
                                alt={skill.name}
                                class="max-w-full max-h-full object-contain"
                                loading="lazy"
                                onerror={(e) =>
                                    ((
                                        e.currentTarget as HTMLImageElement
                                    ).style.display = "none")}
                            />
                        </div>
                        <h3
                            class="font-medium text-sm text-gray-200 line-clamp-2 leading-tight mb-1"
                            title={skill.name}
                        >
                            {skill.name}
                        </h3>
                        <span
                            class="text-xs font-mono text-indigo-400 bg-indigo-400/10 px-2 py-0.5 rounded mt-auto"
                            >{skill.id}</span
                    >
                    </div>
                {/each}
                {#if filteredSkills.length === 0}
                    <div class="col-span-full py-12 text-center text-gray-500">
                        No skills found matching "{searchQuery}"
                    </div>
                {/if}
            </div>
        {:else if activeTab === "status"}
            <div
                class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4"
            >
                {#each filteredStatus as status (status.id)}
                    <div
                        class="group bg-gray-800 hover:bg-gray-750 border border-gray-700 hover:border-purple-500 rounded-xl p-4 flex flex-col items-center text-center transition-all duration-300 hover:shadow-[0_0_15px_rgba(168,85,247,0.2)] hover:-translate-y-1"
                    >
                        <div
                            class="w-12 h-12 mb-3 rounded-lg bg-gray-900 shadow-inner flex items-center justify-center p-2 relative overflow-hidden group-hover:ring-2 ring-purple-500/50 transition-all"
                        >
                            <img
                                src="{base}/res/status/{status.id}.png"
                                alt={status.name}
                                class="scale-[1.5] pixelated object-contain"
                                loading="lazy"
                                onerror={(e) =>
                                    ((
                                        e.currentTarget as HTMLImageElement
                                    ).style.display = "none")}
                            />
                        </div>
                        <h3
                            class="font-medium text-sm text-gray-200 line-clamp-2 leading-tight mb-1"
                            title={status.name}
                        >
                            {status.name}
                        </h3>
                        <span
                            class="text-xs font-mono text-purple-400 bg-purple-400/10 px-2 py-0.5 rounded mt-auto"
                            >{status.id}</span
                        >
                    </div>
                {/each}
                {#if filteredStatus.length === 0}
                    <div class="col-span-full py-12 text-center text-gray-500">
                        No statuses found matching "{searchQuery}"
                    </div>
                {/if}
            </div>
        {:else}
            <div
                class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4"
            >
                {#each filteredItems as item (item.id)}
                    <div
                        class="group bg-gray-800 hover:bg-gray-750 border border-gray-700 hover:border-emerald-500 rounded-xl p-4 flex flex-col items-center text-center transition-all duration-300 hover:shadow-[0_0_15px_rgba(16,185,129,0.2)] hover:-translate-y-1"
                    >
                        <h3
                            class="font-medium text-sm text-gray-200 line-clamp-3 leading-tight mb-2"
                            title={item.name}
                        >
                            {item.name}
                        </h3>
                        <span
                            class="text-xs font-mono text-emerald-400 bg-emerald-400/10 px-2 py-0.5 rounded mt-auto"
                            >{item.id}</span
                        >
                    </div>
                {/each}
                {#if filteredItems.length === 0}
                    <div class="col-span-full py-12 text-center text-gray-500">
                        No items found matching "{searchQuery}"
                    </div>
                {/if}
            </div>
            {#if filteredItems.length >= 100}
                <div class="mt-8 text-center text-gray-500 text-sm italic">
                    Showing first 100 results... refine search for more.
                </div>
            {/if}
        {/if}
    </main>
</div>

<style>
    /* Prevent image blur when scaling small icons */
    .pixelated {
        image-rendering: pixelated;
    }
</style>
