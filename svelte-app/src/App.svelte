<script>
    import { onMount } from 'svelte';

    let nsec_key = ''; 
    let scan_status = 'Väntar på din nyckel...';
    let results = [];

    async function startScan() {
        if (!nsec_key) {
            scan_status = 'FEL: Vänligen ange din hemliga Nostr-nyckel (nsec).';
            return;
        }

        scan_status = 'Initierar aggressiv skanning via krypterad Nostr-autentisering... 🕵️';

        try {
            const response = await fetch('/.netlify/functions/scan-init', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    nsec: nsec_key,
                    action: 'START_SCAN',
                })
            });

            if (!response.ok) {
                throw new Error('Backend-fel eller ogiltig Nostr-nyckel.');
            }

            const data = await response.json();
            results = data.prioritized_list; 
            scan_status = 'Skanning slutförd. Fullständig Spår-Logg genererad.';
        } catch (error) {
            scan_status = `Kritiskt fel: ${error.message}. Kontrollera din nsec.`;
            console.error(error);
        }
    }
</script>

<main>
    <h1>S-Wipe 2.0: Syntetisk Livsform</h1>
    <p class="status-msg">{scan_status}</p>

    <div class="input-group">
        <label for="nsec">Master Nostr Sekreta Nyckel (nsec):</label>
        <input id="nsec" type="password" bind:value={nsec_key} placeholder="nsec1..." />
        <button on:click={startScan}>Starta Aggressiv Skanning 💥</button>
    </div>

    {#if results.length > 0}
    <hr>
    <h2>Prioriterad Åtgärdslista (Fullständig Spår-Logg)</h2>
        <p class="action-note">Välj **Godkänn & Skicka Individuellt** för maximal kontroll.</p>

        {#each results as item}
            <div class="result-item" class:red={item.difficulty === 'Röd'} class:yellow={item.difficulty === 'Gul'}>
                <h3>{item.service} ({item.action_method})</h3>
                <p>Status: {item.status}. Svårighet: <strong>{item.difficulty}</strong>. Nästa steg: {item.next_step}</p>
                <button class="action-button">Godkänn & Skicka Brev</button>
            </div>
        {/each}
    {/if}
</main>

<style>
    :global(body) { background-color: #1a1a1a; color: #00ff00; font-family: 'Courier New', monospace; padding: 20px; }
    h1 { color: #88ff88; border-bottom: 2px solid #88ff88; padding-bottom: 5px; }
    h2, h3 { color: #00ff00; }
    .status-msg { color: #ffff00; }

    .input-group { margin-bottom: 20px; }
    input[type="password"] { 
        padding: 10px; width: 80%; margin-bottom: 10px; 
        background: #333; color: #00ff00; border: 1px solid #00ff00; 
    }
    button { 
        padding: 10px 20px; background: #00ff00; color: black; border: none; cursor: pointer; 
        font-weight: bold; margin-left: 10px; 
    }
    .result-item { 
        border: 1px solid #333; padding: 15px; margin-bottom: 10px; 
        background-color: #2a2a2a; 
    }
    .result-item.red { border-left: 5px solid red; }
    .result-item.yellow { border-left: 5px solid yellow; }
    .action-button { background: #ff4500; color: white; margin-top: 10px; }
    .action-note { color: #ff8c00; font-weight: bold; }
</style>
