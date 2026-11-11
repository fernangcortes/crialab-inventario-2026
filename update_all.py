import json
import csv
import os

# 1. Load sequence
with open('data/sequencia_auditoria_temporal.json', encoding='utf-8') as f:
    sequence = json.load(f)

# 2. Load master
with open('data/inventario_master.json', encoding='utf-8') as f:
    master = json.load(f)

# Map items that are officially tombados
tombados_map = {}
for it in sequence:
    t = it.get('tombamento_oficial')
    if t:
        clean_t = str(t).lstrip('0')
        tombados_map[clean_t] = it

# Reconcile master items
consolidado = []
for m in master:
    c = dict(m)
    t = str(m.get('tombamento', '')).strip().lstrip('0')
    
    if t in tombados_map:
        seq_it = tombados_map[t]
        c['auditado'] = 'SIM'
        c['localizado'] = 'SIM'
        c['local_fisico'] = 'Central de Operação Técnica (COT)'
        c['estado_fisico'] = seq_it['estado_fisico']
        c['necessita_nova_etiqueta'] = 'NÃO'
        c['fotos_evidencia'] = ', '.join(seq_it['fotos'])
        c['observacao_auditoria'] = f"{seq_it['equipamento']} {seq_it['marca']} {seq_it['modelo']} auditado na COT. Sequência de fotos: {', '.join(seq_it['ordem_fotos'])}."
        c['divergencia_carga'] = 'SIM (Carga da Radioteledifusão localizada fisicamente na COT do CriaLab)' if m['origem'] == 'RADIOTELEDIFUSÃO' else 'NÃO'
    else:
        c['auditado'] = 'NÃO'
        c['localizado'] = 'PENDENTE'
        c['local_fisico'] = 'Pendente de varredura nos demais cômodos'
        c['estado_fisico'] = 'A conferir'
        c['necessita_nova_etiqueta'] = 'A conferir'
        c['observacao_auditoria'] = 'Pendente de conferência física nas próximas áreas ou verificação no Estoque Now.'
        c['fotos_evidencia'] = ''
        c['divergencia_carga'] = 'NÃO'
        
    consolidado.append(c)

with open('data/inventario_conciliado.json', 'w', encoding='utf-8') as f:
    json.dump(consolidado, f, ensure_ascii=False, indent=2)

with open('data/inventario_conciliado.csv', 'w', newline='', encoding='utf-8-sig') as f:
    fieldnames = ['origem', 'seq', 'especie', 'tombamento', 'tombamento_anterior', 'descricao', 'marca', 'auditado', 'localizado', 'local_fisico', 'estado_fisico', 'necessita_nova_etiqueta', 'divergencia_carga', 'observacao_auditoria', 'fotos_evidencia']
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(consolidado)

# 3. Extract all uncataloged/untagged items from the sequence
untagged = [it for it in sequence if not it.get('tombamento_oficial')]
with open('data/bens_nao_cadastrados_cot.json', 'w', encoding='utf-8') as f:
    json.dump(untagged, f, ensure_ascii=False, indent=2)

print(f'Consolidado updated with {len(tombados_map)} tombados e {len(untagged)} não tombados!')
