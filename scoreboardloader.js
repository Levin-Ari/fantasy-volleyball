//Load data and populate tables
async function loadData(){
    try {
        // Fetch both JSON files
        const[teamsResponse, playersResponse] = await Promise.all([
            fetch('teams_output.json'),
            fetch('players_output.json')
        ]);

        if (!teamsResponse.ok || !playersResponse.ok) {
            throw new Error('Failed to load data')
        }

        const teams = await teamsResponse.json();
        const players = await playersResponse.json();

        // Populate tables
        populateTopTeams(teams.slice(0, 5));
        populateTopPlayers(players.slice(0, 5));
        populateFullTeams(teams);
        populateFullPlayers(players);

        //Hide loading, show content
        document.getElementById('loading').style.display = 'none'
        document.getElementById('content').style.display = 'block';
    
    } catch(error) {
        console.error('Error loading data:', error)
        document.getElementById('loading').style.display = 'none';
        const errorDiv = document.getElementById('error')
        errorDiv.textContent = `Error loading data: ${error.message}. Contact Ari with a bug report.`
    }
}

function populateTopTeams(teams) {
    const tbody = document.getElementById('top-teams-body');
    tbody.innerHTML = teams.map((team, index) =>`
    <tr>
        <td class="rank">${index + 1}</td>
        <td>${team.team_name}</td>
        <td class="points">${team['total points']}</td>
    `).join('');
}

function populateTopPlayers(players) {
    const tbody = document.getElementById('top-players-body');
    tbody.innerHTML = players.map((player, index) => `
    <tr>
        <td class="rank">${index + 1}</td>
        <td>${player.name}</td>
        <td>${player.team}</td>
        <td class="points">${player.points}</td>
    </tr>
    `).join('');
}

function populateFullTeams(teams) {
    const tbody = document.getElementById('full-teams-body');
    tbody.innerHTML = teams.map((team, index) => `
        <tr>
            <td class="rank">${index + 1}</td>
            <td>${team.team_name}</td>
            <td>${team.s1} (${team.s1_points})</td>
            <td>${team.h1} (${team.h1_points})</td>
            <td>${team.m1} (${team.m1_points})</td>
            <td>${team.l1} (${team.l1_points})</td>
            <td>${team.s2} (${team.s2_points})</td>
            <td>${team.h2} (${team.h2_points})</td>
            <td>${team.m2} (${team.m2_points})</td>
            <td>${team.w1} (${team.w1_points})</td>
            <td class="points">${team['total points']}</td>
        </tr>
    `).join('');
}

function populateFullPlayers(players) {
    const tbody = document.getElementById('full-players-body');
    tbody.innerHTML = players.map((player, index) => `
        <tr>
            <td class="rank">${index + 1}</td>
            <td>${player.name}</td>
            <td>${player.team}</td>
            <td>${player.assists}</td>
            <td>${player.kills}</td>
            <td>${player.digs}</td>
            <td>${player.blocks}</td>
            <td>${player.aces}</td>
            <td class="points">${player.points}</td>
            <td>${player['points per set'].toFixed(1)}</td>
        </tr>
    `).join('');
}

loadData();