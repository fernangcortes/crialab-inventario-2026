import pypdfium2 as pdfium
import re
import json

doc = pdfium.PdfDocument(r'data\estoquenow.pdf')
full_text = ''
for i in range(len(doc)):
    full_text += f'\n=== PAGE {i+1} ===\n' + doc[i].get_textpage().get_text_range()

# Split into lines and parse
lines = full_text.splitlines()

items = []
current_item = None

# Pattern to start an item: 6 digits (code) + 13 digits (barcode) + 13 digits (qrcode)
start_pattern = re.compile(r'^(\d{6})\s+(\d{12,14})\s+(\d{12,14})\s*(.*)')

for line in lines:
    l_str = line.strip()
    if not l_str or 'Universidade Estadual de Goias' in l_str or 'relatório emitido pelo sistema' in l_str or 'RELATÓRIO DE ITENS' in l_str or 'CÓDIGO CÓDIGO DE BARRAS' in l_str or '=== PAGE' in l_str:
        continue
        
    m = start_pattern.match(l_str)
    if m:
        if current_item:
            items.append(current_item)
        current_item = {
            'codigo': m.group(1),
            'barcode': m.group(2),
            'qrcode': m.group(3),
            'linhas': [m.group(4)] if m.group(4) else []
        }
    elif current_item:
        current_item['linhas'].append(l_str)

if current_item:
    items.append(current_item)

# Post process each item
parsed_catalog = []
for it in items:
    text_block = ' '.join(it['linhas'])
    # Extract name up to numbers/currency
    # Usually: Name [Observações] [Categoria] Qtd Preço ...
    # Let's extract first 100 chars as clean name
    nome = text_block.split('Produto')[0].split('Acessórios')[0].split('Cabos')[0].strip()
    # clean extra numbers at end
    nome_clean = re.sub(r'\s+\d+[,.]\d{2}.*$', '', nome).strip()
    
    # Check if mentions manutenção
    em_manutencao = 'Sim' if 'manutenção' in text_block.lower() or 'sem monitor' in text_block.lower() else 'Não'

    parsed_catalog.append({
        'codigo': it['codigo'],
        'barcode': it['barcode'],
        'qrcode': it['qrcode'],
        'nome': nome_clean[:120] if nome_clean else text_block[:80],
        'texto_completo': text_block,
        'em_manutencao': em_manutencao
    })

print(f'Extracted {len(parsed_catalog)} items from Estoque Now PDF!')
with open('data/estoquenow_completo.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_catalog, f, ensure_ascii=False, indent=2)

print('Sample 8 items:')
for c in parsed_catalog[:8]:
    print(f"[{c['codigo']}] {c['nome']}")
