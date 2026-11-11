import json
import os

with open('data/inventario_conciliado.json', encoding='utf-8') as f:
    master_items = json.load(f)

with open('data/bens_nao_cadastrados_cot.json', encoding='utf-8') as f:
    nao_cadastrados = json.load(f)

# Load photos data
lote1 = json.load(open('data/auditoria_lote1.json', encoding='utf-8')).get('fotos', [])
lote2 = json.load(open('data/auditoria_lote2.json', encoding='utf-8')).get('fotos', [])
lote3 = json.load(open('data/auditoria_lote3.json', encoding='utf-8')).get('fotos', [])
all_photos = lote1 + lote2 + lote3

payload = {
    'master': master_items,
    'nao_cadastrados': nao_cadastrados,
    'photos': all_photos
}

favicon_svg = '''data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="%231565c0"/><stop offset="100%" stop-color="%230d47a1"/></linearGradient></defs><rect width="100" height="100" rx="20" fill="url(%23g)"/><path d="M25 35h50v40H25z" fill="%23ffffff" rx="6"/><circle cx="50" cy="55" r="14" fill="%231565c0"/><circle cx="50" cy="55" r="8" fill="%23ffd54f"/><rect x="40" y="24" width="20" height="8" rx="3" fill="%23ffd54f"/></svg>'''

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CriaLab & Radioteledifusão UEG - Inventário e Gestão Patrimonial 2026</title>

<!-- Metatags SEO e OpenGraph -->
<meta name="description" content="Sistema Integrado de Conciliação Patrimonial, Auditoria Fotográfica por IA e Gestão de Acervo 2026 do CriaLab e Radioteledifusão da Universidade Estadual de Goiás (UEG).">
<meta name="keywords" content="CriaLab, Radioteledifusão, UEG, Inventário 2026, Patrimônio Mobiliário, SEI 202600005037287, SPM">
<meta name="author" content="Fernando Gomes Cortes - Comissão Setorial de Inventário UEG">
<meta name="theme-color" content="#1565c0">

<!-- Open Graph / Facebook / WhatsApp -->
<meta property="og:type" content="website">
<meta property="og:title" content="CriaLab & Radioteledifusão UEG - Inventário Patrimonial 2026">
<meta property="og:description" content="Painel oficial de conciliação de acervo, auditoria fotográfica por multiagentes e preenchimento de fichas SEAD/SPM.">
<meta property="og:image" content="{favicon_svg}">

<!-- Twitter -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="CriaLab & Radioteledifusão UEG - Inventário 2026">
<meta name="twitter:description" content="Painel oficial de conciliação patrimonial e auditoria visual da UEG Laranjeiras.">

<!-- Favicon SVG -->
<link rel="icon" type="image/svg+xml" href="{favicon_svg}">

<style>
  :root {{
    --primary: #1565c0;
    --primary-dark: #0d47a1;
    --primary-light: #e3f2fd;
    --accent: #ff8f00;
    --bg: #f8fafc;
    --card: #ffffff;
    --text: #0f172a;
    --text-muted: #64748b;
    --border: #cbd5e1;
    --border-light: #e2e8f0;
    --success: #16a34a;
    --success-bg: #dcfce7;
    --warning: #d97706;
    --warning-bg: #fef3c7;
    --danger: #dc2626;
    --danger-bg: #fee2e2;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
  body {{ background: var(--bg); color: var(--text); padding-bottom: 60px; line-height: 1.5; }}
  
  header {{
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
    color: white;
    padding: 22px 32px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
  }}
  .header-top {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }}
  .header-title h1 {{ font-size: 22px; font-weight: 800; display: flex; align-items: center; gap: 10px; }}
  .header-title p {{ font-size: 13px; opacity: 0.92; margin-top: 4px; }}
  .header-badges {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
  .badge-processo {{ background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.3); padding: 5px 12px; border-radius: 20px; font-size: 11.5px; }}
  .badge-deadline {{ background: #ef4444; color: white; padding: 5px 12px; border-radius: 20px; font-size: 11.5px; font-weight: 700; }}
  
  .container {{ max-width: 1480px; margin: 25px auto; padding: 0 24px; }}
  
  /* KPI Cards */
  .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 25px; }}
  .kpi-card {{ background: var(--card); border-radius: 12px; padding: 18px 20px; border: 1px solid var(--border-light); box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
  .kpi-title {{ font-size: 11.5px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.5px; }}
  .kpi-value {{ font-size: 30px; font-weight: 800; margin: 6px 0; color: var(--primary); }}
  .kpi-sub {{ font-size: 11.5px; color: var(--text-muted); display: flex; align-items: center; gap: 6px; }}
  
  /* Tabs */
  .tabs {{ display: flex; gap: 8px; border-bottom: 2px solid var(--border-light); margin-bottom: 20px; overflow-x: auto; padding-bottom: 2px; }}
  .tab-btn {{ background: none; border: none; padding: 11px 20px; font-size: 13.5px; font-weight: 600; color: var(--text-muted); cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.2s; white-space: nowrap; border-radius: 6px 6px 0 0; }}
  .tab-btn:hover {{ color: var(--primary); background: rgba(21, 101, 192, 0.04); }}
  .tab-btn.active {{ color: var(--primary); border-bottom-color: var(--primary); background: rgba(21, 101, 192, 0.06); }}
  
  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}
  
  /* Controls & Action Bar */
  .control-bar {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 16px; align-items: center; justify-content: space-between; }}
  .search-box {{ flex: 1; min-width: 280px; position: relative; }}
  .search-box input {{ width: 100%; padding: 11px 16px; border: 1px solid var(--border); border-radius: 8px; font-size: 13px; outline: none; transition: border-color 0.2s; background: var(--card); }}
  .search-box input:focus {{ border-color: var(--primary); box-shadow: 0 0 0 3px rgba(21, 101, 192, 0.15); }}
  .filter-group {{ display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }}
  .btn-filter {{ padding: 8px 14px; border-radius: 7px; border: 1px solid var(--border); background: var(--card); font-size: 12px; cursor: pointer; font-weight: 600; color: var(--text); transition: all 0.15s; }}
  .btn-filter:hover {{ background: #f1f5f9; }}
  .btn-filter.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
  
  .btn-action {{ padding: 9px 16px; border-radius: 7px; background: var(--primary); color: white; border: none; font-size: 12.5px; font-weight: 600; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; gap: 7px; transition: background 0.15s; }}
  .btn-action:hover {{ background: var(--primary-dark); }}
  .btn-secondary {{ background: var(--card); color: var(--text); border: 1px solid var(--border); }}
  .btn-secondary:hover {{ background: #f1f5f9; }}
  
  /* Column Visibility Dropdown */
  .dropdown {{ position: relative; display: inline-block; }}
  .dropdown-menu {{ display: none; position: absolute; right: 0; top: 100%; background: white; min-width: 250px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border-radius: 8px; border: 1px solid var(--border); padding: 12px; z-index: 999; margin-top: 5px; max-height: 400px; overflow-y: auto; }}
  .dropdown-menu.show {{ display: block; }}
  .dropdown-header {{ font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px; padding-bottom: 5px; border-bottom: 1px solid var(--border-light); }}
  .col-toggle-item {{ display: flex; align-items: center; gap: 8px; padding: 6px 4px; font-size: 12.5px; cursor: pointer; }}
  .col-toggle-item input {{ cursor: pointer; }}
  
  /* Tables */
  .table-container {{ background: var(--card); border-radius: 12px; border: 1px solid var(--border-light); overflow-x: auto; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
  table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 12.5px; }}
  th {{ background: #f8fafc; padding: 12px 14px; font-weight: 700; color: #475569; border-bottom: 1px solid var(--border); white-space: nowrap; user-select: none; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid var(--border-light); vertical-align: middle; }}
  tr:hover {{ background: #f8fafc; }}
  
  /* Editable Cells */
  .editable-cell {{ cursor: pointer; position: relative; border-radius: 4px; padding: 2px 4px; transition: background 0.15s; }}
  .editable-cell:hover {{ background: #e0f2fe; outline: 1px dashed var(--primary); }}
  .editing {{ padding: 0 !important; }}
  .editing input, .editing select, .editing textarea {{ width: 100%; padding: 6px 8px; border: 2px solid var(--primary); border-radius: 4px; font-size: 12px; outline: none; background: #fff; }}
  
  /* Badges */
  .badge {{ display: inline-block; padding: 3px 9px; border-radius: 12px; font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3px; }}
  .badge-audited {{ background: var(--success-bg); color: var(--success); }}
  .badge-pending {{ background: #f1f5f9; color: var(--text-muted); }}
  .badge-divergence {{ background: var(--warning-bg); color: var(--warning); }}
  .badge-danger {{ background: var(--danger-bg); color: var(--danger); }}
  .badge-crialab {{ background: #e0f2fe; color: #0284c7; }}
  .badge-radio {{ background: #f3e8ff; color: #9333ea; }}
  
  /* Photo Grid */
  .photo-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }}
  .photo-card {{ background: var(--card); border-radius: 12px; border: 1px solid var(--border-light); overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.04); transition: transform 0.2s, box-shadow 0.2s; }}
  .photo-card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 16px rgba(0,0,0,0.08); }}
  .photo-img-box {{ height: 180px; background: #000; overflow: hidden; display: flex; align-items: center; justify-content: center; cursor: pointer; }}
  .photo-img-box img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }}
  .photo-card:hover .photo-img-box img {{ transform: scale(1.04); }}
  .photo-info {{ padding: 14px; }}
  .photo-title {{ font-size: 13.5px; font-weight: 700; margin-bottom: 4px; }}
  .photo-meta {{ font-size: 11.5px; color: var(--text-muted); margin-bottom: 8px; line-height: 1.45; }}
  
  /* Modal */
  .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.88); z-index: 9999; justify-content: center; align-items: center; padding: 20px; }}
  .modal.active {{ display: flex; }}
  .modal-content {{ max-width: 90%; max-height: 90%; position: relative; text-align: center; }}
  .modal-content img {{ max-width: 100%; max-height: 85vh; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
  .close-modal {{ position: absolute; top: -40px; right: 0; color: white; font-size: 32px; cursor: pointer; font-weight: bold; }}
  
  /* Spaces Grid */
  .spaces-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }}
  .space-box {{ background: var(--card); border-radius: 12px; border: 1px solid var(--border-light); padding: 20px; }}
  .space-box h3 {{ font-size: 14.5px; font-weight: 700; margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between; }}
  .space-box p {{ font-size: 12px; color: var(--text-muted); margin-bottom: 10px; }}
  
  /* Toast Notification */
  .toast {{ position: fixed; bottom: 20px; right: 20px; background: #1e293b; color: white; padding: 12px 20px; border-radius: 8px; font-size: 13px; z-index: 10000; box-shadow: 0 4px 12px rgba(0,0,0,0.2); opacity: 0; transform: translateY(10px); transition: all 0.3s; pointer-events: none; }}
  .toast.show {{ opacity: 1; transform: translateY(0); pointer-events: auto; }}

  @media print {{
    header, .kpi-grid, .tabs, .control-bar, .modal, .toast {{ display: none !important; }}
    .container {{ max-width: 100%; margin: 0; padding: 0; }}
    .table-container {{ border: none; box-shadow: none; }}
    table {{ font-size: 9px; width: 100%; }}
    th, td {{ padding: 4px 6px; border: 1px solid #777; }}
  }}
</style>
</head>
<body>

<header>
  <div class="header-top">
    <div class="header-title">
      <h1>🏛️ CriaLab & Radioteledifusão UEG</h1>
      <p>Sistema Integrado de Conciliação Patrimonial, Auditoria Visual e Gestão de Acervo 2026</p>
    </div>
    <div class="header-badges">
      <div class="badge-processo">SEI: <strong>202600005037287</strong></div>
      <div class="badge-deadline">Prazo SEI: 13/11/2026</div>
      <a href="guia_fotografia_3d_ar.html" target="_blank" class="btn-action" style="background:#ffd54f; color:#0f172a;">📐 Guia Ilustrado 3D / AR</a>
    </div>
  </div>
</header>

<div class="container">
  
  <!-- KPIs -->
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-title">Total no Acervo</div>
      <div class="kpi-value" id="kpi-total">377</div>
      <div class="kpi-sub"><span>📦 CriaLab: 285</span> | <span>📻 Rádio: 92</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Tombados Auditados</div>
      <div class="kpi-value" style="color: var(--success);" id="kpi-audited">5</div>
      <div class="kpi-sub"><span>✓ Confirmados com placa UEG</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Bens Não Tombados</div>
      <div class="kpi-value" style="color: var(--warning);">9</div>
      <div class="kpi-sub"><span>⚠️ Sem foto de tombamento</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Divergências de Setor</div>
      <div class="kpi-value" style="color: var(--accent);">3</div>
      <div class="kpi-sub"><span>🔄 Carga Rádio na COT</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Fotos Processadas (IA)</div>
      <div class="kpi-value" style="color: var(--primary);">31</div>
      <div class="kpi-sub"><span>🤖 14 itens mapeados em sequência</span></div>
    </div>
  </div>

  <!-- Tabs Navigation -->
  <div class="tabs">
    <button class="tab-btn active" onclick="switchTab('tab-inventario')">📋 Inventário Consolidado (377)</button>
    <button class="tab-btn" onclick="switchTab('tab-fotos')">📸 Auditoria Fotográfica COT (31 fotos)</button>
    <button class="tab-btn" onclick="switchTab('tab-extras')">⚠️ Bens Não Tombados na COT (9)</button>
    <button class="tab-btn" onclick="switchTab('tab-espacos')">🗺️ Espaços & Planta Baixa</button>
    <button class="tab-btn" onclick="switchTab('tab-estoquenow')">📦 Estoque Now (Externa / Empréstimos)</button>
    <button class="tab-btn" onclick="switchTab('tab-fichas')">📑 Fichas & Documentos Oficiais</button>
  </div>

  <!-- TAB 1: Inventário Consolidado com Edição Inline e Ocultação de Colunas -->
  <div id="tab-inventario" class="tab-content active">
    
    <div class="control-bar">
      <div class="search-box">
        <input type="text" id="searchInput" placeholder="🔍 Buscar por tombamento, descrição, espécie, marca, serial..." onkeyup="filterTable()">
      </div>
      
      <div class="filter-group">
        <button class="btn-filter active" onclick="setOriginFilter('ALL', this)">Todos (377)</button>
        <button class="btn-filter" onclick="setOriginFilter('CRIA LAB', this)">CriaLab (285)</button>
        <button class="btn-filter" onclick="setOriginFilter('RADIOTELEDIFUSÃO', this)">Radioteledifusão (92)</button>
        <button class="btn-filter" onclick="setStatusFilter('AUDITED', this)">Auditados na COT</button>
        <button class="btn-filter" onclick="setStatusFilter('DIVERGENCE', this)">Divergência Carga</button>
      </div>

      <div class="filter-group">
        <!-- Dropdown de Visibilidade de Colunas -->
        <div class="dropdown">
          <button class="btn-filter btn-secondary" onclick="toggleColumnDropdown()">👁️ Colunas & Campos ▾</button>
          <div class="dropdown-menu" id="colDropdown">
            <div class="dropdown-header">Exibir / Ocultar Colunas</div>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="origem" onchange="toggleColumn(this)"> Origem (CriaLab/Rádio)</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="seq" onchange="toggleColumn(this)"> Seq</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="tombamento" onchange="toggleColumn(this)"> Nº Tombamento</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="especie" onchange="toggleColumn(this)"> Espécie</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="descricao" onchange="toggleColumn(this)"> Descrição</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="marca" onchange="toggleColumn(this)"> Marca</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="status" onchange="toggleColumn(this)"> Status Auditoria</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="local" onchange="toggleColumn(this)"> Local Físico</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="avarias" onchange="toggleColumn(this)"> Estado / Imperfeições</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="fotos" onchange="toggleColumn(this)"> Fotos Evidência</label>
            <div style="margin-top:8px; border-top:1px solid #eee; padding-top:6px; font-size:11px; color:#666;">
              * Colunas desmarcadas não serão impressas nem incluídas no CSV.
            </div>
          </div>
        </div>

        <button class="btn-filter btn-secondary" onclick="exportCustomCSV()">📥 Exportar CSV (Visíveis)</button>
        <button class="btn-action" onclick="window.print()">🖨️ Imprimir / PDF</button>
        <button class="btn-filter btn-secondary" style="color:var(--danger);" onclick="resetEdits()" title="Restaura os dados originais caso tenha feito edições">↺ Restaurar</button>
      </div>
    </div>

    <div style="margin-bottom: 12px; font-size: 12px; color: var(--text-muted); display:flex; justify-content:space-between; align-items:center;">
      <span>💡 <em>Dica: Dê duplo-clique nas células de <strong>Status</strong>, <strong>Local Físico</strong>, <strong>Estado/Imperfeições</strong> ou <strong>Observações</strong> para editar diretamente os dados.</em></span>
      <span id="saveStatus" style="font-weight:600; color:var(--success);">✓ Dados sincronizados</span>
    </div>

    <div class="table-container">
      <table id="mainTable">
        <thead>
          <tr>
            <th class="col-origem">Origem</th>
            <th class="col-seq">Seq</th>
            <th class="col-tombamento">Tombamento</th>
            <th class="col-especie">Espécie</th>
            <th class="col-descricao">Descrição</th>
            <th class="col-marca">Marca</th>
            <th class="col-status">Status Auditoria</th>
            <th class="col-local">Local Físico</th>
            <th class="col-avarias">Estado / Imperfeições</th>
            <th class="col-fotos">Fotos</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </div>

  <!-- TAB 2: Fotos COT -->
  <div id="tab-fotos" class="tab-content">
    <div style="margin-bottom: 15px; font-size: 13px; color: var(--text-muted);">
      31 fotografias da Central de Operação Técnica (COT) processadas por agentes de IA com identificação de placas, números de série e avarias:
    </div>
    <div class="photo-grid" id="photoGrid"></div>
  </div>

  <!-- TAB 3: Bens Extras -->
  <div id="tab-extras" class="tab-content">
    <div style="margin-bottom: 15px; font-size: 13px; color: var(--text-muted);">
      Equipamentos identificados em operação na COT que não constam nas listas oficiais do CriaLab/Rádio ou necessitam de regularização patrimonial:
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
    <div style="margin-bottom: 20px; font-size: 13px; color: var(--text-muted);">
      Divisão dos espaços do CriaLab / Radioteledifusão conforme plantas oficiais (Layout R05/2025). Utilize esta segmentação para as próximas etapas de varredura fotográfica e reconstrução espacial 3D / AR:
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
        <div style="font-size: 11px;">Cenário podcast/videocast, microfones boom/articulados, câmeras PTZ e iluminação difusa.</div>
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
    <div style="background: var(--card); border: 1px solid var(--border-light); border-radius: 12px; padding: 28px; max-width: 850px;">
      <h3 style="margin-bottom: 12px; font-size: 16px;">📦 Cruzamento com Estoque Now (Bens em Externa)</h3>
      <p style="font-size: 13px; color: var(--text-muted); line-height: 1.6; margin-bottom: 20px;">
        Para justificar perante a Comissão os equipamentos que estão em externa, produções ou empréstimos ativos com alunos/equipes durante a passagem das fotos:
      </p>
      
      <div style="background: #f8fafc; border-left: 4px solid var(--primary); padding: 16px; margin-bottom: 20px; font-size: 13px; border-radius: 0 8px 8px 0;">
        <strong>Passo a Passo Rápido:</strong><br>
        1. Como você já está com o site aberto no seu navegador, vá na aba de <strong>Equipamentos / Empréstimos Ativos</strong> no Estoque Now.<br>
        2. Clique em <strong>Exportar (CSV ou Excel)</strong>.<br>
        3. Arraste o arquivo baixado para o campo abaixo ou salve como <code>data/estoquenow.csv</code> na pasta do projeto.
      </div>

      <div style="border: 2px dashed var(--border); padding: 30px; text-align: center; border-radius: 10px; background: #fafafa; cursor: pointer;" onclick="document.getElementById('csvFileInput').click()">
        <input type="file" id="csvFileInput" accept=".csv,.txt" style="display:none;" onchange="handleFileImport(event)">
        <div style="font-size: 28px; margin-bottom: 8px;">📂</div>
        <div style="font-size: 14px; font-weight: 600;">Clique aqui ou arraste o CSV do Estoque Now</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">Conciliação automática instantânea por Placa ou Número de Série</div>
      </div>
    </div>
  </div>

  <!-- TAB 6: Fichas & Documentos -->
  <div id="tab-fichas" class="tab-content">
    <div style="background: var(--card); border: 1px solid var(--border-light); border-radius: 12px; padding: 28px;">
      <h3 style="margin-bottom: 14px; font-size: 16px;">📑 Fichas de Apuração Oficiais Preenchidas para Impressão</h3>
      <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 22px;">
        Fichas formatadas rigorosamente no modelo do SPM / SEAD do Governo de Goiás, com checkboxes marcados (Auditado, Nova Etiqueta, Imperfeição) e bloco de assinaturas para envio ao Processo SEI nº 202600005037287:
      </p>
      <div style="display: flex; gap: 16px; flex-wrap: wrap;">
        <a href="fichas/Ficha_Apuracao_CriaLab_Preenchida.html" target="_blank" class="btn-action" style="padding: 12px 22px; font-size: 13px;">
          🖨️ Ficha Oficial CriaLab (285 Bens)
        </a>
        <a href="fichas/Ficha_Apuracao_Radioteledifusao_Preenchida.html" target="_blank" class="btn-action" style="padding: 12px 22px; font-size: 13px; background: #7e22ce;">
          🖨️ Ficha Oficial Radioteledifusão (92 Bens)
        </a>
        <a href="guia_fotografia_3d_ar.html" target="_blank" class="btn-action" style="padding: 12px 22px; font-size: 13px; background: #0284c7;">
          📐 Guia Ilustrado de Fotografia 3D & AR
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
    <div id="modalCaption" style="color: white; margin-top: 12px; font-size: 13.5px; text-align: center;"></div>
  </div>
</div>

<!-- Toast -->
<div class="toast" id="toast">Alteração salva com sucesso!</div>

<script>
const INITIAL_DATA = {json.dumps(payload, ensure_ascii=False)};

// Carregar do localStorage se houver edições salvas
let localData = localStorage.getItem('crialab_inventario_data_2026');
let DATA = localData ? JSON.parse(localData) : INITIAL_DATA;

let currentOrigin = 'ALL';
let currentStatus = 'ALL';

// Configuração de visibilidade das colunas
let visibleColumns = {{
  origem: true,
  seq: true,
  tombamento: true,
  especie: true,
  descricao: true,
  marca: true,
  status: true,
  local: true,
  avarias: true,
  fotos: true
}};

function showToast(msg) {{
  const toast = document.getElementById('toast');
  toast.innerText = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2500);
}}

function switchTab(tabId) {{
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  if (event && event.target) event.target.classList.add('active');
}}

function renderTable() {{
  const tbody = document.getElementById('tableBody');
  const search = document.getElementById('searchInput').value.toLowerCase();
  
  const filtered = DATA.master.filter(it => {{
    if (currentOrigin !== 'ALL' && it.origem !== currentOrigin) return false;
    if (currentStatus === 'AUDITED' && it.auditado !== 'SIM') return false;
    if (currentStatus === 'DIVERGENCE' && !it.divergencia_carga.startsWith('SIM')) return false;
    
    if (search) {{
      const text = (it.tombamento + ' ' + it.especie + ' ' + it.descricao + ' ' + it.marca + ' ' + it.origem + ' ' + it.local_fisico + ' ' + (it.observacao_auditoria || '')).toLowerCase();
      if (!text.includes(search)) return false;
    }}
    return true;
  }});

  tbody.innerHTML = filtered.map((it, idx) => {{
    const badgeOrigem = it.origem === 'CRIA LAB' ? 'badge-crialab' : 'badge-radio';
    const badgeAudit = it.auditado === 'SIM' ? 'badge-audited' : (it.auditado === 'EXTERNA' ? 'badge-divergence' : 'badge-pending');
    const badgeText = it.auditado === 'SIM' ? 'Auditado' : (it.auditado === 'EXTERNA' ? 'Em Externa' : 'Pendente');
    const avariaBadge = (it.estado_fisico && it.estado_fisico !== 'Normal' && it.estado_fisico !== 'A conferir') 
      ? `<span class="badge badge-danger">${{it.estado_fisico}}</span>` 
      : `<span style="color:#64748b;">${{it.estado_fisico || 'Normal'}}</span>`;

    return `<tr data-seq="${{it.seq}}" data-origem="${{it.origem}}">
      <td class="col-origem" style="${{visibleColumns.origem ? '' : 'display:none;'}}"><span class="badge ${{badgeOrigem}}">${{it.origem}}</span></td>
      <td class="col-seq" style="${{visibleColumns.seq ? '' : 'display:none;'}} font-weight:600; text-align:center;">${{it.seq}}</td>
      <td class="col-tombamento" style="${{visibleColumns.tombamento ? '' : 'display:none;'}} font-weight:700; color:var(--primary);">${{it.tombamento}}</td>
      <td class="col-especie" style="${{visibleColumns.especie ? '' : 'display:none;'}}"><strong>${{it.especie}}</strong></td>
      <td class="col-descricao" style="${{visibleColumns.descricao ? '' : 'display:none;'}}">
        <div class="editable-cell" ondblclick="editField(this, '${{it.seq}}', '${{it.origem}}', 'descricao')">${{it.descricao}}</div>
        ${{it.observacao_auditoria ? '<div class="editable-cell" style="margin-top:4px;" ondblclick="editField(this, \\'' + it.seq + '\\', \\'' + it.origem + '\\', \\'observacao_auditoria\\')"><small style=\\"color:#0d47a1\\"><strong>[Obs]:</strong> ' + it.observacao_auditoria + '</small></div>' : ''}}
      </td>
      <td class="col-marca" style="${{visibleColumns.marca ? '' : 'display:none;'}}">${{it.marca}}</td>
      <td class="col-status" style="${{visibleColumns.status ? '' : 'display:none;'}}">
        <div class="editable-cell" ondblclick="editStatus(this, '${{it.seq}}', '${{it.origem}}')">
          <span class="badge ${{badgeAudit}}">${{badgeText}}</span>
        </div>
      </td>
      <td class="col-local" style="${{visibleColumns.local ? '' : 'display:none;'}}">
        <div class="editable-cell" ondblclick="editField(this, '${{it.seq}}', '${{it.origem}}', 'local_fisico')">${{it.local_fisico || 'Pendente'}}</div>
      </td>
      <td class="col-avarias" style="${{visibleColumns.avarias ? '' : 'display:none;'}}">
        <div class="editable-cell" ondblclick="editEstado(this, '${{it.seq}}', '${{it.origem}}')">${{avariaBadge}}</div>
      </td>
      <td class="col-fotos" style="${{visibleColumns.fotos ? '' : 'display:none;'}} font-size:11px; color:#64748b;">${{it.fotos_evidencia || '-'}}</td>
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

/* Inline Editing */
function editField(el, seq, origem, fieldName) {{
  const currentVal = el.innerText.replace(/^\[Obs\]:\s*/, '');
  el.classList.add('editing');
  el.innerHTML = `<input type="text" value="${{currentVal}}" onblur="saveField(this, '${{seq}}', '${{origem}}', '${{fieldName}}')" onkeydown="if(event.key==='Enter') this.blur()">`;
  el.querySelector('input').focus();
}}

function saveField(input, seq, origem, fieldName) {{
  const val = input.value.trim();
  const item = DATA.master.find(it => it.seq == seq && it.origem == origem);
  if (item) {{
    item[fieldName] = val;
    localStorage.setItem('crialab_inventario_data_2026', JSON.stringify(DATA));
    showToast('Salvo com sucesso!');
  }}
  renderTable();
}}

function editStatus(el, seq, origem) {{
  const item = DATA.master.find(it => it.seq == seq && it.origem == origem);
  if (!item) return;
  el.classList.add('editing');
  el.innerHTML = `
    <select onchange="saveStatusSelect(this, '${{seq}}', '${{origem}}')" onblur="renderTable()">
      <option value="SIM" ${{item.auditado === 'SIM' ? 'selected' : ''}}>Auditado (Localizado)</option>
      <option value="NÃO" ${{item.auditado === 'NÃO' ? 'selected' : ''}}>Pendente</option>
      <option value="EXTERNA" ${{item.auditado === 'EXTERNA' ? 'selected' : ''}}>Em Externa (Estoque Now)</option>
    </select>
  `;
  el.querySelector('select').focus();
}}

function saveStatusSelect(select, seq, origem) {{
  const val = select.value;
  const item = DATA.master.find(it => it.seq == seq && it.origem == origem);
  if (item) {{
    item.auditado = val;
    localStorage.setItem('crialab_inventario_data_2026', JSON.stringify(DATA));
    showToast('Status atualizado!');
  }}
  renderTable();
}}

function editEstado(el, seq, origem) {{
  const item = DATA.master.find(it => it.seq == seq && it.origem == origem);
  if (!item) return;
  el.classList.add('editing');
  el.innerHTML = `
    <select onchange="saveEstadoSelect(this, '${{seq}}', '${{origem}}')" onblur="renderTable()">
      <option value="Normal" ${{item.estado_fisico === 'Normal' ? 'selected' : ''}}>Normal</option>
      <option value="Imperfeição" ${{item.estado_fisico === 'Imperfeição' ? 'selected' : ''}}>Imperfeição</option>
      <option value="Defeito" ${{item.estado_fisico === 'Defeito' ? 'selected' : ''}}>Defeito</option>
      <option value="SUKATECH" ${{item.estado_fisico === 'SUKATECH' ? 'selected' : ''}}>Descarte (SUKATECH)</option>
      <option value="A conferir" ${{item.estado_fisico === 'A conferir' ? 'selected' : ''}}>A conferir</option>
    </select>
  `;
  el.querySelector('select').focus();
}}

function saveEstadoSelect(select, seq, origem) {{
  const val = select.value;
  const item = DATA.master.find(it => it.seq == seq && it.origem == origem);
  if (item) {{
    item.estado_fisico = val;
    localStorage.setItem('crialab_inventario_data_2026', JSON.stringify(DATA));
    showToast('Estado físico atualizado!');
  }}
  renderTable();
}}

function resetEdits() {{
  if (confirm('Tem certeza que deseja restaurar os dados originais? Suas edições locais serão descartadas.')) {{
    localStorage.removeItem('crialab_inventario_data_2026');
    DATA = JSON.parse(JSON.stringify(INITIAL_DATA));
    showToast('Dados restaurados com sucesso!');
    renderTable();
  }}
}}

/* Column Toggles */
function toggleColumnDropdown() {{
  document.getElementById('colDropdown').classList.toggle('show');
}}

window.onclick = function(e) {{
  if (!e.target.matches('.btn-filter') && !e.target.closest('#colDropdown')) {{
    const d = document.getElementById('colDropdown');
    if (d && d.classList.contains('show')) d.classList.remove('show');
  }}
}};

function toggleColumn(checkbox) {{
  const colName = checkbox.getAttribute('data-col');
  visibleColumns[colName] = checkbox.checked;
  
  // Atualiza classes no CSS/tabela
  document.querySelectorAll('.col-' + colName).forEach(el => {{
    el.style.display = checkbox.checked ? '' : 'none';
  }});
}}

/* Export CSV with only visible columns */
function exportCustomCSV() {{
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

  const cols = [];
  if (visibleColumns.origem) cols.push('Origem');
  if (visibleColumns.seq) cols.push('Seq');
  if (visibleColumns.tombamento) cols.push('Nº Tombamento');
  if (visibleColumns.especie) cols.push('Espécie');
  if (visibleColumns.descricao) cols.push('Descrição');
  if (visibleColumns.marca) cols.push('Marca');
  if (visibleColumns.status) cols.push('Status');
  if (visibleColumns.local) cols.push('Local Físico');
  if (visibleColumns.avarias) cols.push('Estado / Imperfeições');
  if (visibleColumns.fotos) cols.push('Fotos');

  const rows = [cols.join(';')];

  filtered.forEach(it => {{
    const r = [];
    if (visibleColumns.origem) r.push('"' + it.origem + '"');
    if (visibleColumns.seq) r.push(it.seq);
    if (visibleColumns.tombamento) r.push('"' + it.tombamento + '"');
    if (visibleColumns.especie) r.push('"' + it.especie + '"');
    if (visibleColumns.descricao) r.push('"' + (it.descricao || '').replace(/"/g, '""') + '"');
    if (visibleColumns.marca) r.push('"' + (it.marca || '') + '"');
    if (visibleColumns.status) r.push('"' + (it.auditado === 'SIM' ? 'Auditado' : (it.auditado === 'EXTERNA' ? 'Em Externa' : 'Pendente')) + '"');
    if (visibleColumns.local) r.push('"' + (it.local_fisico || '') + '"');
    if (visibleColumns.avarias) r.push('"' + (it.estado_fisico || '') + '"');
    if (visibleColumns.fotos) r.push('"' + (it.fotos_evidencia || '') + '"');
    rows.push(r.join(';'));
  }});

  const csvContent = '\uFEFF' + rows.join('\\n');
  const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `inventario_crialab_${{new Date().toISOString().slice(0,10)}}.csv`;
  a.click();
}}

/* File Import for Estoque Now */
function handleFileImport(e) {{
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(evt) {{
    const content = evt.target.result;
    parseEstoqueNow(content);
  }};
  reader.readAsText(file);
}}

function parseEstoqueNow(csvText) {{
  let matched = 0;
  const lines = csvText.split(/\\r?\\n/);
  lines.forEach(line => {{
    const l = line.toUpperCase();
    DATA.master.forEach(it => {{
      const t = String(it.tombamento).replace(/^0+/, '');
      if (t && l.includes(t)) {{
        it.auditado = 'EXTERNA';
        it.local_fisico = 'Em externa / Empréstimo Ativo (Estoque Now)';
        it.observacao_auditoria = 'Item em circulação externa identificado no Estoque Now.';
        matched++;
      }}
    }});
  }});
  localStorage.setItem('crialab_inventario_data_2026', JSON.stringify(DATA));
  showToast(`Estoque Now processado! ${{matched}} itens em externa identificados.`);
  renderTable();
}}

/* Render Photos */
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

/* Render Extras */
function renderExtras() {{
  const tbody = document.getElementById('extrasTableBody');
  tbody.innerHTML = DATA.nao_cadastrados.map(e => `
    <tr>
      <td><strong>${{e.equipamento}}</strong></td>
      <td>${{e.marca}} ${{e.modelo}}</td>
      <td><code>${{e.especificacao_tecnica || e.numero_serie || '-'}}</code></td>
      <td><span class="badge badge-warning">${{e.status_tombamento || 'NÃO TOMBADO'}}</span></td>
      <td>${{e.estado_fisico}}</td>
      <td style="font-size:11.5px; color:#64748b;">${{e.fotos ? e.fotos.join(', ') : '-'}}</td>
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

// Initialize
renderTable();
renderPhotos();
renderExtras();
</script>

</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('index.html and dashboard.html successfully updated with editable fields, metatags, favicon, and column toggles!')
