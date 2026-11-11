import json
import os

with open('data/inventario_conciliado.json', encoding='utf-8') as f:
    items = json.load(f)

def generate_html_ficha(location_filter, filename, title_location):
    sub_items = [it for it in items if it['origem'] == location_filter]
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Ficha de Apuração de Inventário 2026 - {title_location}</title>
<style>
  @page {{
    size: A4 landscape;
    margin: 10mm 10mm 15mm 10mm;
  }}
  body {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 8.5px;
    color: #111;
    margin: 0;
    padding: 10px;
  }}
  .header {{
    text-align: center;
    border-bottom: 2px solid #222;
    padding-bottom: 4px;
    margin-bottom: 6px;
  }}
  .header h1 {{
    font-size: 13px;
    margin: 2px 0;
    text-transform: uppercase;
    font-weight: bold;
  }}
  .header h2 {{
    font-size: 10.5px;
    margin: 2px 0;
    font-weight: normal;
  }}
  .meta-box {{
    display: flex;
    justify-content: space-between;
    margin-top: 4px;
    font-size: 9px;
    background: #f4f4f4;
    padding: 5px 10px;
    border: 1px solid #ddd;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 6px;
  }}
  th, td {{
    border: 1px solid #777;
    padding: 3px 4px;
    vertical-align: middle;
  }}
  th {{
    background: #e9ecef;
    font-weight: bold;
    font-size: 8px;
    text-align: center;
  }}
  .col-seq {{ width: 25px; text-align: center; font-weight: bold; }}
  .col-esp {{ width: 95px; }}
  .col-tomb {{ width: 65px; text-align: center; font-weight: bold; }}
  .col-ant {{ width: 55px; text-align: center; }}
  .col-desc {{ width: auto; }}
  .col-marca {{ width: 65px; text-align: center; }}
  .col-box {{ width: 34px; text-align: center; font-size: 10px; font-weight: bold; }}
  .col-vida {{ width: 45px; text-align: center; }}
  tr.audited {{
    background-color: #e8f5e9;
  }}
  tr.anomalia {{
    background-color: #fff3e0;
  }}
  .box-checked {{
    display: inline-block;
    width: 13px;
    height: 13px;
    border: 1.5px solid #111;
    background: #2e7d32;
    color: #fff;
    line-height: 12px;
    text-align: center;
    font-size: 10px;
    font-weight: bold;
    border-radius: 2px;
  }}
  .box-empty {{
    display: inline-block;
    width: 13px;
    height: 13px;
    border: 1px solid #888;
    background: #fff;
    border-radius: 2px;
  }}
  .footer {{
    margin-top: 15px;
    border-top: 1px solid #333;
    padding-top: 8px;
    page-break-inside: avoid;
  }}
  .sig-block {{
    width: 30%;
    text-align: center;
    border-top: 1px dashed #444;
    margin-top: 35px;
    padding-top: 4px;
  }}
  .print-btn {{
    position: fixed;
    top: 10px;
    right: 10px;
    background: #0288d1;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    font-weight: bold;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    z-index: 9999;
  }}
  @media print {{
    .print-btn {{ display: none; }}
  }}
</style>
</head>
<body>
<button class="print-btn" onclick="window.print()">🖨️ Imprimir / Salvar PDF</button>

<div class="header">
  <h2>Secretaria de Estado da Administração - Governo de Goiás</h2>
  <h1>Sistema de Patrimônio Mobiliário (SPM)</h1>
  <h2>FICHA DE APURAÇÃO DE INVENTÁRIO - EXERCÍCIO 2026</h2>
  <div class="meta-box">
    <div><strong>ÓRGÃO:</strong> UNIVERSIDADE ESTADUAL DE GOIÁS - UEG</div>
    <div><strong>UNIDADE ADM:</strong> 10807 - UNIDADE UNIVERSITÁRIA DE GOIÂNIA - LARANJEIRAS</div>
    <div><strong>LOCALIZAÇÃO:</strong> {title_location}</div>
    <div><strong>TOTAL DE BENS:</strong> {len(sub_items)}</div>
  </div>
</div>

<table>
  <thead>
    <tr>
      <th class="col-seq">SEQ</th>
      <th class="col-esp">ESPÉCIE</th>
      <th class="col-tomb">Nº TOMBAMENTO</th>
      <th class="col-ant">TOMB. ANTERIOR</th>
      <th class="col-desc">DESCRIÇÃO DO BEM</th>
      <th class="col-marca">MARCA</th>
      <th class="col-box">NÃO LOC.</th>
      <th class="col-box">NOVA ETIQ.</th>
      <th class="col-box">IMPERF.</th>
      <th class="col-box">DEFEITO</th>
      <th class="col-box">AUDITADO</th>
      <th class="col-vida">VIDA ÚTIL (ANOS)</th>
    </tr>
  </thead>
  <tbody>"""

    for it in sub_items:
        is_aud = it.get('auditado') == 'SIM'
        is_nova = it.get('necessita_nova_etiqueta') == 'SIM'
        is_imp = it.get('estado_fisico') == 'Imperfeição'
        is_def = it.get('estado_fisico') == 'Defeito'
        
        row_class = 'audited' if is_aud else ''
        if is_imp or is_def or is_nova:
            row_class = 'anomalia'
            
        chk_aud = '<span class="box-checked">✓</span>' if is_aud else '<span class="box-empty"></span>'
        chk_nova = '<span class="box-checked" style="background:#e65100">✓</span>' if is_nova else '<span class="box-empty"></span>'
        chk_imp = '<span class="box-checked" style="background:#d84315">✓</span>' if is_imp else '<span class="box-empty"></span>'
        chk_def = '<span class="box-checked" style="background:#c62828">✓</span>' if is_def else '<span class="box-empty"></span>'
        chk_nao = '<span class="box-empty"></span>'

        obs_html = f"<br><small style='color:#0d47a1'><strong>[Auditado COT]:</strong> {it['observacao_auditoria']} (Fotos: {it.get('fotos_evidencia')})</small>" if is_aud else ""

        html += f"""
    <tr class="{row_class}">
      <td class="col-seq">{it['seq']}</td>
      <td class="col-esp">{it['especie']}</td>
      <td class="col-tomb">{it['tombamento']}</td>
      <td class="col-ant">{it.get('tombamento_anterior', '')}</td>
      <td class="col-desc">
        {it['descricao']}
        {obs_html}
      </td>
      <td class="col-marca">{it['marca']}</td>
      <td class="col-box">{chk_nao}</td>
      <td class="col-box">{chk_nova}</td>
      <td class="col-box">{chk_imp}</td>
      <td class="col-box">{chk_def}</td>
      <td class="col-box">{chk_aud}</td>
      <td class="col-vida"></td>
    </tr>"""

    html += f"""
  </tbody>
</table>

<div class="footer">
  <div>
    <p>Atesto para os devidos fins que as informações aqui prestadas são fidedignas e me responsabilizo pela veracidade das mesmas.</p>
    <div style="display:flex; justify-content:space-around; margin-top:20px;">
      <div class="sig-block">
        <strong>FERNANDO GOMES CORTES</strong><br>
        Comissão Setorial de Inventário (Portaria 1210/2026)<br>
        CPF: ___________________
      </div>
      <div class="sig-block">
        <strong>THAYS SILVIA REIS</strong><br>
        Acompanhamento Operacional do Inventário<br>
        CPF: ___________________
      </div>
      <div class="sig-block">
        <strong>PROF. JOSÉ EDUARDO RIBEIRO MACEDO</strong><br>
        Coordenador da UnU de Goiânia-Laranjeiras<br>
        Data: ___/11/2026
      </div>
    </div>
  </div>
</div>

</body>
</html>"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Generated {filename} ({len(sub_items)} items)')

os.makedirs('fichas', exist_ok=True)
generate_html_ficha('CRIA LAB', 'fichas/Ficha_Apuracao_CriaLab_Preenchida.html', 'CRIA LAB')
generate_html_ficha('RADIOTELEDIFUSÃO', 'fichas/Ficha_Apuracao_Radioteledifusao_Preenchida.html', 'RADIOTELEDIFUSÃO UEG')
