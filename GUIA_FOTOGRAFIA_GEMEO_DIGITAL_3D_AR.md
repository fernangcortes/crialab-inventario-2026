# Guia Técnico de Captura Fotográfica para IA, Inventário e Gêmeo Digital 3D / Realidade Aumentada (AR)
**CriaLab & Radioteledifusão – UEG UnU Goiânia-Laranjeiras**
*Referência Arquitetônica: Planta Baixa Layout R05_25_11_2025*

> 🌐 **Versão Web Ilustrada Interativa:** Acesse o manual visual com plantas arquitetônicas em SVG, cones de visão e simulação passo a passo no arquivo [`guia_fotografia_3d_ar.html`](guia_fotografia_3d_ar.html) ou via [Painel do Inventário](dashboard.html).

---

## 1. Objetivo Estratégico

Este protocolo estabelece o padrão ideal de registro fotográfico dos espaços e equipamentos do CriaLab para cumprir três objetivos integrados:
1. **Auditoria Patrimonial Automatizada por IA:** Leitura imediata de placas de tombamento, códigos de barra, etiquetas de serviço (Service Tag Dell, números de série) e detecção de avarias físicas.
2. **Reconstrução Espacial 3D (Fotogrametria / NeRF / Gaussian Splatting):** Geração de nuvens de pontos e malhas 3D para maquete digital e gêmeo virtual dos estúdios.
3. **Realidade Aumentada (AR):** Projeção dos estúdios e posicionamento de equipamentos virtuais (modelos 3D enriquecidos via web) para pré-visualização de iluminação, cenografia e fluxo técnico.

---

## 2. Padrão de Captura dos Ambientes (Espaços)

Para alimentar motores de reconstrução 3D e permitir que os agentes de IA compreendam a volumetria e a disposição dos estúdios:

### A. Técnica dos 4 Cantos (Enquadramento 45º)
* Posicione-se em cada um dos 4 vértices (cantos) da sala.
* Aponte a câmera para o centro/canto oposto em ângulo de 45º.
* **Altura Constante:** Mantenha a câmera na linha dos olhos (~1,50 m a 1,60 m do chão).
* **Orientação:** Preferencialmente em modo paisagem (horizontal) ou faça um giro vertical se o pé-direito for alto (o CriaLab possui P.D. = 2,70m).

### B. Fotos Periféricas e de Transição (Overlap de 60% a 70%)
* Caminhe pelas paredes tirando fotos com sobreposição de pelo menos 60% entre uma imagem e a seguinte.
* Isso garante os pontos homólogos necessários para que softwares como *Meshroom*, *RealityCapture*, *Luma AI*, *Polycam* ou pipelines de *Gaussian Splatting* calculem as poses exatas de câmera sem distorção.

### C. Condições de Iluminação
* Mantenha todas as luzes do teto e iluminação de serviço acesas.
* Evite luzes de cena saturadas (como refletores RGB coloridos muito fortes) durante o scan de fotogrametria. A iluminação uniforme (branca/neutra) facilita tanto a textura 3D quanto o OCR da IA.

---

## 3. Padrão de Captura dos Equipamentos

Para cada equipamento relevante, o padrão ideal é a **Dupla de Imagens (Visão de Contexto + Macro de Identificação)**:

```
[Foto 1: Contexto / Enquadramento]  ───►  Mostra o bem instalado no ambiente (mesa, rack, tripé)
[Foto 2: Macro / Plaqueta & Serial] ───►  Mostra etiqueta UEG com código de barras e S/N do fabricante
```

### Regras Práticas para o Agente de IA:
1. **Evitar Reflexo no Código de Barras:** Em placas de alumínio ou etiquetas com fita adesiva brilhante, incline o celular levemente (~15º a 20º em relação à superfície) para que o flash ou a luz do teto não estoure o branco sobre os números.
2. **Etiqueta Técnica do Fabricante:** Sempre que possível, fotografe a etiqueta traseira ou inferior do fabricante (ex: *Dell Service Tag*, etiqueta *Sony*, *NovaStar*, *Behringer*, *Yamaha*). Se o tombamento estiver sem placa, o agente recupera o bem no inventário mestre pelo número de série!
3. **Equipamentos em Rack (como a COT):**
   * 1 foto geral do rack inteiro.
   * 1 foto de cada unidade de rack (1U, 2U, 4U) mostrando os painéis frontais.
   * 1 foto dos painéis traseiros com conexões e etiquetas técnicas.

---

## 4. Estrutura Padronizada de Diretórios (Alinhada à Planta Baixa)

Organize os futuros lotes de fotos seguindo a exata nomenclatura da Planta Baixa oficial (`planta/Laranjeiras Layout - Modificado R05_25_11_2025.pdf`):

```text
fotos/
├── 01_estudio_tv/               # Estúdio 01 - TV (42,20m²)
├── 02_estudio_radio/            # Estúdio 02 - Rádio (13,27m²)
├── 03_estudio_videocast/        # Estúdio 03 - VideoCast (21,82m²)
├── 04_estudio_04/               # Estúdio 04 (13,40m²)
├── 05_estudio_05/               # Estúdio 05 (5,53m²)
├── 06_sala_equipamentos/        # Almoxarifado / Acervo Técnico (13,40m²)
├── 07_central_operacao_tecnica/ # COT / Sala Técnica (12,25m²) [Concluído - 31 fotos]
├── 08_redacao/                  # Redação (111,46m² - 32 Estações)
├── 09_gabinetes_e01_a_e08/      # Gabinetes E01 a E08 (~3,2m² cada)
├── 10_coordenacao_adm/          # Coordenação Administrativa (13,49m²)
├── 11_naufo/                    # NAUFO (13,67m²)
└── 12_halls/                    # Hall Entrada (10,44m²) e Circulação (16,42m²)
```

---

## 5. Pipeline para Realidade Aumentada (AR) e Modelagem Virtual

Como você observou, **não é necessário modelar manualmente cada defeito ou marca física de cada equipamento**:

1. **Catálogo de Modelos Gêmeos (Digital Twin Proxy):**
   * O agente identifica a marca e modelo exato (ex: *Behringer X32 Producer*, *Sony URX-P03*, *Blackmagic ATEM Television Studio Pro 4K*, *Dell OptiPlex 5090*, *Dell Monitor P2422Hb*).
   * O sistema busca modelos 3D low-poly/mid-poly prontos nos repositórios padrão (Sketchfab, Poly Haven, CGTrader, TurboSquid ou nos sites dos próprios fabricantes).
   * Os modelos são exportados nos formatos universais de Realidade Aumentada:
     * **`.GLB` / `.GLTF`:** Para web 3D (Three.js / WebXR / Android Scene Viewer).
     * **`.USDZ`:** Para Realidade Aumentada nativa em iOS (Quick Look).
2. **Posicionamento Espacial Automatizado:**
   * Com base nas coordenadas da Planta Baixa e nos pontos identificados nas fotos, os modelos 3D dos equipamentos são inseridos na maquete digital nas suas exatas posições (bancada da COT, grid de luz, mesas da redação).
3. **Simulação e Testes de Cenário (AR):**
   * Permite que técnicos e professores usem o celular ou óculos AR para enxergar modificações de estúdio, novos ângulos de câmera e novas disposições de iluminação diretamente no espaço físico antes de qualquer mudança estrutural.

---

## 6. Tratamento de Bens em Externa (Estoque Now)

Quando um equipamento cadastrado não estiver presente no cômodo:
* A foto do armário ou estante vazia não resultará em "bem extraviado".
* Ao cruzar com a base do **Estoque Now** (`data/estoquenow.csv`), o sistema identificará que o equipamento está em missão externa ou empréstimo ativo para projeto/estudante, registrando automaticamente a conformidade com justificativa oficial para o processo SEI.
