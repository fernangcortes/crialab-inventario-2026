import pypdfium2 as pdfium
import re
import json

doc = pdfium.PdfDocument(r'data\estoquenow.pdf')
full_text = ''
for i in range(len(doc)):
    full_text += f'\n=== PAGE {i+1} ===\n' + doc[i].get_textpage().get_text_range()

print(f'Estoque Now total length: {len(full_text)}')

lines = full_text.splitlines()
items = []
for line in lines:
    line_clean = line.strip()
    # Match pattern: 000116 1859767205932 1859767205932 Name ...
    m = re.match(r'^(\d{6})\s+(\d{12,14})\s+(\d{12,14})\s+(.+)', line_clean)
    if m:
        codigo = m.group(1)
        barcode = m.group(2)
        rest = m.group(4)
        items.append({
            'codigo': codigo,
            'barcode': barcode,
            'raw_desc': rest
        })

print(f'Matched {len(items)} items from Estoque Now PDF!')
if items:
    for it in items[:10]:
        print(' -', it['codigo'], it['raw_desc'][:80])

with open('data/estoquenow_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

# Cross reference with master inventory
with open('data/inventario_master.json', encoding='utf-8') as f:
    master = json.load(f)

matched_with_master = []
for it in items:
    desc_now = it['raw_desc'].upper()
    for m in master:
        desc_m = m['descricao'].upper()
        # check keywords like Datavideo PTC-140, Torpedo LED, Rebel T3i, etc.
        words = [w for w in desc_now.split() if len(w) > 3 and not w.isdigit()]
        common = [w for w in words if w in desc_m]
        if len(common) >= 3:
            matched_with_master.append({
                'estoquenow_cod': it['codigo'],
                'estoquenow_desc': it['raw_desc'],
                'tombamento': m['tombamento'],
                'origem': m['origem'],
                'master_desc': m['descricao']
            })
            break

print(f'Cross-matched {len(matched_with_master)} items between Estoque Now and Master Inventory!')
with open('data/estoquenow_matched.json', 'w', encoding='utf-8') as f:
    json.dump(matched_with_master, f, ensure_ascii=False, indent=2)
