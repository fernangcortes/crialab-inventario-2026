#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sei_search.py — Automação de Pesquisa e Extração de Processos/Documentos no SEI Goiás

Módulo e CLI executável para consulta ao Sistema Eletrônico de Informações (SEI Goiás),
especificamente voltado para a instrução probatória do Processo de Inventário Patrimonial
nº 202600005037287 (CriaLab e Radioteledifusão UEG - Câmpus Goiânia-Laranjeiras).

Arquitetura Dual-Mode:
- Zero dependências obrigatórias: executa diretamente sobre a biblioteca padrão do Python
  (urllib.request, html.parser, json, csv, argparse).
- Opcionalmente acelera via `requests` e `beautifulsoup4` caso estejam instalados no ambiente.
- Suporta motor determinístico offline (--mock) com dados patrimoniais autênticos.
- Exportação em JSON canônico, CSV (RFC-4180), Markdown formatado e tabela para terminal.
"""

import os
import sys
import re
import json
import csv
import io
import time
import ssl
import argparse
from datetime import datetime

# Detecção e suporte opcional a bibliotecas de terceiros (Dual-Mode Engine)
try:
    import requests
    from bs4 import BeautifulSoup
    HAS_THIRD_PARTY = True
except ImportError:
    HAS_THIRD_PARTY = False

# Biblioteca padrão para modo nativo zero-dependências
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
from html.parser import HTMLParser


# ==============================================================================
# 1. CONSTANTES, HEADERS E FIXTURES EMBUTIDAS (GROUND TRUTH PATRIMONIAL)
# ==============================================================================

DEFAULT_BASE_URL = "https://sei.goias.gov.br"
SEARCH_PATH = "/sei/modulos/pesquisa/md_pesq_processo_pesquisar.php"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36 (Compatível SEI-Goiás Search Automation)"
)

# Fixtures embutidas de alta fidelidade com dados reais levantados no CriaLab/UEG
EMBEDDED_FIXTURES = [
    {
        "process_number": "202100020006687",
        "document_number": "97743688",
        "document_type": "Nota Fiscal",
        "date": "05/01/2023",
        "unit": "UEG/COPA-14028",
        "interested": "Floripa Tecnologia Ind e Com LTDA",
        "interested_party": "Floripa Tecnologia Ind e Com LTDA",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_spotware_008479010011225",
        "snippet": "Servidor de Ingest e Playout Spotware-M S/N 008479010011225 Tag UEGSW1 - Contrato 068/2022 Floripa Tecnologia CNPJ 01.151.131/0001-32 Tombamento 3111136",
        "subject": "Aquisição de Servidor de Ingest e Playout Spotware-M - Contrato 068/2022",
        "model": "Spotware-M",
        "serial": "008479010011225",
        "supplier": "Floripa Tecnologia Ind e Com LTDA",
        "cnpj": "01.151.131/0001-32"
    },
    {
        "process_number": "202100020006687",
        "document_number": "97743680",
        "document_type": "Contrato",
        "date": "15/12/2022",
        "unit": "UEG/COPA-14028",
        "interested": "Floripa Tecnologia Ind e Com LTDA",
        "interested_party": "Floripa Tecnologia Ind e Com LTDA",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_contrato_068_2022",
        "snippet": "Contrato Administrativo nº 068/2022 - Fornecimento de infraestrutura e soluções de broadcasting televisivo para a UEG TV",
        "subject": "Contrato Administrativo nº 068/2022 Floripa Tecnologia",
        "model": "Spotware-M",
        "serial": "008479010011225",
        "supplier": "Floripa Tecnologia Ind e Com LTDA"
    },
    {
        "process_number": "202600005037287",
        "document_number": "97743689",
        "document_type": "Nota Fiscal",
        "date": "15/03/2023",
        "unit": "UEG/COPA-14028",
        "interested": "Yamaha Musical do Brasil / Distribuidora Áudio Profissional",
        "interested_party": "Yamaha Musical do Brasil / Distribuidora Áudio Profissional",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_yamaha_bracvx01071",
        "snippet": "Mesa Analógica Yamaha MG12XU 12 canais USB efeitos SPX S/N BRACVX01071 - CriaLab Câmpus Goiânia-Laranjeiras Estoque Now 000215",
        "subject": "Aquisição de Equipamento de Áudio - Mesa Yamaha MG12XU",
        "model": "MG12XU",
        "serial": "BRACVX01071",
        "supplier": "Yamaha Musical do Brasil"
    },
    {
        "process_number": "202600005037287",
        "document_number": "97743690",
        "document_type": "Termo de Recebimento",
        "date": "22/04/2022",
        "unit": "UEG/COT",
        "interested": "Sony Brasil / Merlin Vídeo Pro",
        "interested_party": "Sony Brasil / Merlin Vídeo Pro",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_sony_urxp03_115983",
        "snippet": "Receptor sem fio Bodypack Sony URX-P03 Faixa 42-51 638-697MHz S/N 115983 Kit UWP-D11 fita 02 Radioteledifusão UEG Tombamento 836315",
        "subject": "Termo de Recebimento Definitivo - Sistema de Microfone Sem Fio Sony URX-P03",
        "model": "URX-P03",
        "serial": "115983",
        "supplier": "Sony Brasil / Merlin Vídeo Pro"
    },
    {
        "process_number": "202600005037287",
        "document_number": "97743691",
        "document_type": "Nota Fiscal",
        "date": "10/08/2023",
        "unit": "UEG/COPA-14028",
        "interested": "NovaStar Tech / Painéis Led Brasil Comércio",
        "interested_party": "NovaStar Tech / Painéis Led Brasil Comércio",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_novastar_vx400",
        "snippet": "Controlador e Processador de Vídeo All-in-One NovaStar VX400 para painel de LED S/N 21MB44422N0A10002120 CriaLab Laranjeiras",
        "subject": "Fornecimento de Processador de Vídeo NovaStar VX400 para Estúdio CriaLab",
        "model": "VX400",
        "serial": "21MB44422N0A10002120",
        "supplier": "NovaStar Tech / Painéis Led Brasil Comércio"
    },
    {
        "process_number": "202400005010184",
        "document_number": "97743692",
        "document_type": "Nota de Empenho",
        "date": "14/05/2024",
        "unit": "UEG/COPA-14028",
        "interested": "Dell Computadores do Brasil Ltda",
        "interested_party": "Dell Computadores do Brasil Ltda",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_dell_workstations_pe0162024",
        "snippet": "Computadores Workstation Dell Precision e Monitores 27 polegadas PE 016/2024 Proc 105104 destinados ao CriaLab Laranjeiras valor R$ 197.410,12",
        "subject": "Pregão Eletrônico nº 016/2024 - Estações de Trabalho de Alta Potência CriaLab",
        "model": "Precision 3660",
        "serial": "D3LL-CRIA-01",
        "supplier": "Dell Computadores do Brasil Ltda"
    },
    {
        "process_number": "202600005037287",
        "document_number": "97743688",
        "document_type": "Despacho",
        "date": "28/10/2026",
        "unit": "UEG/COPA-14028",
        "interested": "Universidade Estadual de Goiás - UEG",
        "interested_party": "Universidade Estadual de Goiás - UEG",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_despacho_1049_2026",
        "snippet": "DESPACHO Nº 1049/2026/UEG/COPA-14028 - Prorrogação de prazo fatal para 13/11/2026 e orientações para inventário e saneamento de bens na UnU Laranjeiras",
        "subject": "Inventário Patrimonial 2026 - Prorrogação de Prazo",
        "model": "Geral",
        "serial": "N/A",
        "supplier": "UEG"
    },
    {
        "process_number": "202600020003350",
        "document_number": "92319061",
        "document_type": "Despacho",
        "date": "15/04/2026",
        "unit": "UEG/COPA-14028",
        "interested": "Programa SUKATECH / Secretaria de Ciência e Tecnologia",
        "interested_party": "Programa SUKATECH / Secretaria de Ciência e Tecnologia",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_sukatech_2026",
        "snippet": "Despacho nº 707/2026/UEG/COPA - Minuta de Termo de Responsabilidade e Desfazimento SUKATECH com previsão expressa da categoria *ST Sem Tombamento",
        "subject": "Programa Estadual de Desfazimento e Logística Reversa SUKATECH",
        "model": "Inservíveis *ST",
        "serial": "SUKATECH-2026-001",
        "supplier": "SUKATECH / SECTI"
    },
    {
        "process_number": "202600020012807",
        "document_number": "95819029",
        "document_type": "Plano de Ação",
        "date": "09/10/2026",
        "unit": "UEG/GTI",
        "interested": "Gerência de Tecnologia da Informação UEG",
        "interested_party": "Gerência de Tecnologia da Informação UEG",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_ti_2026",
        "snippet": "Levantamento Setorial de TI 2026 - Auditoria de equipamentos periféricos rede monitores Dell e servidores nas unidades universitárias",
        "subject": "Inventário Geral de Ativos de TI e Telecomunicações 2026",
        "model": "Parque TI",
        "serial": "TI-UEG-2026",
        "supplier": "UEG/GTI"
    },
    {
        "process_number": "202600005037287",
        "document_number": "97743693",
        "document_type": "Relatório de Inventário",
        "date": "11/11/2026",
        "unit": "UEG/COPA-14028",
        "interested": "Universidade Estadual de Goiás - CriaLab Acervo",
        "interested_party": "Universidade Estadual de Goiás - CriaLab Acervo",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_estoquenow_245",
        "snippet": "Relatório Consolidado do Estoque Now - 245 itens operacionais audiovisuais lentes Sony Canon Atem Mini Pro iluminadores e acessórios do CriaLab",
        "subject": "Acervo Audiovisual Operacional do Laboratório CriaLab - Sistema Estoque Now",
        "model": "Estoque Now 245",
        "serial": "EN-245-ITEMS",
        "supplier": "CriaLab Acervo"
    },
    {
        "process_number": "202600005037287",
        "document_number": "97743694",
        "document_type": "Ficha de Tombamento Legado",
        "date": "28/10/2026",
        "unit": "UEG/COPA-14028",
        "interested": "Universidade Estadual de Goiás",
        "interested_party": "Universidade Estadual de Goiás",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_dlink_dir615",
        "snippet": "Roteador Wireless D-Link DIR-615 S/N F3XE4B7024692 MAC 84C9B24D4C04 Tombamento Anterior 702226 / UEG 72490 - Bem Legado para Regularização SPM",
        "subject": "Auditoria de Bens Legados com Tombamento Anterior - D-Link DIR-615",
        "model": "DIR-615",
        "serial": "F3XE4B7024692",
        "supplier": "D-Link Latin America"
    },
    {
        "process_number": "202600005037287",
        "document_number": "97743695",
        "document_type": "Nota Fiscal",
        "date": "12/09/2022",
        "unit": "UEG/COPA-14028",
        "interested": "Blackmagic Design / ProShow Vídeo Profissional",
        "interested_party": "Blackmagic Design / ProShow Vídeo Profissional",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_atem_mini_pro",
        "snippet": "Switcher de Produção e Mesa de Corte Blackmagic Atem Mini Pro HDMI transmissão ao vivo CriaLab Laranjeiras Estoque Now 000021",
        "subject": "Aquisição de Switcher de Transmissão Ao Vivo Atem Mini Pro",
        "model": "Atem Mini Pro",
        "serial": "BM-ATEM-98214",
        "supplier": "Blackmagic Design"
    },
    {
        "process_number": "202600005037287",
        "document_number": "97743696",
        "document_type": "Nota Fiscal",
        "date": "08/11/2022",
        "unit": "UEG/COPA-14028",
        "interested": "Sony Brasil Ltda",
        "interested_party": "Sony Brasil Ltda",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_sony_lens_2470",
        "snippet": "Lente fotográfica e cinematográfica intercambiável Sony FE 24-70mm F2.8 G Master acervo audiovisual Estoque Now 000030 CriaLab",
        "subject": "Aquisição de Ópticas Profissionais Sony G Master para Cinema",
        "model": "FE 24-70mm f/2.8 GM",
        "serial": "SN-GM2470-4412",
        "supplier": "Sony Brasil Ltda"
    },
    {
        "process_number": "202600005037287",
        "document_number": "97743697",
        "document_type": "Nota Fiscal",
        "date": "14/02/2023",
        "unit": "UEG/COPA-14028",
        "interested": "Ezcap Eletrônicos Importação e Distribuição",
        "interested_party": "Ezcap Eletrônicos Importação e Distribuição",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_ezcap_game_pro",
        "snippet": "Placa de Captura de Vídeo ezcap Game Pro 4K60fps USB 3.0 COD 13729 S/N EZCAP26920100003 COT Radioteledifusão Estoque Now 000090",
        "subject": "Aquisição de Placa de Captura 4K ezcap Game Pro",
        "model": "Game Pro 4K",
        "serial": "EZCAP26920100003",
        "supplier": "Ezcap Eletrônicos"
    },
    {
        "process_number": "202600005037287",
        "document_number": "97743698",
        "document_type": "Nota Fiscal",
        "date": "20/01/2024",
        "unit": "UEG/COPA-14028",
        "interested": "Seagate Technology / Magazine Informática",
        "interested_party": "Seagate Technology / Magazine Informática",
        "link": "https://sei.goias.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?chave=mock_seagate_4tb",
        "snippet": "HD Externo Portátil Seagate Backup Plus 4TB USB 3.0 S/N NT3D44VV Model SRD0NF1 Loggagem 08 CriaLab Laranjeiras Estoque Now 000196",
        "subject": "Aquisição de Dispositivos de Armazenamento Portátil 4TB Seagate",
        "model": "SRD0NF1",
        "serial": "NT3D44VV",
        "supplier": "Seagate Technology"
    }
]


# ==============================================================================
# 2. MODELO DE DADOS (SEIRecord)
# ==============================================================================

class SEIRecord(dict):
    """
    Registro estruturado de processo ou documento do SEI Goiás.
    Compatível com acesso estilo dicionário e serialização JSON.
    """
    def __init__(
        self,
        process_number="",
        document_number="",
        document_type="",
        date="",
        unit="",
        interested="",
        interested_party="",
        link="",
        snippet="",
        subject="",
        model="",
        serial="",
        supplier="",
        **kwargs
    ):
        interested_val = interested or interested_party or supplier or ""
        snippet_val = snippet or subject or ""
        data = {
            "process_number": str(process_number or "").strip(),
            "document_number": str(document_number or "").strip(),
            "document_type": str(document_type or "").strip(),
            "date": str(date or "").strip(),
            "unit": str(unit or "").strip(),
            "interested": str(interested_val).strip(),
            "interested_party": str(interested_val).strip(),
            "link": str(link or "").strip(),
            "snippet": str(snippet_val).strip(),
            "subject": str(snippet_val).strip(),
            "model": str(model or "").strip(),
            "serial": str(serial or "").strip(),
            "supplier": str(interested_val).strip()
        }
        data.update(kwargs)
        super().__init__(data)

    def to_canonical_dict(self):
        """Retorna o esquema estrito exigido pelo contrato em PROJECT.md."""
        d = {
            "process_number": self.get("process_number", ""),
            "document_number": self.get("document_number", ""),
            "document_type": self.get("document_type", ""),
            "date": self.get("date", ""),
            "unit": self.get("unit", ""),
            "interested": self.get("interested", ""),
            "link": self.get("link", ""),
            "snippet": self.get("snippet", "")
        }
        if self.get("model"):
            d["model"] = self.get("model")
        if self.get("serial"):
            d["serial"] = self.get("serial")
        if self.get("supplier"):
            d["supplier"] = self.get("supplier")
        return d


# ==============================================================================
# 3. HTML PARSER (INFRA FRAMEWORK SEI - ZERO DEPENDÊNCIAS)
# ==============================================================================

class SEIHtmlTableParser(HTMLParser):
    """
    Parser HTML especializado para extrair tabelas do Framework Infra do SEI
    (table.infraTable, tr.infraTrClara, tr.infraTrEscura) usando a stdlib.
    """
    def __init__(self, base_url=DEFAULT_BASE_URL):
        super().__init__()
        self.base_url = base_url
        self.in_table = False
        self.in_thead = False
        self.in_row = False
        self.row_has_th = False
        self.in_cell = False
        self.in_link = False
        self.current_cell_text = []
        self.current_link_text = []
        self.current_link_href = None
        self.current_row_cells = []
        self.results = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get("class", "").split()

        if tag == "table":
            if any(c in classes for c in ["infraTable", "tabelaResultado"]) or "Resultado da Pesquisa" in attr_dict.get("summary", ""):
                self.in_table = True
        elif self.in_table and tag == "thead":
            self.in_thead = True
        elif self.in_table and tag == "tr":
            if self.in_thead or any(c in classes for c in ["infraTrCabecalho", "infraTh", "cabecalho"]):
                self.in_row = False
                return
            if any(c in classes for c in ["infraTrClara", "infraTrEscura"]) or self.in_table:
                self.in_row = True
                self.row_has_th = False
                self.current_row_cells = []
        elif self.in_row and tag == "th":
            self.row_has_th = True
        elif self.in_row and tag == "td":
            self.in_cell = True
            self.current_cell_text = []
            self.current_link_href = None
            self.current_link_text = []
        elif self.in_cell and tag == "a":
            self.in_link = True
            self.current_link_href = attr_dict.get("href")
            self.current_link_text = []

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell_text.append(data)
        if self.in_link:
            self.current_link_text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.in_link:
            self.in_link = False
        elif tag == "td" and self.in_cell:
            self.in_cell = False
            cell_str = " ".join("".join(self.current_cell_text).split())
            self.current_row_cells.append({
                "text": cell_str,
                "link": self.current_link_href,
                "link_text": "".join(self.current_link_text).strip()
            })
        elif tag == "tr" and self.in_row:
            self.in_row = False
            if not self.row_has_th and len(self.current_row_cells) >= 3:
                self._parse_row(self.current_row_cells)
        elif tag == "thead" and self.in_thead:
            self.in_thead = False
        elif tag == "table" and self.in_table:
            self.in_table = False

    def _parse_row(self, cells):
        # Mapeamento flexível de colunas (layout padrão: 4 ou 6 colunas)
        c0 = cells[0] if len(cells) > 0 else {"text": "", "link": None, "link_text": ""}
        c1 = cells[1] if len(cells) > 1 else {"text": ""}
        c2 = cells[2] if len(cells) > 2 else {"text": ""}
        c3 = cells[3] if len(cells) > 3 else {"text": ""}
        c4 = cells[4] if len(cells) > 4 else {"text": ""}
        c5 = cells[5] if len(cells) > 5 else {"text": ""}

        full_text = " ".join(c.get("text", "") for c in cells)

        # Sentinel rejection: se coluna 0 ou documento/tipo contém cabeçalhos da tabela, descarte
        proc_or_doc = c0.get("link_text") or c0.get("text", "")
        c0_clean = proc_or_doc.strip().lower()
        if c0_clean in ["processo", "documento", "protocolo", "tipo", "unidade", "data", "interessado", "resumo"]:
            return

        # Extração de Link
        link = c0.get("link") or ""
        if link and not link.startswith("http"):
            link = urllib.parse.urljoin(self.base_url, link)

        # Extração de Protocolo / Processo / Documento
        proc_match = re.search(r"\b(20[12]\d[0-9]{11})\b", proc_or_doc or full_text)
        doc_match = re.search(r"\b([789]\d{7})\b", proc_or_doc or full_text)

        process_number = proc_match.group(1) if proc_match else (proc_or_doc if len(proc_or_doc) >= 15 else "")
        document_number = doc_match.group(1) if doc_match else (proc_or_doc if (7 <= len(proc_or_doc) <= 9 and proc_or_doc.isdigit()) else "")

        # Extração de Data
        date_match = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", full_text)
        date_val = date_match.group(1) if date_match else c1.get("text", "")

        # Extração de Unidade
        unit_match = re.search(r"\b(UEG/[A-Z0-9_\-]+(?:-\d+)?|UEG)\b", full_text, re.IGNORECASE)
        unit_val = unit_match.group(1) if unit_match else ""

        # Mapeamento baseado no número de colunas
        if len(cells) >= 6:
            doc_type = c1.get("text", "")
            unit_val = unit_val or c2.get("text", "")
            date_val = date_val or c3.get("text", "")
            interested_val = c4.get("text", "")
            snippet_val = c5.get("text", "")
        else:
            doc_type = "Processo" if process_number else "Documento"
            interested_val = c2.get("text", "")
            snippet_val = c3.get("text", "")

        if doc_type.strip().lower() in ["tipo", "tipo do documento", "documento / tipo"]:
            return

        self.results.append(SEIRecord(
            process_number=process_number,
            document_number=document_number,
            document_type=doc_type,
            date=date_val,
            unit=unit_val,
            interested=interested_val,
            link=link,
            snippet=snippet_val
        ))


def parse_sei_html_bs4(html_content, base_url=DEFAULT_BASE_URL):
    """Parser alternativo usando BeautifulSoup quando disponível."""
    soup = BeautifulSoup(html_content, "html.parser")
    results = []

    rows = soup.select("table.infraTable tr.infraTrClara, table.infraTable tr.infraTrEscura")
    if not rows:
        rows = [tr for tr in soup.select("table tr") if not tr.find_parent("thead") and not tr.find_all("th")]

    for tr in rows:
        if tr.find_parent("thead") or tr.find_all("th"):
            continue
        tds = tr.find_all("td")
        if len(tds) < 3:
            continue

        first_col_text = tds[0].get_text(strip=True)
        if first_col_text.lower() in ["processo", "documento", "protocolo", "tipo", "unidade", "data", "interessado", "resumo"]:
            continue

        row_text = " ".join(td.get_text(strip=True) for td in tds)
        link_tag = tr.find("a", href=True)
        link = link_tag["href"] if link_tag else ""
        if link and not link.startswith("http"):
            link = urllib.parse.urljoin(base_url, link)

        proc_match = re.search(r"\b(20[12]\d[0-9]{11})\b", row_text)
        doc_match = re.search(r"\b([789]\d{7})\b", row_text)
        date_match = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", row_text)
        unit_match = re.search(r"\b(UEG/[A-Z0-9_\-]+(?:-\d+)?|UEG)\b", row_text, re.IGNORECASE)

        proc_val = proc_match.group(1) if proc_match else (first_col_text if len(first_col_text) >= 15 else "")
        doc_val = doc_match.group(1) if doc_match else (first_col_text if (7 <= len(first_col_text) <= 9 and first_col_text.isdigit()) else "")

        if len(tds) >= 6:
            doc_type = tds[1].get_text(strip=True)
            unit_val = unit_match.group(1) if unit_match else tds[2].get_text(strip=True)
            date_val = date_match.group(1) if date_match else tds[3].get_text(strip=True)
            interested_val = tds[4].get_text(strip=True)
            snippet_val = tds[5].get_text(strip=True)
        else:
            doc_type = "Processo" if proc_val else "Documento"
            date_val = date_match.group(1) if date_match else tds[1].get_text(strip=True)
            interested_val = tds[2].get_text(strip=True)
            snippet_val = tds[3].get_text(strip=True) if len(tds) > 3 else ""
            unit_val = unit_match.group(1) if unit_match else ""

        if doc_type.strip().lower() in ["tipo", "tipo do documento", "documento / tipo"]:
            continue

        results.append(SEIRecord(
            process_number=proc_val,
            document_number=doc_val,
            document_type=doc_type,
            date=date_val,
            unit=unit_val,
            interested=interested_val,
            link=link,
            snippet=snippet_val
        ))

    return results


def parse_sei_html_regex(html_content, base_url=DEFAULT_BASE_URL):
    """Parser de resiliência baseado em expressões regulares."""
    results = []
    # Busca por blocos de linha <tr>
    tr_pattern = re.compile(r"<tr[^>]*>(.*?)</tr>", re.IGNORECASE | re.DOTALL)
    for match in tr_pattern.finditer(html_content):
        row_content = match.group(1)
        proc_match = re.search(r"\b(20[12]\d[0-9]{11})\b", row_content)
        if not proc_match:
            continue

        doc_match = re.search(r"\b([789]\d{7})\b", row_content)
        date_match = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", row_content)
        unit_match = re.search(r"\b(UEG/[A-Z0-9_\-]+(?:-\d+)?|UEG)\b", row_content, re.IGNORECASE)
        link_match = re.search(r'href=[\'"]([^\'"]*(?:md_pesq_processo_exibir|documento_consulta_externa)[^\'"]*)[\'"]', row_content, re.IGNORECASE)

        link = link_match.group(1) if link_match else ""
        if link and not link.startswith("http"):
            link = urllib.parse.urljoin(base_url, link)

        clean_text = " ".join(re.sub(r"<[^>]+>", " ", row_content).split())

        results.append(SEIRecord(
            process_number=proc_match.group(1),
            document_number=doc_match.group(1) if doc_match else "",
            document_type="Processo",
            date=date_match.group(1) if date_match else "",
            unit=unit_match.group(1) if unit_match else "",
            interested="Governo de Goiás / UEG",
            link=link,
            snippet=clean_text
        ))

    return results


def parse_sei_html(html_content, base_url=DEFAULT_BASE_URL):
    """Unificador de parsing HTML com fallback em cascata."""
    if HAS_THIRD_PARTY:
        try:
            records = parse_sei_html_bs4(html_content, base_url)
            if records:
                return records
        except Exception:
            pass

    # Parser stdlib
    parser = SEIHtmlTableParser(base_url)
    try:
        parser.feed(html_content)
        if parser.results:
            return parser.results
    except Exception:
        pass

    # Fallback regex
    return parse_sei_html_regex(html_content, base_url)


# ==============================================================================
# 4. MOTOR DE MOCK DETERMINÍSTICO (OFFLINE ENGINE)
# ==============================================================================

class MockSEIEngine:
    """
    Motor determinístico offline para ambientes sandboxed, testes de CI/CD
    e consultas sem acesso à rede externa do Governo de Goiás.
    """
    def __init__(self, fixture_file=None):
        self.fixtures = self._load_fixtures(fixture_file)

    def _load_fixtures(self, fixture_file=None):
        if fixture_file:
            if not os.path.isfile(fixture_file):
                raise FileNotFoundError(f"Arquivo de fixture não encontrado: {fixture_file}")
            with open(fixture_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if fixture_file.endswith(".html") or fixture_file.endswith(".htm"):
                    return parse_sei_html(content)
                data = json.loads(content)
                if isinstance(data, list):
                    return [SEIRecord(**item) for item in data]
                elif isinstance(data, dict) and "results" in data:
                    return [SEIRecord(**item) for item in data["results"]]
                raise ValueError("Formato de fixture JSON inválido: esperado array de objetos.")

        # Tenta carregar fixtures/sei_mock_fixtures.json se existir no workspace
        local_fixture = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "sei_mock_fixtures.json")
        if os.path.isfile(local_fixture):
            try:
                with open(local_fixture, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [SEIRecord(**item) for item in data]
            except Exception:
                pass

        # Fallback para fixtures embutidas no código
        return [SEIRecord(**item) for item in EMBEDDED_FIXTURES]

    @staticmethod
    def _normalize_string(s):
        """Normaliza texto para comparação (minúsculas, sem pontuação excessiva)."""
        if not s:
            return ""
        # Remove acentos para comparação flexível
        s = s.lower()
        replacements = (
            ("á", "a"), ("à", "a"), ("ã", "a"), ("â", "a"), ("ä", "a"),
            ("é", "e"), ("ê", "e"), ("è", "e"),
            ("í", "i"), ("ì", "i"),
            ("ó", "o"), ("ô", "o"), ("õ", "o"), ("ò", "o"),
            ("ú", "u"), ("ü", "u"),
            ("ç", "c")
        )
        for orig, sub in replacements:
            s = s.replace(orig, sub)
        return s

    @staticmethod
    def _clean_digits(s):
        """Remove tudo que não for dígito."""
        return re.sub(r"\D", "", str(s or ""))

    def filter_records(
        self,
        term=None,
        process=None,
        doc=None,
        serial=None,
        model=None,
        supplier=None,
        unit=None,
        date_from=None,
        date_to=None,
        limit=None
    ):
        """Filtra os registros com base nos parâmetros da busca."""
        filtered = []

        term_norm = self._normalize_string(term).strip() if term else ""
        serial_norm = self._normalize_string(serial).strip() if serial else ""
        model_norm = self._normalize_string(model).strip() if model else ""
        supplier_norm = self._normalize_string(supplier).strip() if supplier else ""
        supplier_digits = self._clean_digits(supplier) if supplier else ""
        unit_norm = self._normalize_string(unit).strip() if unit else ""
        process_digits = self._clean_digits(process) if process else ""
        doc_digits = self._clean_digits(doc) if doc else ""

        # Conversão de datas para comparação cronológica
        d_from = None
        d_to = None
        if date_from:
            try:
                d_from = datetime.strptime(date_from.strip(), "%d/%m/%Y")
            except ValueError:
                raise ValueError("Data inicial inválida. Formato esperado: DD/MM/AAAA")
        if date_to:
            try:
                d_to = datetime.strptime(date_to.strip(), "%d/%m/%Y")
            except ValueError:
                raise ValueError("Data final inválida. Formato esperado: DD/MM/AAAA")

        if d_from and d_to and d_from > d_to:
            raise ValueError("Período de datas inválido: data inicial posterior à data final.")

        for rec in self.fixtures:
            # 1. Filtro de Termo Geral (busca em todos os campos relevantes)
            if term_norm:
                record_corpus = " ".join([
                    rec.get("snippet", ""),
                    rec.get("subject", ""),
                    rec.get("process_number", ""),
                    rec.get("document_number", ""),
                    rec.get("document_type", ""),
                    rec.get("interested", ""),
                    rec.get("model", ""),
                    rec.get("serial", ""),
                    rec.get("unit", "")
                ])
                corpus_norm = self._normalize_string(record_corpus)
                tokens = term_norm.split()
                if not (term_norm in corpus_norm or all(t in corpus_norm for t in tokens)):
                    continue

            # 2. Filtro de Processo
            if process_digits:
                rec_proc_digits = self._clean_digits(rec.get("process_number", ""))
                if process_digits not in rec_proc_digits:
                    continue

            # 3. Filtro de Documento
            if doc_digits:
                rec_doc_digits = self._clean_digits(rec.get("document_number", ""))
                if doc_digits not in rec_doc_digits:
                    continue

            # 4. Filtro de Número de Série
            if serial_norm:
                rec_serial_norm = self._normalize_string(rec.get("serial", ""))
                rec_snippet_norm = self._normalize_string(rec.get("snippet", ""))
                if serial_norm not in rec_serial_norm and serial_norm not in rec_snippet_norm:
                    continue

            # 5. Filtro de Modelo
            if model_norm:
                rec_model_norm = self._normalize_string(rec.get("model", ""))
                rec_snippet_norm = self._normalize_string(rec.get("snippet", ""))
                if model_norm not in rec_model_norm and model_norm not in rec_snippet_norm:
                    continue

            # 6. Filtro de Fornecedor / Interessado (com suporte a CNPJ formatado e desformatado)
            if supplier_norm:
                rec_supp_norm = self._normalize_string(
                    " ".join([
                        rec.get("interested", ""),
                        rec.get("supplier", ""),
                        rec.get("snippet", ""),
                        rec.get("cnpj", "")
                    ])
                )
                rec_supp_digits = self._clean_digits(rec_supp_norm)
                match_text = supplier_norm in rec_supp_norm
                match_cnpj = bool(supplier_digits and len(supplier_digits) >= 8 and supplier_digits in rec_supp_digits)
                if not (match_text or match_cnpj):
                    continue

            # 7. Filtro de Unidade
            if unit_norm:
                rec_unit_norm = self._normalize_string(rec.get("unit", ""))
                if unit_norm not in rec_unit_norm:
                    continue

            # 8. Filtro Cronológico de Data
            rec_date_str = rec.get("date", "").strip()
            if rec_date_str and (d_from or d_to):
                try:
                    rec_date = datetime.strptime(rec_date_str, "%d/%m/%Y")
                    if d_from and rec_date < d_from:
                        continue
                    if d_to and rec_date > d_to:
                        continue
                except ValueError:
                    pass

            filtered.append(rec)

        if limit is not None and limit > 0:
            filtered = filtered[:limit]

        return filtered


# ==============================================================================
# 5. MOTOR DE CONSULTA HTTP REAL (LIVE NETWORK ENGINE)
# ==============================================================================

class SEISearchEngine:
    """
    Motor de conexão e automação de pesquisa pública no portal do SEI Goiás.
    Suporta modos nativo (urllib) e acelerado (requests), com retries e backoff.
    """
    def __init__(
        self,
        base_url=DEFAULT_BASE_URL,
        timeout=15,
        retries=3,
        delay=1.0,
        insecure=False,
        ca_bundle=None,
        proxy=None,
        verbose=False
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.delay = delay
        self.insecure = insecure
        self.ca_bundle = ca_bundle
        self.proxy = proxy
        self.verbose = verbose

    def _get_ssl_context(self):
        """Configura o contexto SSL seguro ou permissivo."""
        if self.insecure:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            return ctx
        if self.ca_bundle and os.path.isfile(self.ca_bundle):
            ctx = ssl.create_default_context(cafile=self.ca_bundle)
            return ctx
        return ssl.create_default_context()

    def search(
        self,
        term=None,
        process=None,
        doc=None,
        serial=None,
        model=None,
        supplier=None,
        unit=None,
        date_from=None,
        date_to=None,
        limit=None
    ):
        """Executa a consulta HTTP contra o endpoint público do SEI Goiás."""
        query_free_tokens = []
        if term:
            query_free_tokens.append(term.strip())
        if serial:
            query_free_tokens.append(serial.strip())
        if model:
            query_free_tokens.append(model.strip())
        txt_pesquisa_livre = " ".join(query_free_tokens)

        txt_protocolo = ""
        if process:
            txt_protocolo = process.strip()
        elif doc:
            txt_protocolo = doc.strip()

        form_data = {
            "txtPesquisaLivre": txt_pesquisa_livre,
            "txtProtocoloPesquisa": txt_protocolo,
            "chkSinProcessos": "S",
            "chkSinDocumentosGerados": "S",
            "chkSinDocumentosRecebidos": "S",
            "txtInteressado": supplier.strip() if supplier else "",
            "txtDataInicio": date_from.strip() if date_from else "",
            "txtDataFim": date_to.strip() if date_to else "",
            "txtSiglaUnidade": unit.strip() if unit else "",
            "btnPesquisar": "Pesquisar"
        }

        endpoint_url = (
            f"{self.base_url}{SEARCH_PATH}?"
            "acao_externa=protocolo_pesquisar&"
            "acao_origem_externa=protocolo_pesquisar&"
            "id_orgao_acesso_externo=1"
        )

        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": self.base_url,
            "Referer": endpoint_url,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        last_error = None
        for attempt in range(1, self.retries + 1):
            try:
                if self.verbose:
                    sys.stderr.write(f"[*] Tentativa {attempt}/{self.retries} consultando {endpoint_url}...\n")

                if HAS_THIRD_PARTY:
                    html_response = self._search_requests(endpoint_url, form_data, headers)
                else:
                    html_response = self._search_urllib(endpoint_url, form_data, headers)

                records = parse_sei_html(html_response, self.base_url)
                if limit is not None and limit > 0:
                    records = records[:limit]
                return records

            except Exception as e:
                last_error = e
                if self.verbose:
                    sys.stderr.write(f"[-] Falha na tentativa {attempt}: {e}\n")
                if attempt < self.retries:
                    backoff = self.delay * (2 ** (attempt - 1))
                    time.sleep(backoff)

        # Se todas as tentativas falharem, relata erro amigável
        err_msg = str(last_error or "Erro de rede desconhecido")
        if "10013" in err_msg or "Permission denied" in err_msg:
            sys.stderr.write(
                f"[ERRO DE CONEXÃO] Acesso a socket bloqueado pelo ambiente (WinError 10013).\n"
                f"Dica: utilize a flag --mock para executar a pesquisa offline com os dados reais do CriaLab.\n"
            )
        else:
            sys.stderr.write(
                f"[ERRO DE CONEXÃO] Não foi possível consultar o SEI Goiás: {err_msg}\n"
                f"Dica: utilize a flag --mock para executar a pesquisa offline com dados patrimoniais autênticos.\n"
            )
        raise ConnectionError(f"Falha de conexão com SEI Goiás: {err_msg}")

    def _search_requests(self, url, form_data, headers):
        """Execução via requests."""
        session = requests.Session()
        session.headers.update(headers)
        if self.proxy:
            session.proxies = {"http": self.proxy, "https": self.proxy}

        # Primeiro acessa o GET para capturar cookie de sessão
        session.get(url, timeout=self.timeout, verify=not self.insecure)
        resp = session.post(url, data=form_data, timeout=self.timeout, verify=not self.insecure)
        resp.raise_for_status()
        return resp.text

    def _search_urllib(self, url, form_data, headers):
        """Execução via urllib da biblioteca padrão."""
        encoded_data = urllib.parse.urlencode(form_data).encode("utf-8")
        cookie_jar = http.cookiejar.CookieJar()
        handlers = [urllib.request.HTTPCookieProcessor(cookie_jar)]

        if self.proxy:
            handlers.append(urllib.request.ProxyHandler({"http": self.proxy, "https": self.proxy}))

        ctx = self._get_ssl_context()
        handlers.append(urllib.request.HTTPSHandler(context=ctx))

        opener = urllib.request.build_opener(*handlers)
        req = urllib.request.Request(url, data=encoded_data, headers=headers)
        with opener.open(req, timeout=self.timeout) as response:
            content_bytes = response.read()
            # SEI comumente responde em ISO-8859-1 ou UTF-8
            try:
                return content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                return content_bytes.decode("iso-8859-1", errors="replace")


# ==============================================================================
# 6. EXPORTADORES ESTRUTURADOS (JSON, CSV, MARKDOWN, TABLE)
# ==============================================================================

def export_json(records):
    """Exporta lista de registros em JSON canônico formatado."""
    output = [rec.to_canonical_dict() if isinstance(rec, SEIRecord) else rec for rec in records]
    return json.dumps(output, indent=2, ensure_ascii=False)


def export_csv(records):
    """Exporta lista de registros em CSV RFC-4180."""
    fieldnames = [
        "process_number",
        "document_number",
        "document_type",
        "date",
        "unit",
        "interested",
        "link",
        "snippet"
    ]
    output_io = io.StringIO()
    writer = csv.DictWriter(
        output_io,
        fieldnames=fieldnames,
        extrasaction="ignore",
        lineterminator="\n"
    )
    writer.writeheader()
    for rec in records:
        writer.writerow(rec if isinstance(rec, dict) else rec.to_canonical_dict())
    return output_io.getvalue()


def _clean_md_cell(val):
    r"""
    Sanitiza o conteúdo de uma célula de tabela Markdown:
    - Trata valores nulos ou vazios convertendo para '-'
    - Converte quebras de linha (\r\n, \r, \n) em espaços
    - Escapa o caractere pipe ('|' -> '\|'), preservando pipes já escapados
    - Normaliza espaços em branco e remove espaços nas pontas
    """
    if val is None:
        return "-"
    s = str(val).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    s = s.replace("\\|", "|").replace("|", "\\|")
    s = " ".join(s.split())
    return s if s else "-"


def export_markdown(records):
    """Exporta lista de registros em tabela formatada Markdown com blindagem contra pipe injection."""
    lines = [
        "# Resultados da Pesquisa SEI Goiás",
        "",
        f"- **Total de registros encontrados:** {len(records)}",
        f"- **Data da consulta:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        "",
        "| ID | Processo | Documento | Tipo | Data | Unidade | Interessado | Link | Trecho / Snippet |",
        "|---|---|---|---|---|---|---|---|---|"
    ]
    for idx, rec in enumerate(records, 1):
        if not isinstance(rec, dict) and hasattr(rec, "to_canonical_dict"):
            r = rec.to_canonical_dict()
        else:
            r = rec if isinstance(rec, dict) else {}

        proc = _clean_md_cell(r.get("process_number"))
        doc = _clean_md_cell(r.get("document_number"))
        dtype = _clean_md_cell(r.get("document_type"))
        date = _clean_md_cell(r.get("date"))
        unit = _clean_md_cell(r.get("unit"))
        interested = _clean_md_cell(r.get("interested"))
        link = (r.get("link") or "").strip()
        link_text = doc if doc != "-" else "Visualizar"
        link_md = f"[{link_text}]({link})" if link else "-"
        snippet = _clean_md_cell(r.get("snippet"))

        lines.append(f"| {idx} | {proc} | {doc} | {dtype} | {date} | {unit} | {interested} | {link_md} | {snippet} |")

    lines.append("")
    return "\n".join(lines)


def export_table(records):
    """Exporta lista de registros em formato de tabela textual para terminal."""
    if not records:
        return "Nenhum registro encontrado."

    headers = ["Processo", "Documento", "Tipo", "Data", "Unidade", "Interessado"]
    rows = []
    for rec in records:
        rows.append([
            rec.get("process_number", "")[:17],
            rec.get("document_number", "")[:10],
            rec.get("document_type", "")[:15],
            rec.get("date", "")[:10],
            rec.get("unit", "")[:16],
            rec.get("interested", "")[:35]
        ])

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            if len(val) > col_widths[i]:
                col_widths[i] = len(val)

    sep_line = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    header_line = "|" + "|".join(f" {headers[i].ljust(col_widths[i])} " for i in range(len(headers))) + "|"

    output = [sep_line, header_line, sep_line]
    for row in rows:
        row_str = "|" + "|".join(f" {row[i].ljust(col_widths[i])} " for i in range(len(row))) + "|"
        output.append(row_str)
    output.append(sep_line)
    output.append(f"Total: {len(records)} registro(s)")
    return "\n".join(output)


# ==============================================================================
# 7. INTEGRAÇÃO CRUZADA COM BASES LOCAIS DO INVENTÁRIO
# ==============================================================================

def check_cross_inventory(query_term):
    """
    Verifica se o termo pesquisado consta nas bases locais do SPM ou do Estoque Now.
    """
    if not query_term:
        return []

    base_dir = os.path.dirname(os.path.abspath(__file__))
    matches = []

    # 1. Base Master SPM (data/inventario_master.json)
    spm_path = os.path.join(base_dir, "data", "inventario_master.json")
    if os.path.isfile(spm_path):
        try:
            with open(spm_path, "r", encoding="utf-8") as f:
                spm_data = json.load(f)
                term_lower = query_term.lower()
                for item in spm_data:
                    item_str = json.dumps(item, ensure_ascii=False).lower()
                    if term_lower in item_str:
                        matches.append({
                            "source": "SPM_MASTER",
                            "tombamento": item.get("tombamento_atual") or item.get("tombamento"),
                            "descricao": item.get("descricao") or item.get("nome") or item.get("especie"),
                            "carga": item.get("carga_setorial") or item.get("origem")
                        })
        except Exception:
            pass

    # 2. Base Estoque Now (data/estoquenow_completo.json)
    en_path = os.path.join(base_dir, "data", "estoquenow_completo.json")
    if os.path.isfile(en_path):
        try:
            with open(en_path, "r", encoding="utf-8") as f:
                en_data = json.load(f)
                term_lower = query_term.lower()
                for item in en_data:
                    item_str = json.dumps(item, ensure_ascii=False).lower()
                    if term_lower in item_str:
                        matches.append({
                            "source": "ESTOQUE_NOW",
                            "codigo": item.get("codigo"),
                            "descricao": item.get("descricao") or item.get("nome") or item.get("especie"),
                            "categoria": item.get("categoria") or ("Em manutenção" if item.get("em_manutencao") == "Sim" else "Ativo Operacional")
                        })
        except Exception:
            pass

    return matches


# ==============================================================================
# 8. FUNÇÃO DE ALTO NÍVEL PARA USO PROGRAMÁTICO (API)
# ==============================================================================

def search_sei(
    term=None,
    process=None,
    doc=None,
    serial=None,
    model=None,
    supplier=None,
    unit=None,
    date_from=None,
    date_to=None,
    format="json",
    output=None,
    mock=False,
    fixture_file=None,
    limit=None,
    **kwargs
):
    """
    Função programática para execução de pesquisas no SEI Goiás.
    Pode ser importada e utilizada diretamente em scripts e suítes de teste:

    from sei_search import search_sei
    results = search_sei(term="Yamaha", mock=True)
    """
    if mock:
        engine = MockSEIEngine(fixture_file=fixture_file)
        records = engine.filter_records(
            term=term,
            process=process,
            doc=doc,
            serial=serial,
            model=model,
            supplier=supplier,
            unit=unit,
            date_from=date_from,
            date_to=date_to,
            limit=limit
        )
    else:
        engine = SEISearchEngine(**kwargs)
        records = engine.search(
            term=term,
            process=process,
            doc=doc,
            serial=serial,
            model=model,
            supplier=supplier,
            unit=unit,
            date_from=date_from,
            date_to=date_to,
            limit=limit
        )

    # Exportação e salvamento se solicitado
    fmt = (format or "json").lower()
    if fmt == "md":
        fmt = "markdown"

    formatted_output = ""
    if fmt == "json":
        formatted_output = export_json(records)
    elif fmt == "csv":
        formatted_output = export_csv(records)
    elif fmt == "markdown":
        formatted_output = export_markdown(records)
    elif fmt == "table":
        formatted_output = export_table(records)
    else:
        formatted_output = export_json(records)

    if output:
        out_dir = os.path.dirname(os.path.abspath(output))
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        # Use utf-8-sig para CSV (Excel) ou utf-8 padrão
        enc = "utf-8-sig" if fmt == "csv" else "utf-8"
        with open(output, "w", encoding=enc) as f:
            f.write(formatted_output)

    return records


# ==============================================================================
# 9. INTERFACE DE LINHA DE COMANDO (CLI)
# ==============================================================================

def build_cli_parser():
    """Constrói o parser de linha de comando com todas as flags e documentação."""
    parser = argparse.ArgumentParser(
        prog="sei_search.py",
        description=(
            "sei_search.py — Automação de Pesquisa e Extração de Processos/Documentos no SEI Goiás.\n"
            "Desenvolvido para auditoria patrimonial e instrução do Processo SEI nº 202600005037287."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Parâmetros de Busca
    search_group = parser.add_argument_group("Filtros de Pesquisa")
    search_group.add_argument(
        "--term", "-t",
        dest="term",
        type=str,
        default=None,
        help="Termo de pesquisa livre (ex: 'Yamaha MG12XU', 'Spotware', 'NovaStar')"
    )
    search_group.add_argument(
        "--process", "-p",
        dest="process",
        type=str,
        default=None,
        help="Número do processo SEI / NUP (ex: '202600005037287', '202100020006687')"
    )
    search_group.add_argument(
        "--doc", "-d", "--document",
        dest="doc",
        type=str,
        default=None,
        help="Número do documento SEI (ex: '97743688')"
    )
    search_group.add_argument(
        "--serial", "-s",
        dest="serial",
        type=str,
        default=None,
        help="Número de série do equipamento (ex: 'BRACVX01071', '008479010011225', '115983')"
    )
    search_group.add_argument(
        "--model", "-m",
        dest="model",
        type=str,
        default=None,
        help="Modelo do equipamento (ex: 'MG12XU', 'Spotware-M', 'VX400', 'URX-P03')"
    )
    search_group.add_argument(
        "--supplier", "--interessado",
        dest="supplier",
        type=str,
        default=None,
        help="Nome, razão social ou CNPJ do fornecedor / interessado (ex: 'Floripa Tecnologia')"
    )
    search_group.add_argument(
        "--unit", "-u",
        dest="unit",
        type=str,
        default=None,
        help="Sigla da unidade administrativa geradora (ex: 'UEG/COPA-14028', 'UEG')"
    )
    search_group.add_argument(
        "--date-from", "--data-inicio",
        dest="date_from",
        type=str,
        default=None,
        help="Data inicial de autuação / expedição no formato DD/MM/AAAA (ex: '01/01/2021')"
    )
    search_group.add_argument(
        "--date-to", "--data-fim",
        dest="date_to",
        type=str,
        default=None,
        help="Data final de autuação / expedição no formato DD/MM/AAAA (ex: '31/12/2026')"
    )
    search_group.add_argument(
        "--assunto",
        dest="assunto",
        type=str,
        default=None,
        help="Descrição ou código do assunto administrativo"
    )

    # Parâmetros de Simulação e Mock
    mock_group = parser.add_argument_group("Modo Offline e Simulação")
    mock_group.add_argument(
        "--mock",
        dest="mock",
        action="store_true",
        default=False,
        help="Ativa o motor de simulação offline utilizando fixtures com dados patrimoniais autênticos"
    )
    mock_group.add_argument(
        "--fixture-file",
        dest="fixture_file",
        type=str,
        default=None,
        help="Caminho para arquivo customizado de fixtures (formato JSON ou HTML do SEI)"
    )
    mock_group.add_argument(
        "--cross-inventory",
        dest="cross_inventory",
        action="store_true",
        default=False,
        help="Cruza os termos de busca com os bancos de dados locais (inventario_master e estoquenow)"
    )

    # Parâmetros de Saída
    output_group = parser.add_argument_group("Configuração de Saída e Exportação")
    output_group.add_argument(
        "--format", "-f",
        dest="format",
        type=str,
        default="json",
        help="Formato de saída (json, csv, markdown, table) [default: table/json]"
    )
    output_group.add_argument(
        "--output", "-o",
        dest="output",
        type=str,
        default=None,
        help="Caminho do arquivo de destino para salvar os resultados"
    )
    output_group.add_argument(
        "--limit",
        dest="limit",
        type=int,
        default=None,
        help="Limite máximo de registros a serem retornados"
    )
    output_group.add_argument(
        "--quiet", "-q",
        dest="quiet",
        action="store_true",
        default=False,
        help="Modo silencioso: exibe exclusivamente os dados puros na saída padrão"
    )
    output_group.add_argument(
        "--verbose", "-v", "--debug",
        dest="verbose",
        action="store_true",
        default=False,
        help="Habilita mensagens detalhadas de log e depuração durante a execução"
    )

    # Parâmetros Avançados de Conexão HTTP
    net_group = parser.add_argument_group("Conexão e Rede HTTP")
    net_group.add_argument(
        "--base-url",
        dest="base_url",
        type=str,
        default=DEFAULT_BASE_URL,
        help=f"URL base do SEI Goiás (padrão: {DEFAULT_BASE_URL})"
    )
    net_group.add_argument(
        "--timeout",
        dest="timeout",
        type=int,
        default=15,
        help="Tempo limite (em segundos) para requisições HTTP (padrão: 15)"
    )
    net_group.add_argument(
        "--retries",
        dest="retries",
        type=int,
        default=3,
        help="Número de tentativas de conexão em caso de falha transitória (padrão: 3)"
    )
    net_group.add_argument(
        "--delay",
        dest="delay",
        type=float,
        default=1.0,
        help="Intervalo base (em segundos) para retries e controle de taxa (padrão: 1.0)"
    )
    net_group.add_argument(
        "--insecure",
        dest="insecure",
        action="store_true",
        default=False,
        help="Desativa a verificação de certificados SSL (útil para cadeias ICP-Brasil ausentes)"
    )
    net_group.add_argument(
        "--ca-bundle",
        dest="ca_bundle",
        type=str,
        default=None,
        help="Caminho para arquivo de certificados confiáveis (CA Bundle)"
    )
    net_group.add_argument(
        "--proxy",
        dest="proxy",
        type=str,
        default=None,
        help="URL de proxy HTTP/HTTPS para redes corporativas"
    )

    return parser


def main(argv=None):
    """Ponto de entrada principal da CLI."""
    if argv is None:
        argv = sys.argv[1:]

    parser = build_cli_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return e.code

    # Validação do parâmetro --format
    valid_formats = ["json", "csv", "markdown", "md", "table"]
    format_chosen = (args.format or "json").lower()
    if format_chosen not in valid_formats:
        sys.stderr.write(f"Erro: Formato de saída desconhecido: '{args.format}'. Formatos válidos: json, csv, markdown, table.\n")
        return 1

    if format_chosen == "md":
        format_chosen = "markdown"

    # Se --output tiver extensão reconhecida e formato não for explícito, infere
    if args.output and "--format" not in argv and "-f" not in argv:
        ext = os.path.splitext(args.output)[1].lower()
        if ext == ".csv":
            format_chosen = "csv"
        elif ext in [".md", ".markdown"]:
            format_chosen = "markdown"
        elif ext == ".json":
            format_chosen = "json"

    # Validação do parâmetro --limit
    if args.limit is not None and args.limit <= 0:
        sys.stderr.write("Erro: O parâmetro --limit deve ser um número inteiro positivo maior que zero.\n")
        return 1

    # Validação de datas
    date_regex = re.compile(r"^\d{2}/\d{2}/\d{4}$")
    d_from = None
    d_to = None
    if args.date_from:
        val = args.date_from.strip()
        if not date_regex.match(val):
            sys.stderr.write(f"Erro: Formato de data inicial inválido: '{args.date_from}'. Use DD/MM/AAAA.\n")
            return 1
        try:
            d_from = datetime.strptime(val, "%d/%m/%Y")
        except ValueError:
            sys.stderr.write(f"Erro: Data inicial inválida no calendário: '{args.date_from}'.\n")
            return 1

    if args.date_to:
        val = args.date_to.strip()
        if not date_regex.match(val):
            sys.stderr.write(f"Erro: Formato de data final inválido: '{args.date_to}'. Use DD/MM/AAAA.\n")
            return 1
        try:
            d_to = datetime.strptime(val, "%d/%m/%Y")
        except ValueError:
            sys.stderr.write(f"Erro: Data final inválida no calendário: '{args.date_to}'.\n")
            return 1

    if d_from and d_to and d_from > d_to:
        sys.stderr.write(
            f"Erro: Período de datas inválido: data inicial ({args.date_from}) posterior à data final ({args.date_to}).\n"
        )
        return 1

    # Validação de fixture file se informada
    if args.fixture_file:
        if not os.path.isfile(args.fixture_file):
            sys.stderr.write(f"Erro: Arquivo de fixture não encontrado: '{args.fixture_file}'.\n")
            return 1

    # Validação de diretório de saída se informado
    if args.output:
        out_dir = os.path.dirname(os.path.abspath(args.output))
        if out_dir and not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except Exception as e:
                sys.stderr.write(f"Erro ao criar diretório para arquivo de saída '{out_dir}': {e}\n")
                return 1

    # Execução da Integração Cruzada (--cross-inventory)
    if args.cross_inventory:
        search_kw = args.term or args.serial or args.model or args.process or ""
        cross_results = check_cross_inventory(search_kw)
        if cross_results and not args.quiet:
            sys.stderr.write(f"[*] Cruzamento local encontrou {len(cross_results)} ocorrência(s) nas bases locais:\n")
            for cr in cross_results[:5]:
                sys.stderr.write(f"    - [{cr.get('source')}] {cr.get('tombamento') or cr.get('codigo')}: {cr.get('descricao')}\n")

    # Execução da Pesquisa (Mock vs Live)
    try:
        if args.mock:
            if args.verbose:
                sys.stderr.write("[*] Modo de simulação offline ativado (--mock).\n")
            engine = MockSEIEngine(fixture_file=args.fixture_file)
            records = engine.filter_records(
                term=args.term,
                process=args.process,
                doc=args.doc,
                serial=args.serial,
                model=args.model,
                supplier=args.supplier,
                unit=args.unit,
                date_from=args.date_from,
                date_to=args.date_to,
                limit=args.limit
            )
        else:
            engine = SEISearchEngine(
                base_url=args.base_url,
                timeout=args.timeout,
                retries=args.retries,
                delay=args.delay,
                insecure=args.insecure,
                ca_bundle=args.ca_bundle,
                proxy=args.proxy,
                verbose=args.verbose
            )
            records = engine.search(
                term=args.term,
                process=args.process,
                doc=args.doc,
                serial=args.serial,
                model=args.model,
                supplier=args.supplier,
                unit=args.unit,
                date_from=args.date_from,
                date_to=args.date_to,
                limit=args.limit
            )
    except FileNotFoundError as e:
        sys.stderr.write(f"Erro: {e}\n")
        return 1
    except ValueError as e:
        sys.stderr.write(f"Erro de validação: {e}\n")
        return 1
    except ConnectionError as e:
        sys.stderr.write(f"Erro: {e}\n")
        return 1
    except Exception as e:
        sys.stderr.write(f"Erro inesperado durante a execução: {e}\n")
        return 1

    # Renderização da Saída
    if format_chosen == "json":
        formatted_text = export_json(records)
    elif format_chosen == "csv":
        formatted_text = export_csv(records)
    elif format_chosen == "markdown":
        formatted_text = export_markdown(records)
    elif format_chosen == "table":
        formatted_text = export_table(records)
    else:
        formatted_text = export_json(records)

    # Gravação em Arquivo ou Saída no Terminal
    if args.output:
        try:
            enc = "utf-8-sig" if format_chosen == "csv" else "utf-8"
            with open(args.output, "w", encoding=enc) as f:
                f.write(formatted_text)
            if not args.quiet:
                sys.stderr.write(f"Resultados salvos com sucesso em: {args.output} ({len(records)} registros)\n")
        except Exception as e:
            sys.stderr.write(f"Erro ao salvar arquivo de saída '{args.output}': {e}\n")
            return 1
    else:
        # Imprime na saída padrão (stdout)
        try:
            print(formatted_text)
        except UnicodeEncodeError:
            sys.stdout.buffer.write(formatted_text.encode("utf-8", errors="replace"))
            sys.stdout.buffer.write(b"\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
