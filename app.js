/* =============================================================================
   PROJETO INTEGRADO III - SPRINT 1
   Lógica do Dashboard (Consumo da API REST Backend e Renderização de Gráficos/Mapa)
   Membro Responsável: Victor (Frontend / Scrum Master)
   ============================================================================= */

const API_BASE_URL = 'http://localhost:8000';

let map = null;
let chartEvolucao = null;
let chartTipos = null;
let chartCausas = null;
let chartRodovias = null;

let currentPage = 0;
const pageSize = 10;
let tableData = [];

// Inicialização da Aplicação quando o DOM carrega
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    loadDashboardData();
    setupEventListeners();
});

// 1. Inicializar Mapa Interativo Leaflet
function initMap() {
    // Centro do Brasil
    map = L.map('map').setView([-14.2350, -51.9253], 4);

    // Camada de Mapa Dark Tile
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);
}

// 2. Carregar Dados de Todos os Endpoints da API REST
async function loadDashboardData() {
    try {
        await checkHealth();
        await Promise.all([
            fetchKPIs(),
            fetchEvolucaoMensal(),
            fetchTiposAcidente(),
            fetchCausasAcidente(),
            fetchRiscoEstado(),
            fetchRodoviasCriticas(),
            fetchOcorrencias()
        ]);
    } catch (err) {
        console.warn("Utilizando dados de demonstração (Backend offline ou inicializando).", err);
    }
}

// Verificar conexão da API
async function checkHealth() {
    const statusText = document.getElementById('api-status-text');
    try {
        const res = await fetch(`${API_BASE_URL}/health`);
        const data = await res.json();
        if (data.status === 'online') {
            statusText.textContent = `API Conectada (${data.database})`;
            statusText.style.color = '#2a9d8f';
        }
    } catch (e) {
        statusText.textContent = 'Modo Demonstrativo (API Offline)';
        statusText.style.color = '#ffb703';
    }
}

// Fetch 1: KPIs
async function fetchKPIs() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/kpis`);
        const data = await res.json();
        
        document.getElementById('kpi-total-acidentes').textContent = Number(data.total_acidentes).toLocaleString('pt-BR');
        document.getElementById('kpi-total-mortos').textContent = Number(data.total_mortos).toLocaleString('pt-BR');
        document.getElementById('kpi-total-feridos').textContent = Number(data.total_feridos).toLocaleString('pt-BR');
        document.getElementById('kpi-icr-medio').textContent = Number(data.indice_risco_medio || 4.45).toLocaleString('pt-BR', {minimumFractionDigits: 2});
        document.getElementById('kpi-detalhe-feridos').textContent = `${Number(data.total_feridos_graves || 0).toLocaleString('pt-BR')} graves | ${Number(data.total_feridos_leves || 0).toLocaleString('pt-BR')} leves`;
    } catch (e) {
        console.error("Erro ao buscar KPIs:", e);
    }
}

// Fetch 2: Evolução Mensal (Linha/Área)
async function fetchEvolucaoMensal() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/evolucao-mensal`);
        const data = await res.json();

        const labels = data.map(d => d.mes_nome);
        const acidentes = data.map(d => d.total_acidentes);
        const mortos = data.map(d => d.total_mortos);

        renderChartEvolucao(labels, acidentes, mortos);
    } catch (e) {
        console.error("Erro ao buscar Evolução Mensal:", e);
    }
}

function renderChartEvolucao(labels, acidentes, mortos) {
    const ctx = document.getElementById('chart-evolucao').getContext('2d');
    if (chartEvolucao) chartEvolucao.destroy();

    chartEvolucao = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Acidentes',
                    data: acidentes,
                    borderColor: '#3a86ef',
                    backgroundColor: 'rgba(58, 134, 239, 0.15)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Vítimas Fatais',
                    data: mortos,
                    borderColor: '#e63946',
                    backgroundColor: 'rgba(230, 57, 70, 0.2)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#94a3b8' } } },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
            }
        }
    });
}

// Fetch 3: Tipos de Acidente (Rosca)
async function fetchTiposAcidente() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/tipos-acidente`);
        const data = await res.json();

        const labels = data.map(d => d.tipo_acidente);
        const valores = data.map(d => d.total_ocorrencias);

        renderChartTipos(labels, valores);
    } catch (e) {
        console.error("Erro ao buscar Tipos de Acidente:", e);
    }
}

function renderChartTipos(labels, valores) {
    const ctx = document.getElementById('chart-tipos').getContext('2d');
    if (chartTipos) chartTipos.destroy();

    chartTipos = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: valores,
                backgroundColor: ['#3a86ef', '#00b4d8', '#ffb703', '#fb8500', '#e63946', '#8d99ae']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', font: { size: 10 } } } }
        }
    });
}

// Fetch 4: Causas (Barras Horizontais)
async function fetchCausasAcidente() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/causas-acidente`);
        const data = await res.json();

        const labels = data.map(d => d.causa_acidente);
        const valores = data.map(d => d.total_ocorrencias);

        renderChartCausas(labels, valores);
    } catch (e) {
        console.error("Erro ao buscar Causas:", e);
    }
}

function renderChartCausas(labels, valores) {
    const ctx = document.getElementById('chart-causas').getContext('2d');
    if (chartCausas) chartCausas.destroy();

    chartCausas = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ocorrências',
                data: valores,
                backgroundColor: '#ffb703'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { display: false } }
            }
        }
    });
}

// Fetch 5: Risco por Estado (Popula Mapa Leaflet)
async function fetchRiscoEstado() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/risco-estado`);
        const data = await res.json();

        data.forEach(item => {
            if (item.lat_centroide && item.lng_centroide) {
                const color = item.icr_total > 20000 ? '#e63946' : item.icr_total > 12000 ? '#ffb703' : '#00b4d8';
                
                const circle = L.circleMarker([item.lat_centroide, item.lng_centroide], {
                    radius: Math.min(Math.max(item.total_acidentes / 400, 8), 25),
                    fillColor: color,
                    color: '#fff',
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.7
                }).addTo(map);

                circle.bindPopup(`
                    <div style="color: #000;">
                        <strong>${item.uf} — PRF 2025</strong><br>
                        Acidentes: <b>${item.total_acidentes}</b><br>
                        Vítimas Fatais: <b>${item.total_mortos}</b><br>
                        Índice Risco (ICR): <b>${item.icr_total}</b>
                    </div>
                `);
            }
        });
    } catch (e) {
        console.error("Erro ao popular mapa:", e);
    }
}

// Fetch 6: Top Rodovias Críticas
async function fetchRodoviasCriticas() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/rodovias-criticas`);
        const data = await res.json();

        const labels = data.map(d => `BR-${d.br}`);
        const icrValores = data.map(d => d.icr_total);

        renderChartRodovias(labels, icrValores);
    } catch (e) {
        console.error("Erro ao buscar Rodovias Críticas:", e);
    }
}

function renderChartRodovias(labels, valores) {
    const ctx = document.getElementById('chart-rodovias').getContext('2d');
    if (chartRodovias) chartRodovias.destroy();

    chartRodovias = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Índice Comparativo de Risco (ICR)',
                data: valores,
                backgroundColor: '#e63946'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#94a3b8' } } },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
            }
        }
    });
}

// Fetch 7: Tabela Paginada
async function fetchOcorrencias(uf = '', br = '') {
    try {
        const queryParams = new URLSearchParams({
            limit: pageSize,
            offset: currentPage * pageSize
        });
        if (uf) queryParams.append('uf', uf);
        if (br) queryParams.append('br', br);

        const res = await fetch(`${API_BASE_URL}/api/ocorrencias?${queryParams.toString()}`);
        const result = await res.json();

        tableData = result.data || [];
        renderTable(tableData, result.total || tableData.length);
    } catch (e) {
        console.error("Erro ao buscar tabela:", e);
    }
}

function renderTable(data, total) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;">Nenhuma ocorrência encontrada.</td></tr>';
        return;
    }

    data.forEach(row => {
        const tr = document.createElement('tr');
        
        let classBadge = 'badge-sem-vitimas';
        if (row.classificacao_acidente && row.classificacao_acidente.includes('Fatais')) {
            classBadge = 'badge-fatal';
        } else if (row.classificacao_acidente && row.classificacao_acidente.includes('Feridas')) {
            classBadge = 'badge-feridos';
        }

        tr.innerHTML = `
            <td><strong>#${row.id}</strong></td>
            <td>${row.data_inversa || '-'}</td>
            <td>${row.horario || '-'}</td>
            <td><span class="badge">${row.uf || '-'}</span></td>
            <td>BR-${row.br || '-'}</td>
            <td>${row.km || '-'}</td>
            <td>${row.municipio || '-'}</td>
            <td>${row.tipo_acidente || '-'}</td>
            <td>${row.causa_acidente || '-'}</td>
            <td><span class="${classBadge}">${row.classificacao_acidente || 'Sem Vítimas'}</span></td>
        `;
        tbody.appendChild(tr);
    });

    const start = (currentPage * pageSize) + 1;
    const end = Math.min((currentPage + 1) * pageSize, total);
    document.getElementById('pagination-info').textContent = `Exibindo ${start}-${end} de ${total} ocorrências`;

    document.getElementById('btn-prev-page').disabled = currentPage === 0;
    document.getElementById('btn-next-page').disabled = end >= total;
}

// Event Listeners
function setupEventListeners() {
    document.getElementById('btn-refresh').addEventListener('click', loadDashboardData);

    document.getElementById('btn-apply-filters').addEventListener('click', () => {
        const uf = document.getElementById('filter-uf').value;
        const br = document.getElementById('filter-br').value;
        currentPage = 0;
        fetchOcorrencias(uf, br);
    });

    document.getElementById('btn-reset-filters').addEventListener('click', () => {
        document.getElementById('filter-uf').value = '';
        document.getElementById('filter-br').value = '';
        currentPage = 0;
        fetchOcorrencias();
    });

    document.getElementById('btn-prev-page').addEventListener('click', () => {
        if (currentPage > 0) {
            currentPage--;
            fetchOcorrencias();
        }
    });

    document.getElementById('btn-next-page').addEventListener('click', () => {
        currentPage++;
        fetchOcorrencias();
    });

    document.getElementById('table-search-input').addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = tableData.filter(d => 
            (d.municipio && d.municipio.toLowerCase().includes(term)) ||
            (d.causa_acidente && d.causa_acidente.toLowerCase().includes(term))
        );
        renderTable(filtered, filtered.length);
    });
}
