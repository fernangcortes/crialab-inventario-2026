import json

items_sequence = [
    {
        'id': 1,
        'equipamento': 'Mesa de Som Digital / Console',
        'marca': 'Behringer',
        'modelo': 'X32 Producer',
        'fotos': ['IMG_20261111_103510.jpg', 'IMG_20261111_103516.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento', '2. Placa de tombamento UEG'],
        'tombamento_oficial': '00836325',
        'status_tombamento': 'TOMBADO (Placa oficial 00836325 na lateral)',
        'especificacao_tecnica': 'Mesa digital 17 faders motorizados',
        'estado_fisico': 'Normal'
    },
    {
        'id': 2,
        'equipamento': 'Microfone Dinâmico Vocal',
        'marca': 'Shure',
        'modelo': 'SM58',
        'fotos': ['IMG_20261111_103541.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento'],
        'tombamento_oficial': None,
        'status_tombamento': 'NÃO TOMBADO (Sem placa física no corpo)',
        'especificacao_tecnica': 'Shure SM58 dinâmico cardióide',
        'estado_fisico': 'Imperfeição (globo metálico amassado)'
    },
    {
        'id': 3,
        'equipamento': 'Receptor Sem Fio Bodypack',
        'marca': 'Sony',
        'modelo': 'URX-P03 (Kit UWP-D11)',
        'fotos': ['IMG_20261111_103556.jpg', 'IMG_20261111_103625.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento no estojo (fita 02)', '2. Especificação técnica / Serial do fabricante'],
        'tombamento_oficial': None,
        'status_tombamento': 'NÃO TOMBADO (Sem foto de tombamento = Objeto não estava tombado)',
        'especificacao_tecnica': 'S/N: 115983, Faixa 42-51 (638.125-697.875 MHz)',
        'estado_fisico': 'Normal'
    },
    {
        'id': 4,
        'equipamento': 'Mesa de Som Analógica USB',
        'marca': 'Yamaha',
        'modelo': 'MG12XU',
        'fotos': ['IMG_20261111_103810.jpg', 'IMG_20261111_103849.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento (painel superior)', '2. Especificação técnica / Serial no painel traseiro'],
        'tombamento_oficial': None,
        'status_tombamento': 'NÃO TOMBADO (Sem foto de tombamento = Objeto não estava tombado)',
        'especificacao_tecnica': 'S/N: BRACVX01071, 12 canais, efeitos SPX, USB 2.0',
        'estado_fisico': 'Normal'
    },
    {
        'id': 5,
        'equipamento': 'Switcher de Vídeo Broadcast 4K',
        'marca': 'Blackmagic Design',
        'modelo': 'ATEM Television Studio Pro 4K',
        'fotos': ['IMG_20261111_103949.jpg', 'IMG_20261111_104009.jpg', 'IMG_20261111_104014.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento', '2. Especificação técnica / Serial do fabricante', '3. Placa de tombamento UEG'],
        'tombamento_oficial': '03269767',
        'status_tombamento': 'TOMBADO (Placa oficial 03269767 fixada no chassi)',
        'especificacao_tecnica': 'S/N: 9798249, switcher broadcast 4K 8 entradas',
        'estado_fisico': 'Imperfeição (fita adesiva preta sobre as teclas 4 a 10)'
    },
    {
        'id': 6,
        'equipamento': 'Computador Desktop Slim (SFF)',
        'marca': 'Dell',
        'modelo': 'OptiPlex 5090 (Core i7)',
        'fotos': ['IMG_20261111_104048.jpg', 'IMG_20261111_104129.jpg', 'IMG_20261111_104140.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento na bancada', '2. Especificação técnica / Etiqueta regulatória', '3. Placa de tombamento UEG'],
        'tombamento_oficial': '02612297',
        'status_tombamento': 'TOMBADO (Placa metálica 02612297)',
        'especificacao_tecnica': 'DP/N: RP4H1 A00 BRH1, Reg Model D15S',
        'estado_fisico': 'Normal'
    },
    {
        'id': 7,
        'equipamento': 'Monitor Flat Panel 23.8"',
        'marca': 'Dell',
        'modelo': 'P2422Hb',
        'fotos': ['IMG_20261111_104156.jpg', 'IMG_20261111_104211.jpg', 'IMG_20261111_104217.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento', '2. Especificação técnica / Service Tag do fabricante', '3. Placa de tombamento UEG'],
        'tombamento_oficial': '02612249',
        'status_tombamento': 'TOMBADO (Placa oficial 02612249)',
        'especificacao_tecnica': 'Service Tag: GZ9BHH3, Express SVC: 369 604 859 43, Fabr: Nov/2021',
        'estado_fisico': 'Normal'
    },
    {
        'id': 8,
        'equipamento': 'Monitor Pivot Vertical 19.5"',
        'marca': 'Dell',
        'modelo': 'P2014Ht',
        'fotos': ['IMG_20261111_104232.jpg', 'IMG_20261111_104244.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento vertical', '2. Especificação técnica / Portas traseiras'],
        'tombamento_oficial': None,
        'status_tombamento': 'NÃO TOMBADO (Sem foto de tombamento = Objeto não estava tombado)',
        'especificacao_tecnica': 'Model P2014Ht, portas VGA/DVI/DP/USB',
        'estado_fisico': 'Normal'
    },
    {
        'id': 9,
        'equipamento': 'Notebook ("PAINEL LED")',
        'marca': 'Dell',
        'modelo': 'Latitude 3420',
        'fotos': ['IMG_20261111_104324.jpg', 'IMG_20261111_104356.jpg', 'IMG_20261111_104408.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento com tag manual', '2. Especificação técnica / Service Tag na base', '3. Placa de tombamento UEG no teclado'],
        'tombamento_oficial': '02610808',
        'status_tombamento': 'TOMBADO (Placa oficial 02610808)',
        'especificacao_tecnica': 'Service Tag: C8XH2L3, Express Code: 26661341271, Reg Model P144G',
        'estado_fisico': 'Normal'
    },
    {
        'id': 10,
        'equipamento': 'Processador de Vídeo LED (Rackmount)',
        'marca': 'NovaStar',
        'modelo': 'VX400 (All-in-One Controller)',
        'fotos': ['IMG_20261111_104431.jpg', 'IMG_20261111_104438.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento montado no rack', '2. Especificação técnica / Etiqueta do fabricante'],
        'tombamento_oficial': None,
        'status_tombamento': 'NÃO TOMBADO (Sem foto de tombamento = Objeto não estava tombado)',
        'especificacao_tecnica': 'S/N: 21MB44422N0A10002120, entradas HDMI/DVI/SDI/Ópticas',
        'estado_fisico': 'Normal'
    },
    {
        'id': 11,
        'equipamento': 'Servidor de Ingest e Playout 4U (Rackmount)',
        'marca': 'Floripa Tecnologia',
        'modelo': 'Spotware - M (tag operacional UEGSW1)',
        'fotos': ['IMG_20261111_104514.jpg', 'IMG_20261111_104547.jpg'],
        'ordem_fotos': ['1. Visão geral frontal no rack (fita UEGSW1)', '2. Especificação técnica traseira do fabricante'],
        'tombamento_oficial': None,
        'status_tombamento': 'NÃO TOMBADO NO CHASSI (Sem foto de tombamento = Sem placa física afixada)',
        'especificacao_tecnica': 'S/N: 008479010011225, Fabr: 05/01/2023, Floripa Tecnologia Ind e Com LTDA',
        'estado_fisico': 'Normal'
    },
    {
        'id': 12,
        'equipamento': 'Roteador Wireless 300Mbps',
        'marca': 'D-Link',
        'modelo': 'DIR-615',
        'fotos': ['IMG_20261111_104755.jpg', 'IMG_20261111_104809.jpg'],
        'ordem_fotos': ['1. Visão geral com etiqueta manual Secretaria/Tombo antigo', '2. Especificação técnica na base'],
        'tombamento_oficial': None,
        'status_tombamento': 'NÃO TOMBADO OFICIALMENTE (Etiqueta manual TOMBO 702226 / UEG 72490)',
        'especificacao_tecnica': 'S/N: F3XE4B7024692, MAC: 84C9B24D4C04, H/W: E5, F/W: 5.11BR',
        'estado_fisico': 'Imperfeição (restos de fita crepe antiga da Secretaria)'
    },
    {
        'id': 13,
        'equipamento': 'Placa de Captura de Vídeo USB 3.0',
        'marca': 'ezcap',
        'modelo': 'Game Pro 4K60fps (COD. 13729)',
        'fotos': ['IMG_20261111_104826.jpg', 'IMG_20261111_104837.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento', '2. Especificação técnica no verso'],
        'tombamento_oficial': None,
        'status_tombamento': 'NÃO TOMBADO (Sem foto de tombamento = Objeto não estava tombado)',
        'especificacao_tecnica': 'S/N: EZCAP26920100003, USB 3.0 4K60fps capture',
        'estado_fisico': 'Normal'
    },
    {
        'id': 14,
        'equipamento': 'HD Externo Portátil 4TB',
        'marca': 'Seagate',
        'modelo': 'Portable Drive (SRD0NF1 / 2N1AP6-500)',
        'fotos': ['IMG_20261111_104935.jpg', 'IMG_20261111_104945.jpg'],
        'ordem_fotos': ['1. Visão geral do equipamento com etiqueta Loggagem 08', '2. Especificação técnica na base'],
        'tombamento_oficial': None,
        'status_tombamento': 'NÃO TOMBADO (Sem foto de tombamento = Objeto não estava tombado)',
        'especificacao_tecnica': 'S/N: NT3D44VV, Capacidade 4TB (3,63TB formatado), Fabr: 2024',
        'estado_fisico': 'Normal'
    }
]

total_photos = sum(len(x['fotos']) for x in items_sequence)
print('Total sequence items:', len(items_sequence))
print('Total photos mapped:', total_photos)

# Save structured sequence
with open('data/sequencia_auditoria_temporal.json', 'w', encoding='utf-8') as f:
    json.dump(items_sequence, f, ensure_ascii=False, indent=2)

print('Saved data/sequencia_auditoria_temporal.json successfully!')
