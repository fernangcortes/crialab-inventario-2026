import json
import csv
import os
import glob

def run_reconciliation():
    master_path = os.path.join('data', 'inventario_master.json')
    if not os.path.exists(master_path):
        print("inventario_master.json not found!")
        return

    with open(master_path, encoding='utf-8') as f:
        master_items = json.load(f)

    # Index master items by tombamento and tombamento_anterior
    by_tomb = {}
    by_tomb_ant = {}
    for it in master_items:
        t = str(it.get('tombamento', '')).strip().lstrip('0')
        if t:
            by_tomb[t] = it
        ta = str(it.get('tombamento_anterior', '')).strip().lstrip('0')
        if ta:
            by_tomb_ant[ta] = it

    # Read all auditoria_lote*.json
    auditoria_files = sorted(glob.glob(os.path.join('data', 'auditoria_lote*.json')))
    print(f"Found {len(auditoria_files)} auditoria files: {auditoria_files}")

    audited_photos = []
    audited_bens = []
    for af in auditoria_files:
        try:
            with open(af, encoding='utf-8') as f:
                data = json.load(f)
                fotos = data.get('fotos', [])
                audited_photos.extend(fotos)
        except Exception as e:
            print(f"Error reading {af}: {e}")

    # Process audited items and match with master
    matched_tombamentos = set()
    audit_findings = []

    for f in audited_photos:
        placa = f.get('placa_tombamento', {})
        tomb_num = str(placa.get('numero', '')).strip().lstrip('0') if placa else ''
        sn = str(f.get('numero_serie_fabricante', '') or '').strip()
        marca = f.get('marca', '')
        modelo = f.get('modelo', '')
        equip = f.get('tipo_equipamento', '')
        estado = f.get('estado_fisico', 'Normal')
        arquivo = f.get('arquivo', '')
        obs = f.get('observacoes', '')

        matched_item = None
        match_type = 'None'

        if tomb_num:
            if tomb_num in by_tomb:
                matched_item = by_tomb[tomb_num]
                match_type = 'Tombamento Atual'
                matched_tombamentos.add(tomb_num)
            elif tomb_num in by_tomb_ant:
                matched_item = by_tomb_ant[tomb_num]
                match_type = 'Tombamento Anterior'
                matched_tombamentos.add(str(matched_item.get('tombamento')).lstrip('0'))

        # Fallback match by Serial Number or specific description in master
        if not matched_item and sn:
            for it in master_items:
                desc = it.get('descricao', '').upper()
                if sn.upper() in desc:
                    matched_item = it
                    match_type = 'Número de Série'
                    matched_tombamentos.add(str(it.get('tombamento')).lstrip('0'))
                    break

        audit_findings.append({
            'foto': os.path.basename(arquivo),
            'caminho_foto': arquivo,
            'equipamento_identificado': equip,
            'marca_identificada': marca,
            'modelo_identificado': modelo,
            'tombamento_placa': tomb_num,
            'serial_number': sn,
            'estado_fisico': estado,
            'match_type': match_type,
            'matched_tombamento': matched_item.get('tombamento') if matched_item else None,
            'matched_origem': matched_item.get('origem') if matched_item else None,
            'matched_especie': matched_item.get('especie') if matched_item else None,
            'matched_descricao': matched_item.get('descricao') if matched_item else None,
            'observacoes': obs
        })

    # Update master items with audit status
    consolidado = []
    for it in master_items:
        t = str(it.get('tombamento', '')).strip().lstrip('0')
        is_audited = t in matched_tombamentos
        
        # Check if photos matched this item
        related_photos = [af for af in audit_findings if str(af.get('matched_tombamento', '')).lstrip('0') == t]
        
        estado = 'Pendente'
        avarias = []
        fotos_str = []
        local_fisico = 'Pendente'
        precisa_etiqueta = False

        if is_audited and related_photos:
            estado = 'Auditado / Localizado'
            local_fisico = 'Central de Operação Técnica (COT)'
            for rp in related_photos:
                fotos_str.append(rp['foto'])
                if rp['estado_fisico'] in ['Imperfeição', 'Defeito']:
                    avarias.append(f"{rp['estado_fisico']}: {rp['observacoes']}")
                if not rp['tombamento_placa']:
                    precisa_etiqueta = True

        it_copy = dict(it)
        it_copy['status_auditoria'] = estado
        it_copy['local_fisico_encontrado'] = local_fisico
        it_copy['fotos_evidencia'] = ', '.join(set(fotos_str))
        it_copy['avarias_observacoes'] = '; '.join(avarias)
        it_copy['precisa_nova_etiqueta'] = 'SIM' if precisa_etiqueta else 'NÃO'
        it_copy['divergencia_localizacao'] = 'SIM' if is_audited and it['origem'] == 'RADIOTELEDIFUSÃO' else 'NÃO'
        consolidado.append(it_copy)

    # Save consolidado
    with open(os.path.join('data', 'inventario_conciliado.json'), 'w', encoding='utf-8') as f:
        json.dump(consolidado, f, ensure_ascii=False, indent=2)

    with open(os.path.join('data', 'inventario_conciliado.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['origem', 'seq', 'especie', 'tombamento', 'tombamento_anterior', 'descricao', 'marca', 'status_auditoria', 'local_fisico_encontrado', 'precisa_nova_etiqueta', 'divergencia_localizacao', 'avarias_observacoes', 'fotos_evidencia']
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(consolidado)

    with open(os.path.join('data', 'audit_findings.json'), 'w', encoding='utf-8') as f:
        json.dump(audit_findings, f, ensure_ascii=False, indent=2)

    total_master = len(master_items)
    total_audited = len(matched_tombamentos)
    print(f"Reconciliation finished. Master items: {total_master}. Audited with photos: {total_audited}")

if __name__ == '__main__':
    run_reconciliation()
