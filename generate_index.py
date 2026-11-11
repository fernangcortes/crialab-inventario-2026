import json
import os

with open('data/inventario_conciliado.json', encoding='utf-8') as f:
    master_items = json.load(f)

with open('data/sequencia_auditoria_temporal.json', encoding='utf-8') as f:
    cot_sequence = json.load(f)

with open('data/estoquenow_completo.json', encoding='utf-8') as f:
    estoquenow_catalog = json.load(f)

# Load photos data
lote1 = json.load(open('data/auditoria_lote1.json', encoding='utf-8')).get('fotos', [])
lote2 = json.load(open('data/auditoria_lote2.json', encoding='utf-8')).get('fotos', [])
lote3 = json.load(open('data/auditoria_lote3.json', encoding='utf-8')).get('fotos', [])
all_photos = lote1 + lote2 + lote3

payload = {
    'master': master_items,
    'cot_sequence': cot_sequence,
    'estoquenow': estoquenow_catalog,
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
<meta name="keywords" content="CriaLab, Radioteledifusão, UEG, Inventário 2026, Patrimônio, SEI 202600005037287, Estoque Now, Auditoria IA">
<meta name="author" content="Comissão Setorial de Inventário - Fernando Cortes">
<meta property="og:title" content="CriaLab & Radioteledifusão UEG - Inventário 2026">
<meta property="og:description" content="Painel de Auditoria Visual, Reconciliação Estoque Now e Fichas Oficiais SPM/SEAD.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://2026-virid-five.vercel.app">
<link rel="icon" type="image/svg+xml" href="{favicon_svg}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
  :root {{
    --primary: #1565c0;
    --primary-dark: #0d47a1;
    --primary-light: #e3f2fd;
    --accent: #f59e0b;
    --bg: #f8fafc;
    --card: #ffffff;
    --text: #0f172a;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --border-light: #f1f5f9;
    --success: #16a34a;
    --success-bg: #dcfce7;
    --warning: #d97706;
    --warning-bg: #fef3c7;
    --danger: #dc2626;
    --danger-bg: #fee2e2;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.5; }}
  
  /* Topbar */
  .topbar {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 12px 28px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }}
  .brand {{ display: flex; align-items: center; gap: 12px; }}
  .brand-badge {{ background: linear-gradient(135deg, var(--primary), var(--primary-dark)); color: white; padding: 6px 12px; border-radius: 8px; font-weight: 700; font-size: 14px; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(21,101,192,0.3); }}
  .brand-title h1 {{ font-size: 15px; font-weight: 700; color: var(--text); }}
  .brand-title p {{ font-size: 11px; color: var(--text-muted); }}

  .sei-badge {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; background: var(--primary-light); color: var(--primary-dark); padding: 4px 10px; border-radius: 6px; font-weight: 600; border: 1px solid #bbdefb; }}

  /* Container */
  .container {{ max-width: 1480px; margin: 0 auto; padding: 24px 28px; }}

  /* Stats Grid */
  .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .stat-card {{ background: var(--card); border-radius: 12px; padding: 18px 20px; border: 1px solid var(--border-light); box-shadow: 0 1px 3px rgba(0,0,0,0.04); display: flex; flex-direction: column; transition: transform 0.15s, box-shadow 0.15s; }}
  .stat-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.06); }}
  .stat-label {{ font-size: 11.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); margin-bottom: 6px; }}
  .stat-value {{ font-size: 26px; font-weight: 700; color: var(--text); line-height: 1.1; }}
  .stat-desc {{ font-size: 11px; color: var(--text-muted); margin-top: 6px; }}

  /* Tabs Navigation */
  .tabs-nav {{ display: flex; gap: 8px; border-bottom: 2px solid var(--border); margin-bottom: 24px; overflow-x: auto; }}
  .tab-btn {{ background: none; border: none; padding: 12px 18px; font-size: 13.5px; font-weight: 600; color: var(--text-muted); cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px; transition: all 0.2s; white-space: nowrap; }}
  .tab-btn:hover {{ color: var(--primary); }}
  .tab-btn.active {{ color: var(--primary); border-bottom-color: var(--primary); }}

  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}

  /* Filters & Controls */
  .controls-bar {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; margin-bottom: 16px; background: var(--card); padding: 14px 18px; border-radius: 10px; border: 1px solid var(--border-light); }}
  .search-box {{ flex: 1; min-width: 260px; position: relative; }}
  .search-box input {{ width: 100%; padding: 8px 12px 8px 34px; border-radius: 6px; border: 1px solid var(--border); font-size: 13px; font-family: inherit; outline: none; transition: border-color 0.2s; }}
  .search-box input:focus {{ border-color: var(--primary); }}
  .search-box::before {{ content: '🔍'; position: absolute; left: 10px; top: 50%; transform: translateY(-50%); font-size: 13px; opacity: 0.5; }}

  .filter-group {{ display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }}
  .filter-label {{ font-size: 12px; font-weight: 600; color: var(--text-muted); margin-right: 4px; }}
  .btn-filter {{ background: var(--bg); border: 1px solid var(--border); padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 500; cursor: pointer; transition: all 0.15s; color: var(--text); }}
  .btn-filter:hover {{ background: #e2e8f0; }}
  .btn-filter.active {{ background: var(--primary); color: white; border-color: var(--primary); }}

  .btn-action {{ background: var(--primary); color: white; border: none; padding: 7px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: background 0.15s; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; }}
  .btn-action:hover {{ background: var(--primary-dark); }}
  .btn-secondary {{ background: #f1f5f9; color: var(--text); border: 1px solid var(--border); }}
  .btn-secondary:hover {{ background: #e2e8f0; }}

  /* Column Visibility Dropdown */
  .dropdown {{ position: relative; display: inline-block; }}
  .dropdown-menu {{ display: none; position: absolute; right: 0; top: 100%; background: white; min-width: 250px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border-radius: 8px; border: 1px solid var(--border); padding: 12px; z-index: 999; margin-top: 5px; max-height: 400px; overflow-y: auto; }}
  .dropdown-menu.show {{ display: block; }}
  .dropdown-header {{ font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px; padding-bottom: 5px; border-bottom: 1px solid var(--border-light); }}
  .col-toggle-item {{ display: flex; align-items: center; gap: 8px; padding: 6px 4px; font-size: 12.5px; cursor: pointer; }}
  
  /* Tables */
  .table-container {{ background: var(--card); border-radius: 12px; border: 1px solid var(--border-light); overflow-x: auto; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
  table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 12.5px; }}
  th {{ background: #f8fafc; padding: 12px 14px; font-weight: 700; color: #475569; border-bottom: 1px solid var(--border); white-space: nowrap; user-select: none; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid var(--border-light); vertical-align: middle; }}
  tr:hover {{ background: #f8fafc; }}
  
  /* Sortable Table Headers */
  th.sortable {{ cursor: pointer; position: relative; transition: background 0.15s, color 0.15s; }}
  th.sortable:hover {{ background: #e2e8f0; color: var(--primary); }}
  th.sortable::after {{ content: ' ⇅'; opacity: 0.3; font-size: 11px; margin-left: 6px; display: inline-block; }}
  th.sortable.sort-asc::after {{ content: ' ▲'; opacity: 1; color: var(--primary); font-weight: 900; }}
  th.sortable.sort-desc::after {{ content: ' ▼'; opacity: 1; color: var(--primary); font-weight: 900; }}

  /* Editable Cells */
  .editable-cell {{ cursor: pointer; position: relative; border-radius: 4px; padding: 2px 4px; transition: background 0.15s; }}
  .editable-cell:hover {{ background: #e0f2fe; outline: 1px dashed var(--primary); }}
  .editing {{ padding: 0 !important; }}
  .editing input, .editing select {{ width: 100%; padding: 6px 8px; border: 2px solid var(--primary); border-radius: 4px; font-size: 12px; outline: none; background: #fff; }}
  
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
  .photo-meta {{ font-size: 11.5px; color: var(--text-muted); line-height: 1.6; }}

  /* Spaces Grid */
  .spaces-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }}
  .space-box {{ background: var(--card); border-radius: 10px; border: 1px solid var(--border); padding: 16px; }}
  .space-box h3 {{ font-size: 14px; font-weight: 700; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }}
  .space-box p {{ font-size: 12px; color: var(--text-muted); margin-bottom: 10px; }}

  /* Modal */
  .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(4px); align-items: center; justify-content: center; }}
  .modal.active {{ display: flex; }}
  .modal-content {{ max-width: 90%; max-height: 90%; position: relative; }}
  .modal-content img {{ max-width: 100%; max-height: 85vh; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
  .close-modal {{ position: absolute; top: -35px; right: 0; color: white; font-size: 28px; cursor: pointer; }}

  /* Toast Notification */
  .toast {{ position: fixed; bottom: 24px; right: 24px; background: #0f172a; color: white; padding: 12px 20px; border-radius: 8px; font-size: 13px; font-weight: 500; box-shadow: 0 10px 25px rgba(0,0,0,0.2); z-index: 9999; display: none; align-items: center; gap: 8px; }}
  .toast.show {{ display: flex; animation: slideUp 0.3s ease; }}
  @keyframes slideUp {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}

  /* Print Styles */
  @media print {{
    .topbar, .tabs-nav, .controls-bar, .btn-action, .btn-filter, #toast, .sei-badge {{ display: none !important; }}
    body {{ background: white; color: black; }}
    .table-container {{ border: none; box-shadow: none; }}
    table {{ font-size: 10px; }}
    th, td {{ padding: 6px 8px; border: 1px solid #ccc; }}
    .tab-content {{ display: none !important; }}
    #tab-tabela {{ display: block !important; }}
    th.sortable::after {{ display: none !important; }}
  }}
</style>
</head>
<body>

<!-- Topbar -->
<header class="topbar">
  <div class="brand">
    <div class="brand-badge">CriaLab & Rádio</div>
    <div class="brand-title">
      <h1>Inventário Físico & Reconciliação Patrimonial 2026</h1>
      <p>Unidade Universitária Goiânia - Laranjeiras | Universidade Estadual de Goiás</p>
    </div>
  </div>
  <div style="display: flex; gap: 12px; align-items: center;">
    <span class="sei-badge">SEI nº 202600005037287</span>
    <a href="guia_fotografia_3d_ar.html" target="_blank" class="btn-action" style="background:#0284c7;">📐 Guia Fotográfico 3D/AR</a>
  </div>
</header>

<div class="container">

  <!-- Stats Cards -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-label">Acervo Total Oficio</div>
      <div class="stat-value">377 <span style="font-size:14px; font-weight:400; color:var(--text-muted);">bens</span></div>
      <div class="stat-desc">285 CriaLab + 92 Radioteledifusão</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Estoque Now (Ativo)</div>
      <div class="stat-value" style="color:var(--primary);">245 <span style="font-size:14px; font-weight:400; color:var(--text-muted);">itens</span></div>
      <div class="stat-desc">Catálogo extraído de <code>estoquenow.pdf</code></div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Itens Auditados (COT)</div>
      <div class="stat-value" style="color:var(--success);">14 <span style="font-size:14px; font-weight:400; color:var(--text-muted);">equipamentos</span></div>
      <div class="stat-desc">5 com tombamento + 9 sem tombamento</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Fotos COT Processadas</div>
      <div class="stat-value" style="color:#7c3aed;">31 <span style="font-size:14px; font-weight:400; color:var(--text-muted);">fotos</span></div>
      <div class="stat-desc">Central de Operação Técnica (Lotes 1, 2 e 3)</div>
    </div>
  </div>

  <!-- Tabs Nav -->
  <nav class="tabs-nav">
    <button class="tab-btn active" onclick="switchTab('tab-tabela')">📋 Inventário Geral (377 Bens)</button>
    <button class="tab-btn" onclick="switchTab('tab-cot')">🔍 Auditoria COT (14 Itens Mapeados)</button>
    <button class="tab-btn" onclick="switchTab('tab-fotos')">📸 Fotos COT (31 Imagens)</button>
    <button class="tab-btn" onclick="switchTab('tab-estoquenow')">📦 Estoque Now (245 Itens)</button>
    <button class="tab-btn" onclick="switchTab('tab-espacos')">🏢 Planta & Espaços (8 Áreas)</button>
    <button class="tab-btn" onclick="switchTab('tab-fichas')">📑 Fichas SPM / SEAD</button>
  </nav>

  <!-- TAB 1: Tabela Geral Conciliada -->
  <div id="tab-tabela" class="tab-content active">
    
    <div class="controls-bar">
      <div class="search-box">
        <input type="text" id="searchInput" placeholder="Buscar por tombamento, descrição, marca, espécie ou local..." onkeyup="filterTable()">
      </div>

      <div class="filter-group">
        <span class="filter-label">Origem:</span>
        <button class="btn-filter active" onclick="setOriginFilter('ALL', this)">Todos</button>
        <button class="btn-filter" onclick="setOriginFilter('CRIA LAB', this)">CriaLab (285)</button>
        <button class="btn-filter" onclick="setOriginFilter('RADIO UEG', this)">Rádio (92)</button>
      </div>

      <div class="filter-group">
        <span class="filter-label">Status:</span>
        <button class="btn-filter active" onclick="setStatusFilter('ALL', this)">Todos</button>
        <button class="btn-filter" onclick="setStatusFilter('AUDITED', this)">Auditados</button>
        <button class="btn-filter" onclick="setStatusFilter('DIVERGENCE', this)">Divergências</button>
      </div>

      <div style="display: flex; gap: 8px;">
        <!-- Colunas Dropdown -->
        <div class="dropdown">
          <button class="btn-filter btn-secondary" onclick="toggleColumnDropdown()">👁️ Ocultar / Exibir Colunas ▾</button>
          <div id="colDropdown" class="dropdown-menu">
            <div class="dropdown-header">Colunas do Inventário</div>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="origem" onchange="toggleColumn(this)"> Origem</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="seq" onchange="toggleColumn(this)"> Seq</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="tombamento" onchange="toggleColumn(this)"> Tombamento</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="especie" onchange="toggleColumn(this)"> Espécie</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="descricao" onchange="toggleColumn(this)"> Descrição</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="marca" onchange="toggleColumn(this)"> Marca</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="status" onchange="toggleColumn(this)"> Status Auditoria</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="local" onchange="toggleColumn(this)"> Local Físico</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="avarias" onchange="toggleColumn(this)"> Estado / Imperfeições</label>
            <label class="col-toggle-item"><input type="checkbox" checked data-col="fotos" onchange="toggleColumn(this)"> Fotos Evidência</label>
          </div>
        </div>

        <button class="btn-filter btn-secondary" onclick="exportCustomCSV()">📥 Exportar CSV (Visíveis)</button>
        <button class="btn-action" onclick="window.print()">🖨️ Imprimir / PDF</button>
        <button class="btn-filter btn-secondary" style="color:var(--danger);" onclick="resetEdits()">↺ Restaurar</button>
      </div>
    </div>

    <div style="margin-bottom: 12px; font-size: 12px; color: var(--text-muted); display:flex; justify-content:space-between; align-items:center;">
      <span>💡 <em>Dica: <strong>Clique em qualquer cabeçalho de coluna</strong> para ordenar (crescente/decrescente). Dê duplo-clique nas células de <strong>Status</strong>, <strong>Local</strong>, <strong>Estado</strong> ou <strong>Observações</strong> para editar diretamente os dados.</em></span>
      <span id="saveStatus" style="font-weight:600; color:var(--success);">✓ Dados sincronizados localmente</span>
    </div>

    <div class="table-container">
      <table id="mainTable">
        <thead>
          <tr>
            <th class="col-origem sortable" data-field="origem" onclick="sortBy('origem')" title="Clique para ordenar por Origem">Origem</th>
            <th class="col-seq sortable sort-asc" data-field="seq" onclick="sortBy('seq')" title="Clique para ordenar por Sequência">Seq</th>
            <th class="col-tombamento sortable" data-field="tombamento" onclick="sortBy('tombamento')" title="Clique para ordenar por Nº Tombamento">Tombamento</th>
            <th class="col-especie sortable" data-field="especie" onclick="sortBy('especie')" title="Clique para ordenar por Espécie">Espécie</th>
            <th class="col-descricao sortable" data-field="descricao" onclick="sortBy('descricao')" title="Clique para ordenar por Descrição">Descrição</th>
            <th class="col-marca sortable" data-field="marca" onclick="sortBy('marca')" title="Clique para ordenar por Marca">Marca</th>
            <th class="col-status sortable" data-field="auditado" onclick="sortBy('auditado')" title="Clique para ordenar por Status de Auditoria">Status Auditoria</th>
            <th class="col-local sortable" data-field="local_fisico" onclick="sortBy('local_fisico')" title="Clique para ordenar por Local Físico">Local Físico</th>
            <th class="col-avarias sortable" data-field="estado_fisico" onclick="sortBy('estado_fisico')" title="Clique para ordenar por Estado / Imperfeições">Estado / Imperfeições</th>
            <th class="col-fotos sortable" data-field="fotos_evidencia" onclick="sortBy('fotos_evidencia')" title="Clique para ordenar por Fotos">Fotos</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </div>

  <!-- TAB 2: Itens da COT (Sequência Cronológica de 14 Itens) -->
  <div id="tab-cot" class="tab-content">
    <div style="background: #e0f2fe; border-left: 4px solid var(--primary); padding: 14px 18px; margin-bottom: 20px; font-size: 13px; border-radius: 0 8px 8px 0;">
      <strong>Regra Operacional de Captura:</strong> As 31 fotos foram tiradas estritamente em ordem temporal para cada equipamento:
      <strong>1. Visão Geral do Equipamento</strong> ➔ <strong>2. Especificação Técnica / Serial</strong> ➔ <strong>3. Plaqueta de Tombamento (se houver)</strong>.
      Quando não há a 3ª foto de tombamento, significa que <strong>o equipamento não estava tombado fisicamente</strong>.
    </div>

    <div class="table-container">
      <table id="cotTable">
        <thead>
          <tr>
            <th class="sortable sort-asc" data-field="id" onclick="sortCOTBy('id')" title="Clique para ordenar por Item #">Item #</th>
            <th class="sortable" data-field="equipamento" onclick="sortCOTBy('equipamento')" title="Clique para ordenar por Equipamento">Equipamento</th>
            <th class="sortable" data-field="marca" onclick="sortCOTBy('marca')" title="Clique para ordenar por Marca/Modelo">Marca / Modelo</th>
            <th class="sortable" data-field="status_tombamento" onclick="sortCOTBy('status_tombamento')" title="Clique para ordenar por Situação">Situação Patrimonial</th>
            <th class="sortable" data-field="tombamento_oficial" onclick="sortCOTBy('tombamento_oficial')" title="Clique para ordenar por Tombamento">Tombamento Oficial</th>
            <th class="sortable" data-field="especificacao_tecnica" onclick="sortCOTBy('especificacao_tecnica')" title="Clique para ordenar por Specs/Serial">Especificação Técnica / Serial</th>
            <th class="sortable" data-field="estado_fisico" onclick="sortCOTBy('estado_fisico')" title="Clique para ordenar por Estado Físico">Estado Físico</th>
            <th class="sortable" data-field="fotos" onclick="sortCOTBy('fotos')" title="Clique para ordenar por Fotos">Fotos na Sequência</th>
          </tr>
        </thead>
        <tbody id="cotTableBody"></tbody>
      </table>
    </div>
  </div>

  <!-- TAB 3: Fotos COT -->
  <div id="tab-fotos" class="tab-content">
    <div style="margin-bottom: 15px; font-size: 13px; color: var(--text-muted);">
      31 fotografias da Central de Operação Técnica (COT) processadas por agentes de IA com identificação de placas, números de série e avarias:
    </div>
    <div class="photo-grid" id="photoGrid"></div>
  </div>

  <!-- TAB 4: Estoque Now -->
  <div id="tab-estoquenow" class="tab-content">
    <div style="background: #fef3c7; border-left: 4px solid var(--warning); padding: 16px 20px; margin-bottom: 20px; font-size: 13px; border-radius: 0 8px 8px 0;">
      <strong>⚠️ Diretriz Oficial sobre Bens em Externa:</strong>
      Estar no Estoque Now ou em locação/externa <strong>NÃO serve como justificativa final perante o SEI</strong>.
      Como o prazo será prorrogado, o procedimento obrigatório é: <strong>quando o equipamento retornar ao laboratório, tirar as fotos na sequência (Geral ➔ Specs ➔ Placa) e atualizar o sistema aqui via IA para auditá-lo oficialmente com fotos.</strong>
    </div>

    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; flex-wrap:wrap; gap:10px;">
      <div style="font-size:14px; font-weight:700;">
        Catálogo do Estoque Now Extraído de <code>data/estoquenow.pdf</code> (245 itens operacionais):
      </div>
      <div style="width:300px;">
        <input type="text" id="searchEstoque" placeholder="🔍 Filtrar no Estoque Now..." onkeyup="filterEstoqueTable()" style="width:100%; padding:8px 12px; border:1px solid var(--border); border-radius:6px; font-size:12px;">
      </div>
    </div>

    <div class="table-container">
      <table id="estoqueTable">
        <thead>
          <tr>
            <th class="sortable" data-field="codigo" onclick="sortEstoqueBy('codigo')" title="Clique para ordenar por Código">Código</th>
            <th class="sortable sort-asc" data-field="nome" onclick="sortEstoqueBy('nome')" title="Clique para ordenar por Nome">Nome do Equipamento (Estoque Now)</th>
            <th class="sortable" data-field="barcode" onclick="sortEstoqueBy('barcode')" title="Clique para ordenar por Código de Barras">Código de Barras</th>
            <th class="sortable" data-field="em_manutencao" onclick="sortEstoqueBy('em_manutencao')" title="Clique para ordenar por Manutenção">Alerta Manutenção</th>
            <th>Ação no Retorno da Externa</th>
          </tr>
        </thead>
        <tbody id="estoqueTableBody"></tbody>
      </table>
    </div>
  </div>

  <!-- TAB 5: Espaços CriaLab (Planta Baixa) -->
  <div id="tab-espacos" class="tab-content">
    <div style="margin-bottom: 20px; font-size: 13px; color: var(--text-muted);">
      Estrutura de cômodos do CriaLab / Radioteledifusão conforme plantas oficiais (Layout R05/2025):
    </div>
    <div class="spaces-grid">
      <div class="space-box">
        <h3>1. Sala de Operação Técnica (COT) <span class="badge badge-audited">Auditado (14 itens / 31 fotos)</span></h3>
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

let localData = localStorage.getItem('crialab_inventario_data_2026');
let DATA = localData ? JSON.parse(localData) : INITIAL_DATA;

// Ensure cot_sequence and estoquenow are available
DATA.cot_sequence = INITIAL_DATA.cot_sequence;
DATA.estoquenow = INITIAL_DATA.estoquenow;

let currentOrigin = 'ALL';
let currentStatus = 'ALL';

let sortState = {{
  field: 'seq',
  direction: 'asc'
}};

let cotSortState = {{
  field: 'id',
  direction: 'asc'
}};

let estoqueSortState = {{
  field: 'nome',
  direction: 'asc'
}};

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
  if (window.event && window.event.target) window.event.target.classList.add('active');
}}

/* Sorting Functions */
function sortBy(field) {{
  if (sortState.field === field) {{
    sortState.direction = sortState.direction === 'asc' ? 'desc' : 'asc';
  }} else {{
    sortState.field = field;
    sortState.direction = 'asc';
  }}
  updateSortHeaders();
  renderTable();
}}

function updateSortHeaders() {{
  document.querySelectorAll('#mainTable th.sortable').forEach(th => {{
    th.classList.remove('sort-asc', 'sort-desc');
    if (th.getAttribute('data-field') === sortState.field) {{
      th.classList.add(sortState.direction === 'asc' ? 'sort-asc' : 'sort-desc');
    }}
  }});
}}

function sortCOTBy(field) {{
  if (cotSortState.field === field) {{
    cotSortState.direction = cotSortState.direction === 'asc' ? 'desc' : 'asc';
  }} else {{
    cotSortState.field = field;
    cotSortState.direction = 'asc';
  }}
  updateCOTSortHeaders();
  renderCOTSequence();
}}

function updateCOTSortHeaders() {{
  document.querySelectorAll('#cotTable th.sortable').forEach(th => {{
    th.classList.remove('sort-asc', 'sort-desc');
    if (th.getAttribute('data-field') === cotSortState.field) {{
      th.classList.add(cotSortState.direction === 'asc' ? 'sort-asc' : 'sort-desc');
    }}
  }});
}}

function sortEstoqueBy(field) {{
  if (estoqueSortState.field === field) {{
    estoqueSortState.direction = estoqueSortState.direction === 'asc' ? 'desc' : 'asc';
  }} else {{
    estoqueSortState.field = field;
    estoqueSortState.direction = 'asc';
  }}
  updateEstoqueSortHeaders();
  renderEstoqueNow();
}}

function updateEstoqueSortHeaders() {{
  document.querySelectorAll('#estoqueTable th.sortable').forEach(th => {{
    th.classList.remove('sort-asc', 'sort-desc');
    if (th.getAttribute('data-field') === estoqueSortState.field) {{
      th.classList.add(estoqueSortState.direction === 'asc' ? 'sort-asc' : 'sort-desc');
    }}
  }});
}}

function renderTable() {{
  const tbody = document.getElementById('tableBody');
  const search = document.getElementById('searchInput').value.toLowerCase();
  
  let filtered = DATA.master.filter(it => {{
    if (currentOrigin !== 'ALL' && it.origem !== currentOrigin) return false;
    if (currentStatus === 'AUDITED' && it.auditado !== 'SIM') return false;
    if (currentStatus === 'DIVERGENCE' && !it.divergencia_carga.startsWith('SIM')) return false;
    
    if (search) {{
      const text = (it.tombamento + ' ' + it.especie + ' ' + it.descricao + ' ' + it.marca + ' ' + it.origem + ' ' + it.local_fisico + ' ' + (it.observacao_auditoria || '')).toLowerCase();
      if (!text.includes(search)) return false;
    }}
    return true;
  }});

  // Sort filtered list
  filtered.sort((a, b) => {{
    let va = a[sortState.field];
    let vb = b[sortState.field];
    if (va === undefined || va === null) va = '';
    if (vb === undefined || vb === null) vb = '';

    if (sortState.field === 'seq') {{
      const na = parseInt(va, 10) || 0;
      const nb = parseInt(vb, 10) || 0;
      return sortState.direction === 'asc' ? na - nb : nb - na;
    }}

    const cmp = va.toString().localeCompare(vb.toString(), 'pt-BR', {{ numeric: true, sensitivity: 'base' }});
    return sortState.direction === 'asc' ? cmp : -cmp;
  }});

  tbody.innerHTML = filtered.map((it) => {{
    const badgeOrigem = it.origem === 'CRIA LAB' ? 'badge-crialab' : 'badge-radio';
    const badgeAudit = it.auditado === 'SIM' ? 'badge-audited' : 'badge-pending';
    const badgeText = it.auditado === 'SIM' ? 'Auditado' : 'Pendente';
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
  if (confirm('Restaurar dados originais? Suas edições locais serão descartadas.')) {{
    localStorage.removeItem('crialab_inventario_data_2026');
    DATA = JSON.parse(JSON.stringify(INITIAL_DATA));
    showToast('Dados restaurados!');
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
  document.querySelectorAll('.col-' + colName).forEach(el => {{
    el.style.display = checkbox.checked ? '' : 'none';
  }});
}}

/* Export CSV with visible columns and active sort */
function exportCustomCSV() {{
  const search = document.getElementById('searchInput').value.toLowerCase();
  let filtered = DATA.master.filter(it => {{
    if (currentOrigin !== 'ALL' && it.origem !== currentOrigin) return false;
    if (currentStatus === 'AUDITED' && it.auditado !== 'SIM') return false;
    if (currentStatus === 'DIVERGENCE' && !it.divergencia_carga.startsWith('SIM')) return false;
    if (search) {{
      const text = (it.tombamento + ' ' + it.especie + ' ' + it.descricao + ' ' + it.marca + ' ' + it.origem).toLowerCase();
      if (!text.includes(search)) return false;
    }}
    return true;
  }});

  // Apply current sort order to export
  filtered.sort((a, b) => {{
    let va = a[sortState.field];
    let vb = b[sortState.field];
    if (va === undefined || va === null) va = '';
    if (vb === undefined || vb === null) vb = '';
    if (sortState.field === 'seq') {{
      const na = parseInt(va, 10) || 0;
      const nb = parseInt(vb, 10) || 0;
      return sortState.direction === 'asc' ? na - nb : nb - na;
    }}
    const cmp = va.toString().localeCompare(vb.toString(), 'pt-BR', {{ numeric: true, sensitivity: 'base' }});
    return sortState.direction === 'asc' ? cmp : -cmp;
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
    if (visibleColumns.status) r.push('"' + (it.auditado === 'SIM' ? 'Auditado' : 'Pendente') + '"');
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

/* Render COT Items Sequence Table */
function renderCOTSequence() {{
  const tbody = document.getElementById('cotTableBody');
  const items = [...DATA.cot_sequence];

  items.sort((a, b) => {{
    let va = a[cotSortState.field];
    let vb = b[cotSortState.field];
    if (va === undefined || va === null) va = '';
    if (vb === undefined || vb === null) vb = '';

    if (cotSortState.field === 'id') {{
      const na = parseInt(va, 10) || 0;
      const nb = parseInt(vb, 10) || 0;
      return cotSortState.direction === 'asc' ? na - nb : nb - na;
    }}

    if (Array.isArray(va)) va = va.join(', ');
    if (Array.isArray(vb)) vb = vb.join(', ');
    const cmp = va.toString().localeCompare(vb.toString(), 'pt-BR', {{ numeric: true, sensitivity: 'base' }});
    return cotSortState.direction === 'asc' ? cmp : -cmp;
  }});

  tbody.innerHTML = items.map(it => {{
    const isTomb = it.tombamento_oficial ? true : false;
    const badgeStatus = isTomb ? 'badge-audited' : 'badge-divergence';
    
    return `<tr>
      <td style="font-weight:700; text-align:center;">${{it.id}}</td>
      <td><strong>${{it.equipamento}}</strong></td>
      <td>${{it.marca}} ${{it.modelo}}</td>
      <td><span class="badge ${{badgeStatus}}">${{it.status_tombamento}}</span></td>
      <td style="font-weight:700; color:var(--primary);">${{it.tombamento_oficial || '-'}}</td>
      <td><code>${{it.especificacao_tecnica}}</code></td>
      <td>${{it.estado_fisico}}</td>
      <td style="font-size:11px; color:#64748b;">${{it.fotos.join('<br>')}}</td>
    </tr>`;
  }}).join('');
}}

/* Render Estoque Now Table */
function renderEstoqueNow() {{
  const tbody = document.getElementById('estoqueTableBody');
  const search = (document.getElementById('searchEstoque') ? document.getElementById('searchEstoque').value : '').toLowerCase();
  
  let filtered = DATA.estoquenow.filter(it => {{
    if (!search) return true;
    return (it.codigo + ' ' + it.nome + ' ' + it.barcode).toLowerCase().includes(search);
  }});

  filtered.sort((a, b) => {{
    let va = a[estoqueSortState.field];
    let vb = b[estoqueSortState.field];
    if (va === undefined || va === null) va = '';
    if (vb === undefined || vb === null) vb = '';
    const cmp = va.toString().localeCompare(vb.toString(), 'pt-BR', {{ numeric: true, sensitivity: 'base' }});
    return estoqueSortState.direction === 'asc' ? cmp : -cmp;
  }});

  tbody.innerHTML = filtered.map(it => `
    <tr>
      <td style="font-weight:700; color:var(--primary); font-family:monospace;">${{it.codigo}}</td>
      <td><strong>${{it.nome}}</strong></td>
      <td style="font-family:monospace; color:#64748b;">${{it.barcode}}</td>
      <td>${{it.em_manutencao === 'Sim' ? '<span class="badge badge-danger">Em Manutenção</span>' : '<span style="color:#64748b;">Operacional</span>'}}</td>
      <td style="font-size:11.5px; color:#1565c0;">Tirar fotos no retorno (Geral ➔ Specs ➔ Placa) para auditoria por IA</td>
    </tr>
  `).join('');
}}

function filterEstoqueTable() {{
  renderEstoqueNow();
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
renderCOTSequence();
renderEstoqueNow();
renderPhotos();
</script>

</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated index.html and dashboard.html with interactive column sorting for all tables!')
