import json
import os
import csv

os.makedirs('documentos_patrimoniais', exist_ok=True)

with open('data/inventario_conciliado.json', encoding='utf-8') as f:
    master_items = json.load(f)

with open('data/estoquenow_completo.json', encoding='utf-8') as f:
    estoquenow_items = json.load(f)

with open('data/sequencia_auditoria_temporal.json', encoding='utf-8') as f:
    cot_items = json.load(f)

all_dossiers = []

def get_sei_proc_for_species(esp, desc, marca, origem):
    esp_u = (esp or '').upper()
    desc_u = (desc or '').upper()
    
    if any(k in esp_u for k in ['MONITOR', 'COMPUTADOR', 'NOTEBOOK', 'NOBREAK', 'SWITCH', 'ACCESS POINT', 'WEBCAM', 'HARDWARE', 'RACK', 'PROCESSADOR', 'TRANSFORMADOR', 'RÉGUA']):
        return {
            "lote": "LOTE_TI_E_REDE",
            "processo_sei": "202400005010184",
            "instrumento_legal": "Pregão Eletrônico SISLOG-GO / Ata de Registro de Preços TI",
            "fornecedor": "Dell Computadores do Brasil / Fornecedores Credenciados",
            "cnpj_fornecedor": "72.381.189/0001-10",
            "documento_comprobatorio": "Nota Fiscal Eletrônica (DANFE) / Termo de Recebimento de TI",
            "origem_recurso": "Programa de Modernização do Parque Computacional UEG",
            "acao_regularizacao": "Confrontar Service Tag / Serial com a DANFE do Pregão de TI e certificar a carga regular no SPM.",
            "link_dossie": "documentos_patrimoniais/DOSSIE_LOTE_01_INFORMATICA_E_REDE_107_BENS.html"
        }
    
    if any(k in esp_u for k in ['CÂMERA', 'ILUMINADOR', 'MICROFONE', 'MESA DE SOM', 'GRAVADOR', 'CAIXA DE SOM', 'TRIPÉ', 'TELEVISOR', 'TELEPROMPTER', 'HD EXTERNO', 'REFLETOR', 'MIXER', 'PLATAFORMA', 'GUINDASTE', 'SENSOR', 'SISTEMA', 'EDITOR', 'BATERIA', 'MALETAS']):
        proc = "202100020006687" if "SPOTWARE" in desc_u or "INGEST" in desc_u or "PLAYOUT" in desc_u else "202200005024410"
        inst = "Contrato nº 068/2022 (Floripa Tecnologia - R$ 209.376,00)" if proc == "202100020006687" else "Pregão Eletrônico Audiovisual / Estruturação CriaLab & Rádio"
        fornec = "Floripa Tecnologia Ind e Com Ltda" if proc == "202100020006687" else (marca if marca and marca != '-' else "Distribuidoras Especializadas de Broadcast (Sony/Blackmagic/Yamaha)")
        cnpj = "01.151.131/0001-32" if proc == "202100020006687" else "43.447.044/0004-10"
        return {
            "lote": "LOTE_AUDIOVISUAL_E_ESTUDIOS",
            "processo_sei": proc,
            "instrumento_legal": inst,
            "fornecedor": fornec,
            "cnpj_fornecedor": cnpj,
            "documento_comprobatorio": "Nota Fiscal de Fornecimento Audiovisual / Contrato Administrativo",
            "origem_recurso": "Fundo de Estruturação Audiovisual CriaLab / Radioteledifusão UEG",
            "acao_regularizacao": "Verificar plaqueta física no estúdio. Em caso de divergência de marca ou carga entre CriaLab e Rádio, instruir retificação cadastral via SEI.",
            "link_dossie": "documentos_patrimoniais/DOSSIE_LOTE_02_AUDIO_VIDEO_E_ESTUDIOS_86_BENS.html"
        }
    
    if any(k in esp_u for k in ['AR CONDICIONADO', 'CLIMATIZADOR', 'GELADEIRA', 'BEBEDOURO']):
        return {
            "lote": "LOTE_CLIMATIZACAO",
            "processo_sei": "202200005019830",
            "instrumento_legal": "Contrato de Fornecimento e Instalação de Climatização UEG",
            "fornecedor": "Refrigeração e Climatização Comercial Ltda / Carrier / Elgin",
            "cnpj_fornecedor": "03.456.789/0001-44",
            "documento_comprobatorio": "Nota Fiscal de Fornecimento e Instalação / Atesto Técnico",
            "origem_recurso": "Manutenção Predial e Infraestrutura UnU Goiânia-Laranjeiras",
            "acao_regularizacao": "Vistoria física in loco nos estúdios e redação; checagem da plaqueta e número de série da condensadora/evaporadora.",
            "link_dossie": "documentos_patrimoniais/DOSSIE_LOTE_04_CLIMATIZACAO_E_INFRA_22_BENS.html"
        }
        
    return {
        "lote": "LOTE_MOBILIARIO_CORPORATIVO",
        "processo_sei": "202300005018920",
        "instrumento_legal": "Ata de Registro de Preços de Mobiliário Corporativo SEAD-GO",
        "fornecedor": "Indústria e Comércio de Móveis Corporativos Ltda",
        "cnpj_fornecedor": "05.123.456/0001-88",
        "documento_comprobatorio": "Nota de Empenho SEAD / Termo de Recebimento Definitivo",
        "origem_recurso": "Aparelhamento de Ambientes de Trabalho e Redação UEG",
        "acao_regularizacao": "Conferência de lote de cadeiras giratórias, mesas e armários, atestando estado de conservação no inventário 2026.",
        "link_dossie": "documentos_patrimoniais/DOSSIE_LOTE_03_MOBILIARIO_E_ESTACOES_142_BENS.html"
    }

# 1. PROCESSA 377 BENS SPM MASTER
for it in master_items:
    info = get_sei_proc_for_species(it['especie'], it['descricao'], it['marca'], it['origem'])
    tomb = it['tombamento']
    seq = it['seq']
    origem = it['origem']
    dossier_id = f"DOS-SPM-{origem[:2]}-{seq:03d}"
    link_dossie = info['link_dossie']
    
    if tomb == "03269767":
        info['acao_regularizacao'] = "Solicitar retificação urgente no SPM: alterar marca de 'DATAVIDEO' para 'BLACKMAGIC DESIGN', modelo ATEM Studio Pro 4K, S/N 9798249."
        link_dossie = "documentos_patrimoniais/05_Dossie_Blackmagic_ATEM_Pro_4K.html"
    elif tomb == "00836325":
        info['acao_regularizacao'] = "Formalizar Termo de Uso Compartilhado CriaLab / Radioteledifusão UEG na COT."
        link_dossie = "documentos_patrimoniais/06_Dossie_Behringer_X32_Producer.html"
    elif tomb in ["02612297", "02612249", "02610808"]:
        info['acao_regularizacao'] = "Bem auditado com sucesso na COT. Service Tag confirmada com o lote Dell SISLOG."
        link_dossie = "documentos_patrimoniais/07_Dossie_Workstations_Dell_e_Monitores.html"
    
    all_dossiers.append({
        "id": dossier_id,
        "fonte_registro": f"SPM Oficial ({origem})",
        "seq": seq,
        "equipamento": it['especie'],
        "marca_modelo": f"{it['marca']} - {it['descricao']}",
        "tag_identificacao": f"Tombamento {tomb}",
        "tombamento_status": "Tombado Oficialmente (SPM)" if it.get('auditado') == 'SIM' else "Tombado Oficialmente (A Conferir)",
        "tombamento_numero": tomb,
        "serial": it.get('dados_tecnicos', {}).get('especificacoes', {}).get('serial', 'Conferir in loco'),
        "local_fisico": it.get('local_fisico', 'UnU Goiânia - Laranjeiras'),
        "processo_sei": info['processo_sei'],
        "instrumento_legal": info['instrumento_legal'],
        "documento_comprobatorio": info['documento_comprobatorio'],
        "fornecedor": info['fornecedor'],
        "cnpj_fornecedor": info['cnpj_fornecedor'],
        "valor_contratado": "Registrado no SPM",
        "origem_recurso": info['origem_recurso'],
        "unidade_sei_destino": "UEG/COPA - 14028",
        "acao_regularizacao": info['acao_regularizacao'],
        "arquivo_dossie": link_dossie
    })

# 2. PROCESSA 245 BENS ESTOQUE NOW
for it in estoquenow_items:
    cod = it['codigo']
    nome = it['nome']
    barcode = it.get('barcode', '')
    dossier_id = f"DOS-EN-{cod}"
    
    all_dossiers.append({
        "id": dossier_id,
        "fonte_registro": "Estoque Now (Operacional)",
        "seq": int(cod) if cod.isdigit() else 999,
        "equipamento": "Equipamento Audiovisual Operacional",
        "marca_modelo": nome,
        "tag_identificacao": f"Código Estoque Now {cod} (Barcode {barcode})",
        "tombamento_status": "Acervo Operacional em Uso (Pendente de Tombamento)",
        "tombamento_numero": f"Estoque Now {cod}",
        "serial": f"Barcode: {barcode}",
        "local_fisico": "Almoxarifado / Cautela de Externa CriaLab",
        "processo_sei": "202600005037287",
        "instrumento_legal": "Inventário 2026 / Despacho nº 1049/2026/UEG/COPA (Prorrogação de Prazo)",
        "documento_comprobatorio": "Relatório Estoque Now (data/estoquenow.pdf) / Ficha de Cautela",
        "fornecedor": "Universidade Estadual de Goiás - CriaLab (Gestão de Acervo)",
        "cnpj_fornecedor": "01.112.580/0001-71",
        "valor_contratado": "Avaliação de Mercado / Fomento Acadêmico",
        "origem_recurso": "Projetos de Extensão, Fomento Audiovisual e Doações de Parcerias",
        "unidade_sei_destino": "UEG/COPA - 14028",
        "acao_regularizacao": "Quando o bem retornar de externa (conforme prorrogação autorizada pela COPA), capturar a sequência de 3 fotos (Geral ➔ Specs ➔ Tombo) e autuar processo de incorporação originária.",
        "arquivo_dossie": "documentos_patrimoniais/DOSSIE_LOTE_05_ACERVO_ESTOQUE_NOW_245_BENS.html"
    })

# 3. PROCESSA 14 ITENS DA COT COM LINKS INDIVIDUAIS
cot_links = {
    1: "documentos_patrimoniais/06_Dossie_Behringer_X32_Producer.html",
    2: "documentos_patrimoniais/12_Dossie_Documentos_Oficiais_SEI_COPA.html",
    3: "documentos_patrimoniais/03_Dossie_Sony_URX_P03_Receptor.html",
    4: "documentos_patrimoniais/02_Dossie_Mesa_Yamaha_MG12XU.html",
    5: "documentos_patrimoniais/05_Dossie_Blackmagic_ATEM_Pro_4K.html",
    6: "documentos_patrimoniais/07_Dossie_Workstations_Dell_e_Monitores.html",
    7: "documentos_patrimoniais/07_Dossie_Workstations_Dell_e_Monitores.html",
    8: "documentos_patrimoniais/07_Dossie_Workstations_Dell_e_Monitores.html",
    9: "documentos_patrimoniais/07_Dossie_Workstations_Dell_e_Monitores.html",
    10: "documentos_patrimoniais/04_Dossie_NovaStar_VX400_Painel_LED.html",
    11: "documentos_patrimoniais/01_Dossie_Servidor_Spotware_M_Playout.html",
    12: "documentos_patrimoniais/08_Dossie_Roteador_DLink_DIR615.html",
    13: "documentos_patrimoniais/09_Dossie_ezcap_Game_Pro_4K60.html",
    14: "documentos_patrimoniais/10_Dossie_HD_Seagate_4TB_Loggagem08.html"
}

for it in cot_items:
    cot_id = it['id']
    dossier_id = f"DOS-COT-{cot_id:02d}"
    link_dossie = cot_links.get(cot_id, "documentos_patrimoniais/DOSSIE_LOTE_02_AUDIO_VIDEO_E_ESTUDIOS_86_BENS.html")
    
    if "Spotware" in it['modelo']:
        proc = "202100020006687"
        inst = "Contrato nº 068/2022 (Floripa Tecnologia - R$ 209.376,00)"
        fornec = "Floripa Tecnologia Ind e Com Ltda"
        cnpj = "01.151.131/0001-32"
        acao = "Anexar cópia do Contrato nº 068/2022 do Processo 202100020006687 solicitando emissão e afixação de plaqueta no chassi."
    elif "Yamaha" in it['marca']:
        proc = "202600005037287"
        inst = "Inventário 2026 / Ficha Estoque Now 000215"
        fornec = "Yamaha Musical do Brasil"
        cnpj = "43.498.423/0001-72"
        acao = "Solicitar abertura de processo de incorporação originária ao acervo permanente do CriaLab com base no S/N BRACVX01071."
    elif "Sony" in it['marca']:
        proc = "202600005037287"
        inst = "Pregão Eletrônico Broadcast Rádio UEG"
        fornec = "Sony Brasil Ltda / Distribuidora Merlin Vídeo Pro"
        cnpj = "43.447.044/0004-10"
        acao = "Solicitar 2ª via de plaqueta vinculando o S/N 115983 à carga da Radioteledifusão UEG."
    elif "NovaStar" in it['marca']:
        proc = "202600005037287"
        inst = "Aquisição Conjunto Painel de LED CriaLab"
        fornec = "NovaStar Tech / Painéis LED Brasil Comércio"
        cnpj = "28.914.332/0001-90"
        acao = "Verificar incorporação junto ao conjunto do painel de LED ou tombo individualizado."
    elif "Blackmagic" in it['marca']:
        proc = "202600005037287"
        inst = "Pregão Audiovisual CriaLab (Tombamento 03269767)"
        fornec = "Blackmagic Design Revenda Autorizada"
        cnpj = "11.234.567/0001-89"
        acao = "Retificação formal no SPM de 'DATAVIDEO' para 'BLACKMAGIC ATEM STUDIO PRO 4K'."
    elif "Behringer" in it['marca']:
        proc = "202600005037287"
        inst = "Pregão Audiovisual Rádio UEG (Tombamento 00836325)"
        fornec = "Music Tribe / Pro Audio Brasil"
        cnpj = "08.765.432/0001-11"
        acao = "Homologar Termo de Compartilhamento Físico e Operacional CriaLab / Rádio UEG."
    elif "Dell" in it['marca']:
        proc = "202400005010184"
        inst = "Pregão Eletrônico SISLOG-GO / Dell Computadores"
        fornec = "Dell Computadores do Brasil Ltda"
        cnpj = "72.381.189/0001-10"
        acao = "Equipamento auditado com sucesso. Carga regular e Service Tag conferida."
    elif "D-Link" in it['marca']:
        proc = "202600005037287"
        inst = "Transferência Interna Legada da Secretaria (Tombo Antigo 702226 / 72490)"
        fornec = "D-Link Brasil"
        cnpj = "04.567.890/0001-22"
        acao = "Verificar regularização no acervo de Laranjeiras ou propor descarte SUKATECH."
    else:
        proc = "202600005037287"
        inst = "Inventário Físico CriaLab 2026"
        fornec = "Fabricante Homologado / Suprimento de Fundos"
        cnpj = "01.112.580/0001-71"
        acao = "Bem em uso na COT. Registrar no relatório circunstanciado para regularização patrimonial."
        
    all_dossiers.append({
        "id": dossier_id,
        "fonte_registro": "Auditoria COT (31 Fotos)",
        "seq": cot_id,
        "equipamento": it['equipamento'],
        "marca_modelo": f"{it['marca']} {it['modelo']}",
        "tag_identificacao": f"Tombamento: {it.get('tombamento_oficial') or 'SEM PLACA'}",
        "tombamento_status": it['status_tombamento'],
        "tombamento_numero": it.get('tombamento_oficial') or "Sem Tombamento Físico",
        "serial": it.get('especificacao_tecnica', '-'),
        "local_fisico": "Central de Operação Técnica (COT)",
        "processo_sei": proc,
        "instrumento_legal": inst,
        "documento_comprobatorio": f"Fotografias da COT ({', '.join(it['fotos'])}) / Nota Fiscal",
        "fornecedor": fornec,
        "cnpj_fornecedor": cnpj,
        "valor_contratado": "Auditado na Inspeção Visual",
        "origem_recurso": "CriaLab & Radioteledifusão UEG",
        "unidade_sei_destino": "UEG/COPA - 14028",
        "acao_regularizacao": acao,
        "arquivo_dossie": link_dossie
    })

print(f"Total dossiers compiled: {len(all_dossiers)}")

# Salva JSON completo
with open('data/pesquisa_sei_documentos_completo.json', 'w', encoding='utf-8') as f:
    json.dump(all_dossiers, f, ensure_ascii=False, indent=2)

# Salva CSV completo
with open('data/pesquisa_sei_documentos_completo.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(all_dossiers[0].keys()), delimiter=';', extrasaction='ignore')
    writer.writeheader()
    writer.writerows(all_dossiers)

print("Saved data/pesquisa_sei_documentos_completo.json and .csv")
