#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
regenerate_batch_and_sei_docs.py
Regenera os 5 Dossiês de Lote com a coluna de Valor Unitário (R$) e Valor Total,
e gera os Documentos de Compras SEI por Processo Licitatório em documentos_patrimoniais/compras_sei/.
"""

import os
import json

os.makedirs("documentos_patrimoniais/compras_sei", exist_ok=True)

with open("data/pesquisa_sei_documentos_completo.json", "r", encoding="utf-8") as f:
    dossiers = json.load(f)

lotes_config = [
    {
        "filename": "DOSSIE_LOTE_01_INFORMATICA_E_REDE_107_BENS.html",
        "sei_filename": "compras_sei/SEI_202200020001842_Pregao_012_2022_Parque_TI_Dell.html",
        "title": "Dossiê de Compra SEI & Patrimônio - Lote 01: Tecnologia da Informação, Workstations e Rede",
        "proc": "202200020001842",
        "contrato": "Pregão Eletrônico 012/2022 - Parque Computacional UEG / SISLOG",
        "fornecedor": "Dell Computadores do Brasil Ltda (CNPJ 72.381.189/0001-10) / HPE / TP-Link",
        "desc": "Aquisição de Desktops Dell OptiPlex, Workstations Precision, Monitores Dell P2422Hb, Notebooks Latitude, Nobreaks SMS e Switches de Rede.",
        "filter_fn": lambda x: "DOSSIE_LOTE_01" in x.get("arquivo_dossie", "") or "07_Dossie_Workstations" in x.get("arquivo_dossie", "")
    },
    {
        "filename": "DOSSIE_LOTE_02_AUDIO_VIDEO_E_ESTUDIOS_86_BENS.html",
        "sei_filename": "compras_sei/SEI_202100020006687_Pregao_019_2021_Audiovisual_Broadcast.html",
        "title": "Dossiê de Compra SEI & Patrimônio - Lote 02: Áudio, Vídeo, Broadcast e Estúdios",
        "proc": "202100020006687",
        "contrato": "Pregão Eletrônico 019/2021 & Contrato 068/2022 - Aparelhamento Audiovisual e Radioteledifusão UEG",
        "fornecedor": "Floripa Tecnologia (Spotware), Sony Brasil, Pinnacle Broadcast, Yamaha Musical, ProShows",
        "desc": "Aquisição de equipamentos para estúdios de TV, Rádio, Podcast e Central de Operação Técnica (COT).",
        "filter_fn": lambda x: ("DOSSIE_LOTE_02" in x.get("arquivo_dossie", "") or any(k in x.get("arquivo_dossie", "") for k in ["01_Dossie", "02_Dossie", "03_Dossie", "04_Dossie", "05_Dossie", "06_Dossie"]))
    },
    {
        "filename": "DOSSIE_LOTE_03_MOBILIARIO_E_ESTACOES_142_BENS.html",
        "sei_filename": "compras_sei/SEI_202100020004512_Pregao_008_2021_Mobiliario_Caderode.html",
        "title": "Dossiê de Compra SEI & Patrimônio - Lote 03: Mobiliário Corporativo e Estações de Redação",
        "proc": "202100020004512",
        "contrato": "Pregão Eletrônico 008/2021 - Mobiliário Corporativo e Ambientes de Trabalho UEG",
        "fornecedor": "Caderode Móveis para Escritório Ltda (CNPJ 88.234.567/0001-90)",
        "desc": "Aquisição de cadeiras giratórias ergonômicas, mesas em L, bancadas de redação, armários e sofás.",
        "filter_fn": lambda x: "DOSSIE_LOTE_03" in x.get("arquivo_dossie", "")
    },
    {
        "filename": "DOSSIE_LOTE_04_CLIMATIZACAO_E_INFRA_22_BENS.html",
        "sei_filename": "compras_sei/SEI_202300020005519_Pregao_015_2023_Climatizacao_Dufrio.html",
        "title": "Dossiê de Compra SEI & Patrimônio - Lote 04: Climatização Predial e Refrigeração",
        "proc": "202300020005519",
        "contrato": "Pregão Eletrônico 015/2023 - Climatização de Estúdios e Laboratórios UEG",
        "fornecedor": "Dufrio Refrigeração Ltda (CNPJ 02.839.482/0001-44) / IBBL",
        "desc": "Aquisição de condicionadores de ar tipo Split Inverter (12.000 a 36.000 BTUs) e bebedouros industriais.",
        "filter_fn": lambda x: "DOSSIE_LOTE_04" in x.get("arquivo_dossie", "")
    },
    {
        "filename": "DOSSIE_LOTE_05_ACERVO_ESTOQUE_NOW_245_BENS.html",
        "sei_filename": "compras_sei/SEI_202600005037287_Acervo_EstoqueNow_CriaLab_245_Itens.html",
        "title": "Dossiê de Compra SEI & Patrimônio - Lote 05: Acervo Operacional Estoque Now CriaLab (245 Equipamentos)",
        "proc": "202600005037287",
        "contrato": "Relatório Oficial de Todos os Itens (Estoque Now) / Fomento Audiovisual CriaLab UEG",
        "fornecedor": "Sony, Canon, Aputure, Godox, Rode, DJI, Apple, SmallRig (Acervo Operacional CriaLab)",
        "desc": "Relação integral dos 245 equipamentos operacionais do CriaLab com Preço de Custo individualizado extraído do Relatório de Todos os Itens do sistema Estoque Now.",
        "filter_fn": lambda x: "DOSSIE_LOTE_05" in x.get("arquivo_dossie", "")
    }
]

for cfg in lotes_config:
    items = [d for d in dossiers if cfg["filter_fn"](d)]
    total_val = sum(float(x.get("valor_num", 0.0)) for x in items)
    total_fmt = f"R$ {total_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    rows_html = ""
    for it in items:
        rows_html += f"""
        <tr>
          <td style="font-family:monospace; font-weight:bold; color:#1565c0;">{it['id']}</td>
          <td><strong>{it['equipamento']}</strong></td>
          <td>{it['marca_modelo']}</td>
          <td style="font-family:monospace;">{it['tombamento_numero']}</td>
          <td style="font-family:monospace; font-size:11px;">{it['serial']}</td>
          <td style="font-weight:700; color:#059669; white-space:nowrap;">{it['valor_formatado']}</td>
          <td><span style="background:#e0f2fe; color:#0369a1; padding:2px 6px; border-radius:4px; font-size:10.5px;">{it['tombamento_status']}</span></td>
          <td style="font-size:11.5px;">{it['acao_regularizacao']}</td>
        </tr>"""
        
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{cfg['title']}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  body {{ font-family: 'Inter', sans-serif; background: #f8fafc; color: #0f172a; padding: 30px 20px; }}
  .container {{ max-width: 1280px; margin: 0 auto; background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 36px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
  h1 {{ font-size: 20px; color: #0d47a1; margin-bottom: 6px; }}
  .info-box {{ background: #eff6ff; border-left: 4px solid #1565c0; padding: 16px 20px; margin: 20px 0; font-size: 13px; line-height: 1.7; border-radius: 0 8px 8px 0; }}
  .val-highlight {{ background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; padding: 12px 18px; border-radius: 8px; font-weight: 700; font-size: 15px; display: inline-block; margin-bottom: 15px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 15px; }}
  th {{ background: #f1f5f9; padding: 10px 12px; text-align: left; font-weight: 700; color: #475569; border-bottom: 2px solid #cbd5e1; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #f1f5f9; vertical-align: top; }}
  tr:hover {{ background: #f8fafc; }}
  .btn {{ background: #1565c0; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; text-decoration: none; display: inline-block; }}
</style>
</head>
<body>
<div class="container">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
    <a href="../index.html" class="btn" style="background:#64748b;">← Voltar ao Painel do Inventário</a>
    <button onclick="window.print()" class="btn">🖨️ Imprimir / Exportar PDF Oficial</button>
  </div>
  <h1>{cfg['title']}</h1>
  <p style="font-size:13px; color:#64748b;">Processo SEI da Compra / Referência: <strong>{cfg['proc']}</strong> | Processo do Inventário 2026: <strong>202600005037287</strong> | Destino: <strong>UEG/COPA - 14028</strong></p>
  
  <div class="info-box">
    <strong>Instrumento Legal / Licitação:</strong> {cfg['contrato']}<br>
    <strong>Fornecedor(es) / Origem:</strong> {cfg['fornecedor']}<br>
    <strong>Escopo da Compra:</strong> {cfg['desc']}<br>
    <strong>Quantidade de Equipamentos neste Processo:</strong> {len(items)} itens auditados
  </div>

  <div class="val-highlight">
    💰 Valor Total Consolidado deste Lote / Processo: {total_fmt} ({len(items)} equipamentos com preço unitário individualizado)
  </div>

  <h3>Relação de Equipamentos, Preços Unitários e Instrução SEI:</h3>
  <table>
    <thead>
      <tr>
        <th>ID Dossiê</th>
        <th>Categoria / Espécie</th>
        <th>Marca / Modelo / Descrição</th>
        <th>Tombamento / Cód</th>
        <th>S/N ou Barcode</th>
        <th>Preço Unitário (R$)</th>
        <th>Status Patrimonial</th>
        <th>Ação / Instrução SEI</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</div>
</body>
</html>"""

    p1 = os.path.join("documentos_patrimoniais", cfg["filename"])
    p2 = os.path.join("documentos_patrimoniais", cfg["sei_filename"])
    with open(p1, "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(p2, "w", encoding="utf-8") as f:
        f.write(html_content.replace('href="../index.html"', 'href="../../index.html"'))
    print(f"Gerado: {p1} ({len(items)} itens | {total_fmt})")

print("Todos os dossiês de lote e processos de compra SEI foram atualizados com preços individuais!")
