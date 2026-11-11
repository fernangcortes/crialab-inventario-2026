# Inventário Patrimonial 2026 — CriaLab & Radioteledifusão UEG
## Guia de Instrução Documental SEI Goiás & Automação de Pesquisa (`sei_search.py`)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![SEI Goiás](https://img.shields.io/badge/SEI-Goi%C3%A1s-green.svg)](https://sei.goias.gov.br)
[![Test Suite](https://img.shields.io/badge/tests-88%20passed%20(100%25)-brightgreen.svg)](test_sei_search.py)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero%20mandatory-orange.svg)](#requisitos-e-instalação)

---

## 1. Visão Geral e Contexto Institucional

Este repositório consolida as ferramentas técnicas, o dossiê documental e os mecanismos de automação desenvolvidos para a instrução, conferência física e regularização patrimonial no âmbito do **Processo SEI nº 202600005037287** do Estado de Goiás.

Os trabalhos atendem à Comissão Setorial de Inventário instituída pela **Portaria UEG nº 1210/2026**, responsável pelo acervo permanente da **Unidade Universitária de Goiânia-Laranjeiras (Código SPM 10807)**, abrangendo especificamente:
- **CriaLab|UEG**: Laboratório de Pesquisas Criativas e Inovação em Audiovisual (Carga oficial SPM: 285 bens).
- **Radioteledifusão UEG / COT**: Central de Operação Técnica e estúdios de broadcasting da UEG TV (Carga oficial SPM: 92 bens).
- **Acervo Operacional Estoque Now**: 245 itens operacionais de cinema e audiovisual geridos setorialmente.

### Prazos e Diretrizes Oficiais:
- **Processo Principal:** SEI nº `202600005037287`.
- **Despacho de Prorrogação:** `DESPACHO Nº 1049/2026/UEG/COPA-14028` (SEI nº `97743688`), emitido pelo Coordenador de Patrimônio Isaquiel Melo Peres.
- **Prazo Fatal para Envio:** **13 de novembro de 2026**, com encaminhamento obrigatório das fichas e dossiê probatório à Unidade SEI `UEG/COPA - 14028`.
- **Período de Bloqueio Patrimonial:** Vedação expressa de movimentações físicas e contábeis de **09/10/2026 a 17/12/2026** (Ofício Circular nº 191/2026/UEG - Processo SEI nº 202600020016196).

---

## 2. Requisitos e Instalação

### Requisitos do Sistema:
- **Python 3.8 ou superior** (testado e homologado inclusive em Python 3.11, 3.12, 3.13 e 3.15).
- **Zero Dependências Externas Obrigatórias**: O núcleo do script foi desenvolvido exclusivamente sobre os módulos nativos da biblioteca padrão do Python (`urllib.request`, `urllib.parse`, `html.parser`, `json`, `csv`, `re`, `argparse`, `ssl`). Executa imediatamente em qualquer instalação limpa de Python sem necessidade de privilégios de administrador ou conexão com a internet.

### Instalação e Execução Imediata:
```bash
# Clone ou acesse a pasta do repositório
cd c:\Users\FGC\dev\CriaLab\inventario\2026

# Execução direta com o Python do sistema (zero-install)
python sei_search.py --mock --term "Yamaha"
```

### Modo Acelerado (Opcional):
Caso deseje utilizar adaptadores HTTP avançados com pool de conexões e parser BeautifulSoup, instale opcionalmente os pacotes recomendados:
```bash
pip install requests beautifulsoup4
```
O script detecta automaticamente a presença dessas bibliotecas em tempo de execução via arquitetura *Dual-Mode Engine*.

---

## 3. Manual da Interface de Linha de Comando (CLI)

O script `sei_search.py` disponibiliza parâmetros completos para consultas automatizadas, filtros combinados e exportações multifiltradas.

### 3.1. Resumo de Parâmetros e Opções

| Parâmetro | Flag Curta | Tipo | Descrição |
|---|---|---|---|
| `--term` | `-t` | `string` | Termo de pesquisa livre geral (ex: `"Spotware"`, `"MG12XU"`, `"NovaStar"`) |
| `--process` | `-p` | `string` | Número do processo SEI / NUP com ou sem máscara (ex: `202600005037287`) |
| `--doc` / `--document` | `-d` | `string` | Número único do documento SEI (ex: `97743688`) |
| `--serial` | `-s` | `string` | Número de série de fábrica do equipamento (ex: `BRACVX01071`, `008479010011225`) |
| `--model` | `-m` | `string` | Modelo do equipamento (ex: `MG12XU`, `Spotware-M`, `VX400`, `URX-P03`) |
| `--supplier` / `--interessado` | | `string` | Nome empresarial, razão social ou CNPJ do fornecedor |
| `--unit` | `-u` | `string` | Sigla da unidade produtora no SEI (ex: `UEG/COPA-14028`, `COT`, `UEG`) |
| `--date-from` / `--data-inicio` | | `DD/MM/AAAA` | Data inicial de autuação ou expedição documental |
| `--date-to` / `--data-fim` | | `DD/MM/AAAA` | Data final de autuação ou expedição documental |
| `--assunto` | | `string` | Código ou descrição do assunto administrativo |
| `--format` | `-f` | `choice` | Formato de saída: `json`, `csv`, `markdown`, `table` [padrão: `json`] |
| `--output` | `-o` | `path` | Arquivo físico de destino para gravação dos resultados estruturados |
| `--limit` | | `int` | Limite máximo de registros a serem retornados |
| `--mock` | | `flag` | Ativa o simulador offline com fixtures contendo dados patrimoniais reais |
| `--fixture-file` | | `path` | Carrega arquivo customizado de fixtures em JSON ou HTML |
| `--cross-inventory` | | `flag` | Cruza os termos com as bases locais (`inventario_master.json` e `estoquenow_completo.json`) |
| `--verbose` / `--debug` | `-v` | `flag` | Habilita logs detalhados de diagnóstico na saída de erro (`stderr`) |
| `--quiet` | `-q` | `flag` | Omite mensagens informativas e emite apenas os dados puros |
| `--base-url` | | `url` | URL base do portal SEI Goiás (padrão: `https://sei.goias.gov.br`) |
| `--timeout` | | `int` | Tempo limite para requisições HTTP em segundos (padrão: 15s) |
| `--retries` | | `int` | Número de tentativas com recuo exponencial em caso de erro transitório (padrão: 3) |
| `--insecure` | | `flag` | Ignora erros de validação de certificado SSL (cadeia ICP-Brasil) |

### 3.2. Códigos de Saída (Exit Codes)
- **`0`**: Execução concluída com sucesso (registros encontrados ou pesquisa finalizada sem erros).
- **`1`**: Erro de validação de parâmetros, arquivo inexistente, formato inválido ou falha de conexão de rede.

---

## 4. Receitas Prontas de Pesquisa para os Bens Não Tombados

Abaixo encontram-se os comandos prontos e parametrizados para localização imediata dos ativos auditados na Central de Operação Técnica (COT) e CriaLab:

### Caso 1: Servidor de Ingest e Playout Floripa Spotware-M
- **Identificação Física:** Tag `UEGSW1`, S/N `008479010011225`, Fabricação `05/01/2023`.
- **Descoberta:** Pertencente ao **Contrato nº 068/2022** firmado com a empresa Floripa Tecnologia (CNPJ `01.151.131/0001-32`), vinculado ao **Processo SEI nº `202100020006687`**. Tombamento SPM correspondente: nº `3111136` (Seq 259 CriaLab).
```bash
# Busca pelo serial do equipamento
python sei_search.py --mock --serial "008479010011225" --format markdown

# Busca cruzada por fornecedor e modelo
python sei_search.py --mock --supplier "Floripa Tecnologia" --model "Spotware-M" --format json
```

### Caso 2: Mesa de Som Analógica Yamaha MG12XU
- **Identificação Física:** 12 canais, efeitos SPX, interface USB, S/N `BRACVX01071`.
- **Contexto:** Presente no catálogo operacional do Estoque Now (Código `000215`). Ausente de plaqueta física na bancada da COT.
```bash
# Busca pelo número de série da mesa
python sei_search.py --mock --serial "BRACVX01071" --format markdown

# Busca pelo modelo e marca
python sei_search.py --mock --model "MG12XU" --term "Yamaha" --format table
```

### Caso 3: Processador de Vídeo LED NovaStar VX400
- **Identificação Física:** Controlador All-in-One HDMI/DVI/SDI, S/N `21MB44422N0A10002120`.
- **Contexto:** Alocado no rack da COT para alimentação do painel de LED do estúdio/auditório.
```bash
# Busca direta pelo serial do controlador
python sei_search.py --mock --serial "21MB44422N0A10002120" --format json

# Exportação para arquivo CSV
python sei_search.py --mock --model "VX400" --format csv --output "novastar_sei.csv"
```

### Caso 4: Receptor Sem Fio Bodypack Sony URX-P03 (Kit UWP-D11)
- **Identificação Física:** Faixa 42-51 (638-697 MHz), S/N `115983`, etiqueta adesiva "fita 02".
- **Descoberta:** Identificado como receptor do **Kit UWP-D11 nº 2** da Radioteledifusão UEG, registrado no SPM sob o tombamento nº `836315`.
```bash
# Busca pelo serial e unidade setorial
python sei_search.py --mock --serial "115983" --unit "COT" --format markdown
```

### Caso 5: Estações de Trabalho e Monitores CriaLab (Alta Potência)
- **Origem Administrativa:** **Pregão Eletrônico nº 016/2024** da UEG (Processo de compra nº `105104`), autuado no **Processo SEI nº `202400005010184`**. Valor contratado: R$ 197.410,12.
```bash
# Localização de empenho e notas fiscais das workstations
python sei_search.py --mock --process "202400005010184" --format markdown
```

### Caso 6: Desfazimento de Inservíveis pelo Programa SUKATECH
- **Normativa:** Decreto Estadual nº 9.718/2020 e Despacho nº 707/2026/UEG/COPA-14028, autuado no **Processo SEI nº `202600020003350`**.
```bash
# Consulta do processo de desfazimento e modelo de Termo de Responsabilidade *ST
python sei_search.py --mock --process "202600020003350" --format table
```

### Caso 7: Roteador Wireless D-Link DIR-615 (Tombamento Legado)
- **Identificação Física:** S/N `F3XE4B7024692`, MAC `84C9B24D4C04`, etiquetas manuscritas `TOMBO 702226 / UEG 72490`.
- **Estratégia:** Item legado do acervo histórico da unidade, regularizável mediante atualização de tombamento anterior no SPM.
```bash
# Busca pelo serial do roteador
python sei_search.py --mock --serial "F3XE4B7024692" --format json
```

---

## 5. Formatos de Saída Suportados

### 5.1. JSON Canônico (`--format json`)
Retorna um array estruturado de objetos de acordo com o esquema definido em `PROJECT.md`:
```json
[
  {
    "process_number": "202100020006687",
    "document_number": "97743688",
    "document_type": "Nota Fiscal",
    "date": "05/01/2023",
    "unit": "UEG/COPA-14028",
    "interested": "Floripa Tecnologia Ind e Com LTDA",
    "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_spotware_008479010011225",
    "snippet": "Servidor de Ingest e Playout Spotware-M S/N 008479010011225 Tag UEGSW1 - Contrato 068/2022 Floripa Tecnologia CNPJ 01.151.131/0001-32 Tombamento 3111136"
  }
]
```

### 5.2. CSV Formatado (`--format csv`)
Em conformidade com a RFC-4180 e compatível com Excel/LibreOffice (delimitado por vírgulas, escape de aspas e codificação UTF-8-sig):
```csv
process_number,document_number,document_type,date,unit,interested,link,snippet
202600005037287,97743689,Nota Fiscal,15/03/2023,UEG/COPA-14028,Yamaha Musical do Brasil / Distribuidora Áudio Profissional,https://sei.goias.gov.br/...,Mesa Analógica Yamaha MG12XU 12 canais USB efeitos SPX S/N BRACVX01071 - CriaLab
```

### 5.3. Markdown (`--format markdown`)
Renderiza uma tabela elegante pronta para incorporação direta em relatórios administrativos e despachos SEI:
```markdown
# Resultados da Pesquisa SEI Goiás

- **Total de registros encontrados:** 1
- **Data da consulta:** 11/11/2026 17:00:00

| ID | Processo | Documento | Tipo | Data | Unidade | Interessado | Link | Trecho / Snippet |
|---|---|---|---|---|---|---|---|---|
| 1 | 202600005037287 | 97743689 | Nota Fiscal | 15/03/2023 | UEG/COPA-14028 | Yamaha Musical | [97743689](https://...) | Mesa Yamaha MG12XU S/N BRACVX01071 |
```

### 5.4. Tabela Textual (`--format table`)
Apresenta uma tabela ASCII com bordas estruturadas, ideal para visualização rápida no terminal do operador.

---

## 6. Instrução Probatória e Guia Documental Patrimonial

Para fundamentar as decisões perante a Coordenação de Patrimônio da UEG (`UEG/COPA - 14028`), consulte o documento oficial completo:
👉 **[`GUIA_INSTRUCAO_PATRIMONIAL_SEI.md`](GUIA_INSTRUCAO_PATRIMONIAL_SEI.md)**

### Os 7 Tipos Documentais Probatórios Exigidos:
1. **Nota Fiscal de Compra (DANFE):** Comprova a titularidade originária, custo contábil de entrada e números de série para início da depreciação acumulada (Lei Federal nº 4.320/1964).
2. **Processo Licitatório (Edital, Termo de Referência, Contrato):** Demonstra a legalidade do ato administrativo e especificações técnicas contratadas (Leis nº 8.666/1993 e nº 14.133/2021).
3. **Nota de Empenho (NE):** Vincula a despesa ao elemento `44.90.52 - Material Permanente` no SIOFI-Net.
4. **Ordem de Fornecimento & Termo de Recebimento Definitivo (Atesto):** Fixa o marco temporal da entrega física na unidade por servidor habilitado.
5. **Termo de Doação / Cessão de Uso / Transferência:** Formaliza a transmissão jurídica de acervos oriundos de projetos de pesquisa (FAPEG, CNPq) ou doações privadas.
6. **Termo de Responsabilidade / Cautela (Minuta SEI nº 92319152):** Atribui a guarda e vigilância aos titulares dos laboratórios (IN nº 005/2019-SEAD).
7. **Ficha de Apuração do SPM (Bens Não Cadastrados):** Documento oficial para geração de plaquetas e cadastramento no acervo estadual.

### Procedimento Especial — TCA (Termo Circunstanciado Administrativo):
Para apuração célere de bens móveis extraviados ou não localizados cujo valor econômico não justifique sindicância complexa, instruir os autos conforme a **Instrução Normativa nº 02/2023-CGE** e orientações do Ofício Externo SEAD nº 2317 (SEI nº 97650901).

---

## 7. Suíte Automatizada de Testes E2E

A confiabilidade de toda a suíte é comprovada por testes unitários e de integração de ponta a ponta:

```bash
# Executa todos os 88 testes automatizados (Tiers 1 a 4)
python test_sei_search.py

# Execução com verbosidade detalhada
python test_sei_search.py -v
```

### Arquitetura dos Níveis de Teste (Test Tiers):
- **Tier 1 (Feature Coverage — 45 Testes):** Cobre individualmente todas as flags e filtros CLI (`--term`, `--process`, `--serial`, `--model`, `--supplier` [com suporte a CNPJ formatado e desformatado], `--unit`, `--format`, `--output`, `--mock`).
- **Tier 2 (Boundary & Corner Cases — 17 Testes):** Valida termos vazios, acentuação UTF-8, símbolos técnicos (`Ø82mm`), seriais inexistentes, datas inválidas (rejeição estrita com código 1), formatos desconhecidos, isolamento de `<thead>` no parser HTML e blindagem de pipes no Markdown.
- **Tier 3 (Cross-Feature Combinations — 15 Testes):** Valida combinações multi-flags, filtros cumulativos AND, restrição de cardinalidade `--limit`, agregação de flags curtas e integração cruzada `--cross-inventory` com Estoque Now e SPM Master.
- **Tier 4 (Real-World Scenarios & Document Audit — 11 Testes):** Valida os 5 cenários reais de busca dos bens não tombados e audita formalmente o conteúdo, normas jurídicas e integridade de `GUIA_INSTRUCAO_PATRIMONIAL_SEI.md`.

---

## 8. Estrutura do Repositório

```
inventario/2026/
├── sei_search.py                      # Script principal de automação e busca pública SEI
├── GUIA_INSTRUCAO_PATRIMONIAL_SEI.md   # Guia exaustivo de instrução processual patrimonial
├── README.md                           # Este manual operacional consolidado
├── test_sei_search.py                  # Suíte automatizada de testes E2E (88 testes)
├── TEST_INFRA.md                       # Matriz de cobertura e arquitetura de testes
├── TEST_READY.md                       # Relatório de prontidão da suíte de testes
├── fixtures/
│   └── sei_mock_fixtures.json          # Base de dados em JSON para simulação offline
├── data/
│   ├── inventario_master.json          # Carga oficial SPM (377 bens móveis da unidade)
│   ├── estoquenow_completo.json        # Catálogo do sistema Estoque Now (245 itens)
│   └── bens_nao_cadastrados_cot.json   # Bens sem plaqueta auditados na COT
└── fichas/
    ├── Ficha_Apuracao_CriaLab_Preenchida.html
    └── Ficha_Apuracao_Radioteledifusao_Preenchida.html
```

---

## 9. Conformidade e Integridade

Desenvolvido para apoio às atividades administrativas e acadêmicas da Universidade Estadual de Goiás — Unidade Universitária de Goiânia-Laranjeiras. Todos os dados fictícios utilizados no modo de simulação preservam rigorosamente o sigilo e a integridade das bases públicas estaduais.
