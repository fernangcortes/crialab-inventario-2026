import json
import os

with open('data/inventario_conciliado.json', encoding='utf-8') as f:
    master_items = json.load(f)

with open('data/bens_nao_cadastrados_cot.json', encoding='utf-8') as f:
    nao_cadastrados = json.load(f)

# Load photos data from all 3 lotes
lote1 = json.load(open('data/auditoria_lote1.json', encoding='utf-8')).get('fotos', [])
lote2 = json.load(open('data/auditoria_lote2.json', encoding='utf-8')).get('fotos', [])
lote3 = json.load(open('data/auditoria_lote3.json', encoding='utf-8')).get('fotos', [])
all_photos = lote1 + lote2 + lote3

# Prepare payload
data_payload = {
    'master': master_items,
    'nao_cadastrados': nao_cadastrados,
    'photos': all_photos
}

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CriaLab & Radioteledifusão UEG - Painel de Gestão e Inventário 2026</title>
<style>
  :root {{
    --primary: #1565c0;
    --primary-dark: #0d47a1;
    --accent: #ff8f00;
    --bg: #f8fafc;
    --card: #ffffff;
    --text: #1e293b;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --success: #16a34a;
    --warning: #f59e0b;
    --danger: #dc2626;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
  body {{ background: var(--bg); color: var(--text); padding-bottom: 50px; }}
  
  header {{
    background: linear-gradient(135deg, var(--primary-dark), var(--primary));
    color: white;
    padding: 20px 30px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }}
  .header-top {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }}
  .header-title h1 {{ font-size: 22px; font-weight: 700; display: flex; align-items: center; gap: 10px; }}
  .header-title p {{ font-size: 13px; opacity: 0.9; margin-top: 4px; }}
  .badge-processo {{ background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); padding: 4px 10px; border-radius: 20px; font-size: 11px; }}
  
  .container {{ max-width: 1400px; margin: 25px auto; padding: 0 20px; }}
  
  /* KPI Cards */
  .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; }}
  .kpi-card {{ background: var(--card); border-radius: 10px; padding: 18px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
  .kpi-title {{ font-size: 12px; font-weight: 600; text-transform: uppercase; color: var(--text-muted); }}
  .kpi-value {{ font-size: 28px; font-weight: 800; margin: 6px 0; color: var(--primary); }}
  .kpi-sub {{ font-size: 11px; color: var(--text-muted); display: flex; align-items: center; gap: 5px; }}
  
  /* Tabs */
  .tabs {{ display: flex; gap: 10px; border-bottom: 2px solid var(--border); margin-bottom: 20px; overflow-x: auto; }}
  .tab-btn {{ background: none; border: none; padding: 10px 18px; font-size: 14px; font-weight: 600; color: var(--text-muted); cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.2s; white-space: nowrap; }}
  .tab-btn:hover {{ color: var(--primary); }}
  .tab-btn.active {{ color: var(--primary); border-bottom-color: var(--primary); }}
  
  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}
  
  /* Search & Controls */
  .control-bar {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 15px; align-items: center; justify-content: space-between; }}
  .search-box {{ flex: 1; min-width: 280px; position: relative; }}
  .search-box input {{ width: 100%; padding: 10px 14px; border: 1px solid var(--border); border-radius: 8px; font-size: 13px; }}
  .filter-group {{ display: flex; gap: 8px; flex-wrap: wrap; }}
  .btn-filter {{ padding: 8px 14px; border-radius: 6px; border: 1px solid var(--border); background: var(--card); font-size: 12px; cursor: pointer; font-weight: 500; }}
  .btn-filter.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
  .btn-action {{ padding: 8px 16px; border-radius: 6px; background: var(--primary); color: white; border: none; font-size: 12px; font-weight: 600; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; }}
  .btn-action:hover {{ background: var(--primary-dark); }}
  
  /* Tables */
  .table-container {{ background: var(--card); border-radius: 10px; border: 1px solid var(--border); overflow-x: auto; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
  table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 12px; }}
  th {{ background: #f1f5f9; padding: 12px 14px; font-weight: 600; color: #475569; border-bottom: 1px solid var(--border); white-space: nowrap; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid var(--border); vertical-align: middle; }}
  tr:hover {{ background: #f8fafc; }}
  
  .badge {{ display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 10px; font-weight: 700; text-transform: uppercase; }}
  .badge-audited {{ background: #dcfce7; color: #15803d; }}
  .badge-pending {{ background: #f1f5f9; color: #64748b; }}
  .badge-divergence {{ background: #fef3c7; color: #b45309; }}
  .badge-warning {{ background: #fee2e2; color: #b91c1c; }}
  .badge-crialab {{ background: #e0f2fe; color: #0369a1; }}
  .badge-radio {{ background: #f3e8ff; color: #7e22ce; }}
  
  /* Photo Grid */
  .photo-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }}
  .photo-card {{ background: var(--card); border-radius: 10px; border: 1px solid var(--border); overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: transform 0.2s; }}
  .photo-card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
  .photo-img-box {{ height: 180px; background: #000; overflow: hidden; display: flex; align-items: center; justify-content: center; cursor: pointer; }}
  .photo-img-box img {{ width: 100%; height: 100%; object-fit: cover; transition: opacity 0.2s; }}
  .photo-info {{ padding: 14px; }}
  .photo-title {{ font-size: 13px; font-weight: 700; margin-bottom: 4px; }}
  .photo-meta {{ font-size: 11px; color: var(--text-muted); margin-bottom: 8px; line-height: 1.4; }}
  
  /* Modal */
  .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 9999; justify-content: center; align-items: center; padding: 20px; }}
  .modal.active {{ display: flex; }}
  .modal-content {{ max-width: 90%; max-height: 90%; position: relative; }}
  .modal-content img {{ max-width: 100%; max-height: 85vh; border-radius: 6px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
  .close-modal {{ position: absolute; top: -35px; right: 0; color: white; font-size: 28px; cursor: pointer; font-weight: bold; }}
  
  /* Layout Spaces */
  .spaces-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 15px; }}
  .space-box {{ background: var(--card); border-radius: 10px; border: 1px solid var(--border); padding: 18px; }}
  .space-box h3 {{ font-size: 14px; font-weight: 700; margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between; }}
  .space-box p {{ font-size: 12px; color: var(--text-muted); margin-bottom: 12px; }}
</style>
</head>
<body>

<header>
  <div class="header-top">
    <div class="header-title">
      <h1>🏛️ CriaLab & Radioteledifusão UEG</h1>
      <p>Sistema Integrado de Conciliação Patrimonial, Auditoria Visual e Gestão de Acervo 2026</p>
    </div>
    <div style="text-align: right; display: flex; align-items: center; gap: 10px;">
      <div>
        <div class="badge-processo">Processo SEI: <strong>202600005037287</strong></div>
        <div style="font-size: 11px; margin-top: 5px; opacity: 0.9;">Prazo Limite: <strong>13/11/2026</strong> (Despacho 1049/2026)</div>
      </div>
      <a href="guia_fotografia_3d_ar.html" target="_blank" class="btn-action" style="background:#ffd54f; color:#0f172a; font-weight:700;">📐 Guia Ilustrado 3D / AR</a>
    </div>
  </div>
</header>

<div class="container">
  
  <!-- KPIs -->
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-title">Total de Bens no Acervo</div>
      <div class="kpi-value">377</div>
      <div class="kpi-sub"><span>📦 CriaLab: 285</span> | <span>📻 Rádio: 92</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Bens Auditados (COT)</div>
      <div class="kpi-value" style="color: var(--success);" id="kpi-audited">8</div>
      <div class="kpi-sub"><span>✓ Conciliados com placa/serial</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Bens Não Cadastrados</div>
      <div class="kpi-value" style="color: var(--warning);">6</div>
      <div class="kpi-sub"><span>⚠️ Na COT sem tombamento oficial</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Divergências de Setor</div>
      <div class="kpi-value" style="color: var(--accent);">5</div>
      <div class="kpi-sub"><span>🔄 Carga Rádio localizada na COT</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Fotos Processadas (IA)</div>
      <div class="kpi-value" style="color: var(--primary);">31</div>
      <div class="kpi-sub"><span>🤖 Multiagentes Gemini Flash</span></div>
    </div>
  </div>

  <!-- Tabs Navigation -->
  <div class="tabs">
    <button class="tab-btn active" onclick="switchTab('tab-inventario')">📋 Inventário Consolidado (377)</button>
    <button class="tab-btn" onclick="switchTab('tab-fotos')">📸 Auditoria Fotográfica COT (31 fotos)</button>
    <button class="tab-btn" onclick="switchTab('tab-extras')">⚠️ Bens Extras / Não Cadastrados (6)</button>
    <button class="tab-btn" onclick="switchTab('tab-espacos')">🗺️ Espaços & Planta Baixa</button>
    <button class="tab-btn" onclick="switchTab('tab-estoquenow')">📦 Estoque Now (Externa / Empréstimos)</button>
    <button class="tab-btn" onclick="switchTab('tab-fichas')">📑 Fichas & Documentos SEI</button>
  </div>

  <!-- TAB 1: Inventário Consolidado -->
  <div id="tab-inventario" class="tab-content active">
    <div class="control-bar">
      <div class="search-box">
        <input type="text" id="searchInput" placeholder="🔍 Buscar por tombamento, descrição, espécie, marca..." onkeyup="filterTable()">
      </div>
      <div class="filter-group">
        <button class="btn-filter active" onclick="setOriginFilter('ALL', this)">Todos (377)</button>
        <button class="btn-filter" onclick="setOriginFilter('CRIA LAB', this)">CriaLab (285)</button>
        <button class="btn-filter" onclick="setOriginFilter('RADIOTELEDIFUSÃO', this)">Radioteledifusão (92)</button>
        <button class="btn-filter" onclick="setStatusFilter('AUDITED', this)">Auditados na COT</button>
        <button class="btn-filter" onclick="setStatusFilter('DIVERGENCE', this)">Divergência Carga</button>
      </div>
      <a href="data/inventario_conciliado.csv" download class="btn-action">📥 Baixar Planilha CSV</a>
    </div>

    <div class="table-container">
      <table id="mainTable">
        <thead>
          <tr>
            <th>Origem</th>
            <th>Seq</th>
            <th>Tombamento</th>
            <th>Espécie</th>
            <th>Descrição</th>
            <th>Marca</th>
            <th>Status Auditoria</th>
            <th>Local Físico</th>
            <th>Fotos</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </div>

  <!-- TAB 2: Fotos COT -->
  <div id="tab-fotos" class="tab-content">
    <div style="margin-bottom: 15px; font-size: 13px; color: var(--text-muted);">
      Mostrando 31 fotografias da Central de Operação Técnica analisadas minuciosamente por multiagentes de IA:
    </div>
    <div class="photo-grid" id="photoGrid"></div>
  </div>

  <!-- TAB 3: Bens Extras -->
  <div id="tab-extras" class="tab-content">
    <div style="margin-bottom: 15px; font-size: 13px; color: var(--text-muted);">
      Equipamentos identificados em pleno uso operacional na COT que não constam nas listas oficiais do CriaLab ou Radioteledifusão (ou possuem tombamento informal):
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Equipamento</th>
            <th>Marca / Modelo</th>
            <th>Número de Série (S/N)</th>
            <th>Identificação Encontrada</th>
            <th>Estado Físico</th>
            <th>Recomendação da Comissão</th>
          </tr>
        </thead>
        <tbody id="extrasTableBody"></tbody>
      </table>
    </div>
  </div>

  <!-- TAB 4: Espaços CriaLab (Planta Baixa) -->
  <div id="tab-espacos" class="tab-content">
    <div style="background: linear-gradient(135deg, #1e3a8a, #1565c0); color: white; padding: 18px 24px; border-radius: 12px; margin-bottom: 22px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; box-shadow: 0 4px 12px rgba(21, 101, 192, 0.2);">
      <div>
        <h4 style="font-size: 15px; font-weight: 800; margin-bottom: 4px; display: flex; align-items: center; gap: 8px;">
          <span>📐</span> Guia Ilustrado de Captura Fotográfica 3D & Realidade Aumentada (AR)
        </h4>
        <p style="font-size: 12.5px; opacity: 0.9;">
          Acesse os diagramas técnicos vetoriais (4 Cantos 45º, Overlap 60-70%, Macro anti-reflexo 15º-20º e Pipeline Digital Twin WebXR).
        </p>
      </div>
      <a href="guia_fotografia_3d_ar.html" target="_blank" class="btn-action" style="background: #ffd54f; color: #0f172a; font-weight: 700; padding: 10px 18px; border-radius: 8px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
        Abrir Guia Ilustrado 3D / AR →
      </a>
    </div>

    <div style="margin-bottom: 20px; font-size: 13px; color: var(--text-muted);">
      Estrutura de cômodos do CriaLab / Radioteledifusão conforme plantas oficiais (Layout R05/2025). Utilize esta segmentação para as próximas etapas de varredura fotográfica e reconstrução espacial 3D / AR:
    </div>
    <div class="spaces-grid">
      <div class="space-box">
        <h3>1. Sala de Operação Técnica (COT) <span class="badge badge-audited">Auditado (31 fotos)</span></h3>
        <p>Área: 12,25m² | Pé Direito: 2,70m</p>
        <div style="font-size: 11px;">Mesas Behringer X32, Blackmagic ATEM 4K, Desktops Dell OptiPlex, Monitores, Servidor Spotware, Processador NovaStar.</div>
      </div>
      <div class="space-box">
        <h3>2. Sala de Equipamentos (Almoxarifado) <span class="badge badge-pending">Pendente</span></h3>
        <p>Área: 13,40m² | Pé Direito: 2,70m</p>
        <div style="font-size: 11px;">Guarda de câmeras, lentes, iluminadores LED/Fresnel, tripés, teleprompters e microfones móveis.</div>
      </div>
      <div class="space-box">
        <h3>3. Estúdio 01 - TV <span class="badge badge-pending">Pendente</span></h3>
        <p>Área: 42,20m² | Pé Direito: 2,70m</p>
        <div style="font-size: 11px;">Estúdio principal de gravação, grid de iluminação, câmeras de estúdio e switcher local.</div>
      </div>
      <div class="space-box">
        <h3>4. Estúdio 02 - Rádio <span class="badge badge-pending">Pendente</span></h3>
        <p>Área: 13,27m² | Pé Direito: 2,70m</p>
        <div style="font-size: 11px;">Mesa de áudio para rádio, fones de ouvido broadcast, processadores de voz e microfones cardióides.</div>
      </div>
      <div class="space-box">
        <h3>5. Estúdio 03 - VideoCast <span class="badge badge-pending">Pendente</span></h3>
        <p>Área: 21,82m² | Pé Direito: 2,70m</p>
        <div style="font-size: 11px;">Cenário podcast/videocast, microfones boom/articulados, câmeras robotizadas PTZ/webcams e iluminação difusa.</div>
      </div>
      <div class="space-box">
        <h3>6. Estúdio 04 & Estúdio 05 <span class="badge badge-pending">Pendente</span></h3>
        <p>Estúdio 04: 13,40m² | Estúdio 05: 5,53m²</p>
        <div style="font-size: 11px;">Estúdios auxiliares e cabines de gravação rápida / locução.</div>
      </div>
      <div class="space-box">
        <h3>7. Redação & Estações de Trabalho <span class="badge badge-pending">Pendente</span></h3>
        <p>Área: 111,46m² | 32 Estações de Trabalho</p>
        <div style="font-size: 11px;">32 bancadas, 48 mesas modulares, 63 cadeiras giratórias, computadores desktops, monitores Dell.</div>
      </div>
      <div class="space-box">
        <h3>8. Gabinetes E01 a E08 & Coordenação <span class="badge badge-pending">Pendente</span></h3>
        <p>8 Gabinetes de ~3,2m² cada + Coord. Adm (13,49m²)</p>
        <div style="font-size: 11px;">Mesas executivas, gaveteiros, armários de arquivo e estações administrativas.</div>
      </div>
    </div>
  </div>

  <!-- TAB 5: Estoque Now -->
  <div id="tab-estoquenow" class="tab-content">
    <div style="background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 25px; max-width: 800px;">
      <h3 style="margin-bottom: 10px; font-size: 16px;">📦 Cruzamento Automatizado com o Estoque Now</h3>
      <p style="font-size: 13px; color: var(--text-muted); line-height: 1.6; margin-bottom: 20px;">
        Para justificar perante a Comissão de Inventário os equipamentos que não se encontram fisicamente nos cômodos durante as fotos (bens em produção externa, coberturas jornalísticas ou locação/empréstimo para estudantes e equipes):
      </p>
      
      <div style="background: #f8fafc; border-left: 4px solid var(--primary); padding: 15px; margin-bottom: 20px; font-size: 13px;">
        <strong>Passo a Passo para Exportação:</strong><br>
        1. Acesse o sistema pelo link oficial: <a href="https://web.estoquenow.com.br/app" target="_blank" style="color: var(--primary); font-weight: 600;">web.estoquenow.com.br/app</a><br>
        2. Faça login com suas credenciais do CriaLab.<br>
        3. Acesse o menu <strong>Relatórios / Exportar Equipamentos</strong> ou <strong>Movimentações / Empréstimos Ativos</strong>.<br>
        4. Exporte o arquivo em <strong>CSV</strong> ou <strong>Excel (.xlsx)</strong>.<br>
        5. Salve o arquivo na pasta do projeto: <code>c:\\Users\\FGC\\dev\\CriaLab\\inventario\\2026\\data\\estoquenow.csv</code>
      </div>

      <p style="font-size: 12px; color: var(--text-muted);">
        Assim que a planilha for inserida na pasta, nosso robô fará o batimento cruzado instantâneo pelo tombamento ou número de série, marcando automaticamente o status: <em>"BEM EM EXTERNA / EMPRÉSTIMO ATIVO NO ESTOQUE NOW"</em>, o que impede a abertura indevida de Termo Circunstanciado Administrativo (TCA).
      </p>
    </div>
  </div>

  <!-- TAB 6: Fichas & Documentos -->
  <div id="tab-fichas" class="tab-content">
    <div style="background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 25px;">
      <h3 style="margin-bottom: 15px; font-size: 16px;">📑 Fichas de Apuração Oficiais Preenchidas para Impressão</h3>
      <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 20px;">
        Fichas formatadas no modelo oficial da SEAD / UEG, com cabeçalho do SPM, checkboxes devidamente marcados (Auditado, Nova Etiqueta, Imperfeição) e bloco de assinaturas para envio ao Processo SEI nº 202600005037287:
      </p>
      <div style="display: flex; gap: 15px; flex-wrap: wrap;">
        <a href="fichas/Ficha_Apuracao_CriaLab_Preenchida.html" target="_blank" class="btn-action" style="padding: 12px 20px; font-size: 13px;">
          🖨️ Ficha Oficial CriaLab (285 Bens)
        </a>
        <a href="fichas/Ficha_Apuracao_Radioteledifusao_Preenchida.html" target="_blank" class="btn-action" style="padding: 12px 20px; font-size: 13px; background: #7e22ce;">
          🖨️ Ficha Oficial Radioteledifusão (92 Bens)
        </a>
      </div>
    </div>
  </div>

</div>

<!-- Image Modal -->
<div class="modal" id="imageModal" onclick="closeModal()">
  <div class="modal-content" onclick="event.stopPropagation()">
    <span class="close-modal" onclick="closeModal()">&times;</span>
    <img id="modalImg" src="">
    <div id="modalCaption" style="color: white; margin-top: 10px; font-size: 13px; text-align: center;"></div>
  </div>
</div>

<script>
const DATA = {json.dumps(data_payload, ensure_ascii=False)};

let currentOrigin = 'ALL';
let currentStatus = 'ALL';

function switchTab(tabId) {{
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}}

function renderTable() {{
  const tbody = document.getElementById('tableBody');
  const search = document.getElementById('searchInput').value.toLowerCase();
  
  const filtered = DATA.master.filter(it => {{
    if (currentOrigin !== 'ALL' && it.origem !== currentOrigin) return false;
    if (currentStatus === 'AUDITED' && it.auditado !== 'SIM') return false;
    if (currentStatus === 'DIVERGENCE' && !it.divergencia_carga.startsWith('SIM')) return false;
    
    if (search) {{
      const text = (it.tombamento + ' ' + it.especie + ' ' + it.descricao + ' ' + it.marca + ' ' + it.origem).toLowerCase();
      if (!text.includes(search)) return false;
    }}
    return true;
  }});

  tbody.innerHTML = filtered.map(it => {{
    const badgeOrigem = it.origem === 'CRIA LAB' ? 'badge-crialab' : 'badge-radio';
    const badgeAudit = it.auditado === 'SIM' ? 'badge-audited' : 'badge-pending';
    const badgeText = it.auditado === 'SIM' ? 'Auditado' : 'Pendente';
    
    return `<tr>
      <td><span class="badge ${{badgeOrigem}}">${{it.origem}}</span></td>
      <td style="font-weight:600; text-align:center;">${{it.seq}}</td>
      <td style="font-weight:700; color:var(--primary);">${{it.tombamento}}</td>
      <td><strong>${{it.especie}}</strong></td>
      <td>
        ${{it.descricao}}
        ${{it.observacao_auditoria && it.auditado === 'SIM' ? '<br><small style="color:#0d47a1"><strong>[Obs COT]:</strong> ' + it.observacao_auditoria + '</small>' : ''}}
      </td>
      <td>${{it.marca}}</td>
      <td><span class="badge ${{badgeAudit}}">${{badgeText}}</span></td>
      <td>${{it.local_fisico}}</td>
      <td style="font-size:11px; color:#64748b;">${{it.fotos_evidencia || '-'}}</td>
    </tr>`;
  }}).join('');
}}

function filterTable() {{
  renderTable();
}}

function setOriginFilter(origem, btn) {{
  currentOrigin = origem;
  document.querySelectorAll('.filter-group .btn-filter').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderTable();
}}

function setStatusFilter(status, btn) {{
  currentStatus = status;
  document.querySelectorAll('.filter-group .btn-filter').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderTable();
}}

function renderPhotos() {{
  const grid = document.getElementById('photoGrid');
  grid.innerHTML = DATA.photos.map(p => {{
    const fileName = p.arquivo.split(/\\\\|\\//).pop();
    const relPath = 'fotos/central de operacao tecnica/' + fileName;
    const tomb = (p.placa_tombamento && p.placa_tombamento.numero) ? p.placa_tombamento.numero : 'Sem Placa';
    const sn = (typeof p.numero_serie_fabricante === 'string') ? p.numero_serie_fabricante : (p.numero_serie_fabricante && p.numero_serie_fabricante.service_tag ? p.numero_serie_fabricante.service_tag : '-');

    return `<div class="photo-card">
      <div class="photo-img-box" onclick="openModal('${{relPath}}', '${{p.tipo_equipamento}} - ${{fileName}}')">
        <img src="${{relPath}}" alt="${{p.tipo_equipamento}}" loading="lazy" onerror="this.style.display='none'">
      </div>
      <div class="photo-info">
        <div class="photo-title">${{p.tipo_equipamento}}</div>
        <div class="photo-meta">
          <strong>Marca/Modelo:</strong> ${{p.marca || '-'}} ${{p.modelo || ''}}<br>
          <strong>Tombamento:</strong> <span style="color:var(--primary); font-weight:bold;">${{tomb}}</span><br>
          <strong>S/N:</strong> ${{sn}}<br>
          <strong>Estado:</strong> ${{p.estado_fisico}}
        </div>
      </div>
    </div>`;
  }}).join('');
}}

function renderExtras() {{
  const tbody = document.getElementById('extrasTableBody');
  tbody.innerHTML = DATA.nao_cadastrados.map(e => `
    <tr>
      <td><strong>${{e.equipamento}}</strong></td>
      <td>${{e.marca}} ${{e.modelo}}</td>
      <td><code>${{e.numero_serie}}</code></td>
      <td><span class="badge badge-warning">${{e.tombamento_identificado}}</span></td>
      <td>${{e.estado_fisico}}</td>
      <td style="font-size:11px;">${{e.recomendacao}}</td>
    </tr>
  `).join('');
}}

function openModal(src, caption) {{
  document.getElementById('modalImg').src = src;
  document.getElementById('modalCaption').innerText = caption;
  document.getElementById('imageModal').classList.add('active');
}}

function closeModal() {{
  document.getElementById('imageModal').classList.remove('active');
}}

// Init
renderTable();
renderPhotos();
renderExtras();
</script>

</body>
</html>
"""

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('dashboard.html created successfully!')
