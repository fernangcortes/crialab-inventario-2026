#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_sei_search.py — Suíte de Testes E2E e Integração SEI Goiás

Cobre a automação de pesquisa patrimonial (sei_search.py) e a conformidade
documental do Guia de Instrução Patrimonial (GUIA_INSTRUCAO_PATRIMONIAL_SEI.md)
no âmbito do Processo SEI nº 202600005037287 (CriaLab & Radioteledifusão UEG).

Estrutura dos Níveis de Teste:
  - Tier 1: Feature Coverage (>=5 testes por feature: term, process, serial, model,
            supplier, unit, format, output, mock)
  - Tier 2: Boundary & Corner Cases (termos vazios, acentuação UTF-8, símbolos,
            inexistentes, datas inválidas, formatos desconhecidos, caminhos inválidos)
  - Tier 3: Cross-Feature Combinations (combinações de multi-flags, filtros AND, limits)
  - Tier 4: Real-World Scenarios & Validação do Guia Documental SEI (Servidor Floripa,
            Yamaha MG12XU, NovaStar VX400, Sony URX-P03, Estoque Now, 7 tipos documentais)

Framework: unittest (Biblioteca padrão Python — Zero Dependências Externas)
Execução: python test_sei_search.py
"""

import csv
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import sei_search

PROJECT_ROOT = Path(__file__).resolve().parent
SEI_SCRIPT = PROJECT_ROOT / "sei_search.py"
GUIA_DOC = PROJECT_ROOT / "GUIA_INSTRUCAO_PATRIMONIAL_SEI.md"
FIXTURES_FILE = PROJECT_ROOT / "fixtures" / "sei_mock_fixtures.json"


def run_cli(args, timeout=15):
    """
    Executa o script sei_search.py via subprocesso isolado.
    Retorna o objeto CompletedProcess resultante.
    """
    cmd = [sys.executable, str(SEI_SCRIPT)] + list(args)
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        cwd=PROJECT_ROOT,
    )
    return proc


def extract_json_results(output_text):
    """
    Converte o output textual JSON para uma lista de registros.
    Suporta tanto lista de objetos na raiz quanto dict com chave 'results'.
    """
    data = json.loads(output_text.strip())
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        if "results" in data and isinstance(data["results"], list):
            return data["results"]
        return [data]
    return []


# ==============================================================================
# TIER 1: FEATURE COVERAGE (>=5 Testes por Feature)
# ==============================================================================

class TestTier1FeatureCoverage(unittest.TestCase):
    """Tier 1: Cobertura exaustiva das flags individuais do CLI."""

    @classmethod
    def setUpClass(cls):
        if not SEI_SCRIPT.exists():
            raise unittest.SkipTest("sei_search.py ainda não criado na raiz do projeto")

    # --------------------------------------------------------------------------
    # Feature 1: --term / -t (5 testes)
    # --------------------------------------------------------------------------

    def test_tier1_term_exact_keyword(self):
        """F-TERM-01: Pesquisa por palavra-chave exata 'Spotware'."""
        proc = run_cli(["--mock", "--term", "Spotware", "--format", "json"])
        self.assertEqual(proc.returncode, 0, f"Falha na execução: {proc.stderr}")
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1, "Deveria encontrar ao menos 1 registro para 'Spotware'")
        self.assertTrue(
            any("Spotware" in (r.get("snippet", "") + r.get("subject", "") + r.get("model", "")) for r in records),
            "Nenhum registro retornado contém a palavra 'Spotware'"
        )

    def test_tier1_term_multiword_keyword(self):
        """F-TERM-02: Pesquisa por termo composto 'Yamaha MG12XU'."""
        proc = run_cli(["--mock", "--term", "Yamaha MG12XU", "--format", "json"])
        self.assertEqual(proc.returncode, 0, f"Falha na execução: {proc.stderr}")
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(
            any("MG12XU" in (r.get("snippet", "") + r.get("model", "")) for r in records)
        )

    def test_tier1_term_short_flag(self):
        """F-TERM-03: Operação correta da flag curta '-t' com 'NovaStar'."""
        proc = run_cli(["--mock", "-t", "NovaStar", "--format", "json"])
        self.assertEqual(proc.returncode, 0, f"Falha na execução: {proc.stderr}")
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("NovaStar" in str(r) for r in records))

    def test_tier1_term_snippet_matching(self):
        """F-TERM-04: Recuperação de termos específicos contidos no snippet."""
        proc = run_cli(["--mock", "--term", "008479010011225", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertIn("008479010011225", str(records[0]))

    def test_tier1_term_subject_matching(self):
        """F-TERM-05: Recuperação de termos presentes no assunto administrativo."""
        proc = run_cli(["--mock", "--term", "SUKATECH", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("SUKATECH" in str(r) for r in records))

    # --------------------------------------------------------------------------
    # Feature 2: --process / -p (5 testes)
    # --------------------------------------------------------------------------

    def test_tier1_process_standard_nup(self):
        """F-PROC-01: Pesquisa por processo SEI NUP padrão 202100020006687."""
        proc = run_cli(["--mock", "--process", "202100020006687", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        for r in records:
            self.assertEqual(r.get("process_number"), "202100020006687")

    def test_tier1_process_short_flag(self):
        """F-PROC-02: Operação da flag curta '-p' com processo do inventário 202600005037287."""
        proc = run_cli(["--mock", "-p", "202600005037287", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        for r in records:
            self.assertEqual(r.get("process_number"), "202600005037287")

    def test_tier1_process_it_inventory(self):
        """F-PROC-03: Localização de processo de inventário de TI 202600020012807."""
        proc = run_cli(["--mock", "--process", "202600020012807", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].get("process_number"), "202600020012807")

    def test_tier1_process_sukatech_disposal(self):
        """F-PROC-04: Localização do processo de desfazimento 202600020003350."""
        proc = run_cli(["--mock", "--process", "202600020003350", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].get("process_number"), "202600020003350")

    def test_tier1_process_workstations(self):
        """F-PROC-05: Localização do processo de compras de TI 202400005010184."""
        proc = run_cli(["--mock", "--process", "202400005010184", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].get("process_number"), "202400005010184")

    # --------------------------------------------------------------------------
    # Feature 3: --serial / -s (5 testes)
    # --------------------------------------------------------------------------

    def test_tier1_serial_spotware(self):
        """F-SER-01: Pesquisa por serial do Servidor Floripa Spotware-M."""
        proc = run_cli(["--mock", "--serial", "008479010011225", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("008479010011225" in str(r) for r in records))

    def test_tier1_serial_yamaha(self):
        """F-SER-02: Pesquisa por serial da Mesa Yamaha MG12XU (BRACVX01071)."""
        proc = run_cli(["--mock", "--serial", "BRACVX01071", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("BRACVX01071" in str(r) for r in records))

    def test_tier1_serial_novastar(self):
        """F-SER-03: Pesquisa por serial do NovaStar VX400 (21MB44422N0A10002120)."""
        proc = run_cli(["--mock", "--serial", "21MB44422N0A10002120", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("21MB44422N0A10002120" in str(r) for r in records))

    def test_tier1_serial_sony(self):
        """F-SER-04: Pesquisa por serial do Receptor Sony URX-P03 (115983)."""
        proc = run_cli(["--mock", "--serial", "115983", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("115983" in str(r) for r in records))

    def test_tier1_serial_short_flag(self):
        """F-SER-05: Operação da flag curta '-s' com serial do D-Link (F3XE4B7024692)."""
        proc = run_cli(["--mock", "-s", "F3XE4B7024692", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("F3XE4B7024692" in str(r) for r in records))

    # --------------------------------------------------------------------------
    # Feature 4: --model / -m (5 testes)
    # --------------------------------------------------------------------------

    def test_tier1_model_spotware(self):
        """F-MOD-01: Pesquisa por modelo 'Spotware-M'."""
        proc = run_cli(["--mock", "--model", "Spotware-M", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("Spotware-M" in str(r) for r in records))

    def test_tier1_model_yamaha(self):
        """F-MOD-02: Pesquisa por modelo 'MG12XU'."""
        proc = run_cli(["--mock", "--model", "MG12XU", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("MG12XU" in str(r) for r in records))

    def test_tier1_model_novastar(self):
        """F-MOD-03: Pesquisa por modelo 'VX400'."""
        proc = run_cli(["--mock", "--model", "VX400", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("VX400" in str(r) for r in records))

    def test_tier1_model_sony(self):
        """F-MOD-04: Pesquisa por modelo 'URX-P03'."""
        proc = run_cli(["--mock", "--model", "URX-P03", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("URX-P03" in str(r) for r in records))

    def test_tier1_model_short_flag(self):
        """F-MOD-05: Operação da flag curta '-m' com modelo 'DIR-615'."""
        proc = run_cli(["--mock", "-m", "DIR-615", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("DIR-615" in str(r) for r in records))

    # --------------------------------------------------------------------------
    # Feature 5: --supplier (5 testes)
    # --------------------------------------------------------------------------

    def test_tier1_supplier_floripa_name(self):
        """F-SUP-01: Pesquisa por fornecedor 'Floripa Tecnologia'."""
        proc = run_cli(["--mock", "--supplier", "Floripa Tecnologia", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("Floripa" in str(r) for r in records))

    def test_tier1_supplier_full_corporate(self):
        """F-SUP-02: Pesquisa por razão social completa com 'Ind e Com LTDA'."""
        proc = run_cli(["--mock", "--supplier", "Floripa Tecnologia Ind e Com LTDA", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)

    def test_tier1_supplier_cnpj_formatted(self):
        """F-SUP-03: Pesquisa por CNPJ formatado 01.151.131/0001-32."""
        proc = run_cli(["--mock", "--supplier", "01.151.131/0001-32", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1, "Deve encontrar a Floripa Tecnologia pelo CNPJ formatado")
        self.assertTrue(any("Floripa" in str(r) for r in records))

    def test_tier1_supplier_cnpj_unformatted(self):
        """F-SUP-04: Pesquisa por CNPJ numérico desformatado '01151131000132'."""
        proc = run_cli(["--mock", "--supplier", "01151131000132", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1, "Deve encontrar a Floripa Tecnologia pelo CNPJ desformatado")
        self.assertTrue(any("Floripa" in str(r) for r in records))

    def test_tier1_supplier_audio_video(self):
        """F-SUP-05: Pesquisa por fornecedor do setor audiovisual 'Sony Brasil'."""
        proc = run_cli(["--mock", "--supplier", "Sony Brasil", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(any("Sony" in str(r) for r in records))

    # --------------------------------------------------------------------------
    # Feature 6: --unit / -u (5 testes)
    # --------------------------------------------------------------------------

    def test_tier1_unit_copa_code(self):
        """F-UNI-01: Pesquisa por unidade com código SEI 'UEG/COPA-14028'."""
        proc = run_cli(["--mock", "--unit", "UEG/COPA-14028", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        for r in records:
            self.assertIn("COPA", r.get("unit", ""))

    def test_tier1_unit_ueg_prefix(self):
        """F-UNI-02: Pesquisa por prefixo amplo 'UEG'."""
        proc = run_cli(["--mock", "--unit", "UEG", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)

    def test_tier1_unit_copa_keyword(self):
        """F-UNI-03: Pesquisa por sigla setorial 'COPA'."""
        proc = run_cli(["--mock", "--unit", "COPA", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)

    def test_tier1_unit_short_flag(self):
        """F-UNI-04: Operação da flag curta '-u' com 'COT' (Radioteledifusão)."""
        proc = run_cli(["--mock", "-u", "COT", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)

    def test_tier1_unit_campus_scope(self):
        """F-UNI-05: Pesquisa por unidade técnica 'GTI'."""
        proc = run_cli(["--mock", "--unit", "GTI", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)

    # --------------------------------------------------------------------------
    # Feature 7: --format [json, csv, markdown, table] (5 testes)
    # --------------------------------------------------------------------------

    def test_tier1_format_json_validity(self):
        """F-FMT-01: Validação de saída canônica em JSON parseável."""
        proc = run_cli(["--mock", "--term", "Spotware", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        try:
            data = json.loads(proc.stdout)
            self.assertTrue(isinstance(data, (list, dict)))
        except json.JSONDecodeError as e:
            self.fail(f"Saída JSON inválida: {e}")

    def test_tier1_format_csv_validity(self):
        """F-FMT-02: Validação de saída CSV RFC-4180 com cabeçalho."""
        proc = run_cli(["--mock", "--term", "Spotware", "--format", "csv"])
        self.assertEqual(proc.returncode, 0)
        lines = [line.strip() for line in proc.stdout.strip().splitlines() if line.strip()]
        self.assertGreaterEqual(len(lines), 2, "CSV deve ter cabeçalho e ao menos uma linha de dados")
        reader = csv.reader(lines)
        header = next(reader)
        self.assertIn("process_number", [h.lower() for h in header])

    def test_tier1_format_markdown_validity(self):
        """F-FMT-03: Validação de saída formatada em tabela Markdown."""
        proc = run_cli(["--mock", "--term", "Spotware", "--format", "markdown"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("|", proc.stdout, "Markdown deve conter separadores de tabela '|'")
        self.assertIn("---", proc.stdout, "Markdown deve conter divisória de cabeçalho")

    def test_tier1_format_short_flag(self):
        """F-FMT-04: Operação da flag curta '-f json'."""
        proc = run_cli(["--mock", "--term", "Spotware", "-f", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)

    def test_tier1_format_table_rendering(self):
        """F-FMT-05: Validação do formato textual 'table'."""
        proc = run_cli(["--mock", "--term", "Spotware", "--format", "table"])
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(len(proc.stdout.strip()) > 0)

    # --------------------------------------------------------------------------
    # Feature 8: --output / -o (5 testes)
    # --------------------------------------------------------------------------

    def test_tier1_output_json_file(self):
        """F-OUT-01: Exportação para arquivo físico .json e verificação do conteúdo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "resultado.json"
            proc = run_cli(["--mock", "--term", "Yamaha", "--format", "json", "--output", str(out_file)])
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(out_file.exists(), "Arquivo de saída JSON não foi gerado")
            content = out_file.read_text(encoding="utf-8")
            records = extract_json_results(content)
            self.assertGreaterEqual(len(records), 1)

    def test_tier1_output_csv_file(self):
        """F-OUT-02: Exportação para arquivo físico .csv e conferência de integridade."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "resultado.csv"
            proc = run_cli(["--mock", "--term", "Yamaha", "--format", "csv", "--output", str(out_file)])
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(out_file.exists(), "Arquivo de saída CSV não foi gerado")
            with open(out_file, mode="r", encoding="utf-8-sig", errors="replace") as f:
                reader = csv.reader(f)
                rows = list(reader)
                self.assertGreaterEqual(len(rows), 2)

    def test_tier1_output_markdown_file(self):
        """F-OUT-03: Exportação para arquivo físico .md com tabela formatada."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "resultado.md"
            proc = run_cli(["--mock", "--term", "Yamaha", "--format", "markdown", "--output", str(out_file)])
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(out_file.exists(), "Arquivo de saída MD não foi gerado")
            content = out_file.read_text(encoding="utf-8")
            self.assertIn("|", content)

    def test_tier1_output_short_flag(self):
        """F-OUT-04: Operação da flag curta '-o' para arquivo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "saida_curta.json"
            proc = run_cli(["--mock", "--term", "NovaStar", "-f", "json", "-o", str(out_file)])
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(out_file.exists())

    def test_tier1_output_overwrite_safety(self):
        """F-OUT-05: Sobrescrita segura de arquivo existente."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "sobrescrita.json"
            out_file.write_text("{\"antigo\": true}", encoding="utf-8")
            proc = run_cli(["--mock", "--term", "Spotware", "--format", "json", "--output", str(out_file)])
            self.assertEqual(proc.returncode, 0)
            content = out_file.read_text(encoding="utf-8")
            records = extract_json_results(content)
            self.assertGreaterEqual(len(records), 1)
            self.assertNotIn("{\"antigo\": true}", content)

    # --------------------------------------------------------------------------
    # Feature 9: --mock (5 testes)
    # --------------------------------------------------------------------------

    def test_tier1_mock_offline_execution(self):
        """F-MCK-01: Execução 100% offline via --mock sem chamadas de rede."""
        proc = run_cli(["--mock", "--term", "Spotware"])
        self.assertEqual(proc.returncode, 0)

    def test_tier1_mock_authentic_inventory_data(self):
        """F-MCK-02: Retorno consistente com os dados autênticos do inventário."""
        proc = run_cli(["--mock", "--serial", "008479010011225", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        r0 = records[0]
        self.assertEqual(r0.get("process_number"), "202100020006687")

    def test_tier1_mock_custom_fixture_loading(self):
        """F-MCK-03: Carga de arquivo de fixture customizado via --fixture-file."""
        custom_data = [
            {
                "process_number": "209900000000001",
                "document_number": "99999999",
                "document_type": "Nota Fiscal",
                "date": "01/01/2099",
                "unit": "UEG/TESTE",
                "interested": "Empresa Teste LTDA",
                "link": "https://sei.goias.gov.br/exibir?mock=custom",
                "snippet": "Item Customizado Para Teste Unitario S/N CUSTOM-999",
                "model": "CustomModel",
                "serial": "CUSTOM-999"
            }
        ]
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as f:
            json.dump(custom_data, f)
            temp_path = f.name

        try:
            proc = run_cli(["--mock", "--fixture-file", temp_path, "--serial", "CUSTOM-999", "--format", "json"])
            self.assertEqual(proc.returncode, 0)
            records = extract_json_results(proc.stdout)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].get("process_number"), "209900000000001")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_tier1_mock_schema_conformance(self):
        """F-MCK-04: Validação do schema dos registros retornados pelo modo mock."""
        proc = run_cli(["--mock", "--term", "Yamaha", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        expected_keys = {"process_number", "document_number", "date", "unit", "link"}
        for r in records:
            self.assertTrue(expected_keys.issubset(set(r.keys())), f"Faltam chaves esperadas no registro: {r}")

    def test_tier1_mock_zero_exit_code(self):
        """F-MCK-05: Código de saída 0 mesmo quando nenhum registro é encontrado."""
        proc = run_cli(["--mock", "--term", "PALAVRA_INEXISTENTE_XYZ_99999", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertEqual(len(records), 0)


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES (15 Testes)
# ==============================================================================

class TestTier2BoundaryAndCornerCases(unittest.TestCase):
    """Tier 2: Entradas anômalas, limites, caracteres especiais e robustez."""

    @classmethod
    def setUpClass(cls):
        if not SEI_SCRIPT.exists():
            raise unittest.SkipTest("sei_search.py ainda não criado na raiz do projeto")

    def test_tier2_empty_term_handling(self):
        """BND-01: Tratamento de termo vazio '--term \"\"'."""
        proc = run_cli(["--mock", "--term", "", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertIsInstance(records, list)

    def test_tier2_whitespace_only_term(self):
        """BND-02: Tratamento de termo contendo apenas espaços em branco."""
        proc = run_cli(["--mock", "--term", "     ", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertIsInstance(records, list)

    def test_tier2_unicode_accents_handling(self):
        """BND-03: Preservação e busca com caracteres acentuados ('Goiânia-Laranjeiras')."""
        proc = run_cli(["--mock", "--term", "Goiânia-Laranjeiras", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)

    def test_tier2_special_symbols_handling(self):
        """BND-04: Caracteres e símbolos especiais técnicos ('Ø82mm', 'R$ 209.376,00')."""
        proc = run_cli(["--mock", "--term", "R$ 209.376,00", "--format", "json"])
        self.assertEqual(proc.returncode, 0)

    def test_tier2_nonexistent_serial(self):
        """BND-05: Serial inexistente retorna lista vazia com código de saída 0."""
        proc = run_cli(["--mock", "--serial", "NONEXISTENT_SERIAL_999999", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertEqual(len(records), 0)

    def test_tier2_nonexistent_process(self):
        """BND-06: Processo inexistente retorna lista vazia com código de saída 0."""
        proc = run_cli(["--mock", "--process", "999999999999999", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertEqual(len(records), 0)

    def test_tier2_invalid_date_from_format(self):
        """BND-07: Formato de data inicial inválido rejeitado com código de saída 1."""
        proc = run_cli(["--mock", "--date-from", "2026-12-31", "--format", "json"])
        self.assertEqual(proc.returncode, 1, "Data com formato inválido (AAAA-MM-DD) deve retornar código 1")
        self.assertIn("Formato de data inicial inválido", proc.stderr)

    def test_tier2_invalid_date_to_format(self):
        """BND-08: Formato de data final inválido no calendário rejeitado com código 1."""
        proc = run_cli(["--mock", "--date-to", "99/99/9999", "--format", "json"])
        self.assertEqual(proc.returncode, 1, "Data inexistente no calendário deve retornar código 1")
        self.assertIn("Data final inválida no calendário", proc.stderr)

    def test_tier2_inverted_date_range(self):
        """BND-09: Período com data inicial posterior à data final rejeitado com código 1."""
        proc = run_cli(["--mock", "--date-from", "31/12/2026", "--date-to", "01/01/2020", "--format", "json"])
        self.assertEqual(proc.returncode, 1, "Período invertido (data inicial > final) deve retornar código 1")
        self.assertIn("posterior à data final", proc.stderr)

    def test_tier2_unknown_format_rejection(self):
        """BND-10: Formato de saída desconhecido ('--format xml') rejeitado com erro."""
        proc = run_cli(["--mock", "--format", "unknown_format_xyz"])
        self.assertNotEqual(proc.returncode, 0, "Deveria falhar para formato não suportado")

    def test_tier2_missing_fixture_file(self):
        """BND-11: Arquivo de fixture inexistente deve retornar erro controlado."""
        proc = run_cli(["--mock", "--fixture-file", "arquivo_que_nao_existe_xyz.json"])
        self.assertNotEqual(proc.returncode, 0, "Deveria falhar para fixture inexistente")

    def test_tier2_corrupted_fixture_file(self):
        """BND-12: Arquivo de fixture com JSON corrompido deve ser rejeitado."""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as f:
            f.write("{ INVALID JSON CONTENT ::: ")
            temp_path = f.name

        try:
            proc = run_cli(["--mock", "--fixture-file", temp_path])
            self.assertNotEqual(proc.returncode, 0)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_tier2_extreme_length_term(self):
        """BND-13: Termo de pesquisa extremamente longo (>500 caracteres)."""
        long_term = "Equipamento" * 60
        proc = run_cli(["--mock", "--term", long_term, "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertEqual(len(records), 0)

    def test_tier2_invalid_output_directory(self):
        """BND-14: Caminho de saída em diretório inexistente/ilegítimo."""
        invalid_path = Path("/diretorio_totalmente_invalido_xyz/out.json")
        proc = run_cli(["--mock", "--term", "Yamaha", "--output", str(invalid_path)])
        self.assertNotEqual(proc.returncode, 0)

    def test_tier2_case_insensitivity_matching(self):
        """BND-15: Busca insensível a maiúsculas/minúsculas ('yamaha' vs 'YAMAHA')."""
        proc_lower = run_cli(["--mock", "--term", "yamaha", "--format", "json"])
        proc_upper = run_cli(["--mock", "--term", "YAMAHA", "--format", "json"])
        self.assertEqual(proc_lower.returncode, 0)
        self.assertEqual(proc_upper.returncode, 0)
        rec_lower = extract_json_results(proc_lower.stdout)
        rec_upper = extract_json_results(proc_upper.stdout)
        self.assertEqual(len(rec_lower), len(rec_upper), "A contagem de resultados deve ser idêntica independentemente do case")

    def test_tier2_html_table_parser_thead_isolation(self):
        """BND-16: Parser HTML stdlib ignora <thead> e <th>, evitando registros fantasmas."""
        html_sample = (
            '<table class="infraTable" summary="Resultado da Pesquisa">'
            '  <thead>'
            '    <tr class="infraTrCabecalho">'
            '      <th>Processo</th><th>Tipo</th><th>Unidade</th><th>Data</th><th>Interessado</th><th>Resumo</th>'
            '    </tr>'
            '  </thead>'
            '  <tbody>'
            '    <tr class="infraTrClara">'
            '      <td><a href="md_pesq_processo_exibir.php?id=123">202600005037287</a></td>'
            '      <td>Nota Fiscal</td>'
            '      <td>UEG/COPA-14028</td>'
            '      <td>15/03/2023</td>'
            '      <td>Yamaha Musical do Brasil</td>'
            '      <td>Mesa Yamaha MG12XU</td>'
            '    </tr>'
            '  </tbody>'
            '</table>'
        )
        records = sei_search.parse_sei_html(html_sample)
        self.assertEqual(len(records), 1, "Deve extrair exatamente 1 registro de dados, descartando o thead")
        rec = records[0].to_canonical_dict() if hasattr(records[0], "to_canonical_dict") else records[0]
        self.assertEqual(rec.get("process_number"), "202600005037287")
        self.assertNotEqual(rec.get("document_number"), "Processo")
        self.assertNotEqual(rec.get("document_type"), "Tipo")

    def test_tier2_markdown_pipe_and_newline_resilience(self):
        """BND-17: export_markdown() sanitiza pipes e quebras de linha em todos os campos."""
        sample_records = [
            {
                "process_number": "202600005037287",
                "document_number": "97743690",
                "document_type": "Termo | Recebimento",
                "date": "22/04/2022",
                "unit": "UEG | COT",
                "interested": "Sony Brasil | Merlin Vídeo Pro\nLinha 2",
                "link": "https://sei.goias.gov.br",
                "snippet": "Receptor URX-P03 | S/N 115983\r\nObservações"
            }
        ]
        md_output = sei_search.export_markdown(sample_records)
        lines = [line.strip() for line in md_output.strip().splitlines() if line.startswith("|")]
        self.assertEqual(len(lines), 3)
        for line in lines:
            unescaped_pipes = len(re.findall(r"(?<!\\)\|", line))
            self.assertEqual(unescaped_pipes, 10, f"Linha Markdown violou invariante de colunas: {line}")


# ==============================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS (12 Testes)
# ==============================================================================

class TestTier3CrossFeatureCombinations(unittest.TestCase):
    """Tier 3: Testes de combinações pairwise e multi-flag."""

    @classmethod
    def setUpClass(cls):
        if not SEI_SCRIPT.exists():
            raise unittest.SkipTest("sei_search.py ainda não criado na raiz do projeto")

    def test_tier3_term_unit_format_json(self):
        """CMB-01: Combinação --term 'Spotware' + --unit 'UEG/COPA-14028' + --format json."""
        proc = run_cli(["--mock", "--term", "Spotware", "--unit", "UEG/COPA-14028", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        for r in records:
            self.assertIn("COPA", r.get("unit", ""))

    def test_tier3_process_supplier_output_csv(self):
        """CMB-02: Combinação --process + --supplier + --format csv + --output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_file = Path(tmpdir) / "proc_supp.csv"
            proc = run_cli([
                "--mock",
                "--process", "202100020006687",
                "--supplier", "Floripa Tecnologia",
                "--format", "csv",
                "--output", str(csv_file)
            ])
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(csv_file.exists())
            content = csv_file.read_text(encoding="utf-8-sig", errors="replace")
            self.assertIn("202100020006687", content)
            self.assertIn("Floripa", content)

    def test_tier3_serial_model_mock(self):
        """CMB-03: Combinação --serial 'BRACVX01071' + --model 'MG12XU' + --mock."""
        proc = run_cli(["--mock", "--serial", "BRACVX01071", "--model", "MG12XU", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertEqual(len(records), 1)
        self.assertIn("BRACVX01071", str(records[0]))

    def test_tier3_serial_unit_markdown(self):
        """CMB-04: Combinação --serial '115983' + --unit 'COT' + --format markdown."""
        proc = run_cli(["--mock", "--serial", "115983", "--unit", "COT", "--format", "markdown"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("115983", proc.stdout)
        self.assertIn("|", proc.stdout)

    def test_tier3_model_format_output_json(self):
        """CMB-05: Combinação --model 'VX400' + --format json + --output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            json_file = Path(tmpdir) / "vx400.json"
            proc = run_cli(["--mock", "--model", "VX400", "--format", "json", "--output", str(json_file)])
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(json_file.exists())
            records = extract_json_results(json_file.read_text(encoding="utf-8"))
            self.assertEqual(len(records), 1)

    def test_tier3_term_format_output_csv(self):
        """CMB-06: Combinação --term 'Estoque Now' + --format csv + --output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_file = Path(tmpdir) / "estoquenow.csv"
            proc = run_cli(["--mock", "--term", "Estoque Now", "--format", "csv", "--output", str(csv_file)])
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(csv_file.exists())

    def test_tier3_process_format_output_markdown(self):
        """CMB-07: Combinação --process '202600005037287' + --format markdown + --output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "proc_inventario.md"
            proc = run_cli(["--mock", "--process", "202600005037287", "--format", "markdown", "--output", str(md_file)])
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(md_file.exists())
            content = md_file.read_text(encoding="utf-8")
            self.assertIn("202600005037287", content)

    def test_tier3_term_date_range_filter(self):
        """CMB-08: Combinação --term 'Floripa' + --date-from '01/01/2021' + --date-to '31/12/2023'."""
        proc = run_cli([
            "--mock",
            "--term", "Floripa",
            "--date-from", "01/01/2021",
            "--date-to", "31/12/2023",
            "--format", "json"
        ])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)

    def test_tier3_triple_filter_model_serial_supplier(self):
        """CMB-09: Filtro tríplice estrito: --model + --serial + --supplier."""
        proc = run_cli([
            "--mock",
            "--model", "Spotware-M",
            "--serial", "008479010011225",
            "--supplier", "Floripa Tecnologia",
            "--format", "json"
        ])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        for r in records:
            self.assertEqual(r.get("process_number"), "202100020006687")
            self.assertIn("Floripa", r.get("interested", ""))

    def test_tier3_limit_parameter_json(self):
        """CMB-10: Restrição de cardinalidade via --limit 1 em formato JSON."""
        proc = run_cli(["--mock", "--term", "202600005037287", "--limit", "1", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertLessEqual(len(records), 1)

    def test_tier3_short_flags_combined(self):
        """CMB-11: Agregação de flags curtas '-t' + '-u' + '-f json'."""
        proc = run_cli(["--mock", "-t", "Spotware", "-u", "COPA", "-f", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)

    def test_tier3_short_flags_serial_model_output(self):
        """CMB-12: Agregação de flags curtas '-s' + '-m' + '-o'."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "curtas.json"
            proc = run_cli(["--mock", "-s", "BRACVX01071", "-m", "MG12XU", "-f", "json", "-o", str(out_file)])
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(out_file.exists())

    def test_tier3_cross_inventory_cli_yamaha(self):
        """CMB-13: Verificação de ponta a ponta de --cross-inventory para Yamaha (Estoque Now)."""
        proc = run_cli(["--mock", "--term", "000215", "--cross-inventory"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("[ESTOQUE_NOW] 000215: Mesa de Som Yamaha - Mg12xu 1", proc.stderr)
        self.assertNotIn("000215: None", proc.stderr)

    def test_tier3_cross_inventory_cli_spotware(self):
        """CMB-14: Verificação de ponta a ponta de --cross-inventory para Spotware (SPM Master)."""
        proc = run_cli(["--mock", "--term", "3111136", "--cross-inventory"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("[SPM_MASTER] 3111136", proc.stderr)
        self.assertNotIn("carga: None", proc.stderr)

    def test_tier3_cross_inventory_programmatic(self):
        """CMB-15: Validação programática das resoluções de fallback em check_cross_inventory()."""
        res_en = sei_search.check_cross_inventory("000215")
        self.assertGreaterEqual(len(res_en), 1)
        en_item = res_en[0]
        self.assertEqual(en_item.get("descricao"), "Mesa de Som Yamaha - Mg12xu 1")
        self.assertIsNotNone(en_item.get("categoria"))

        res_spm = sei_search.check_cross_inventory("3111136")
        self.assertGreaterEqual(len(res_spm), 1)
        spm_item = res_spm[0]
        self.assertEqual(spm_item.get("carga"), "CRIA LAB")


# ==============================================================================
# TIER 4: REAL-WORLD SCENARIOS & GUIA DOCUMENTAL VALIDATION (11 Testes)
# ==============================================================================

class TestTier4RealWorldScenariosAndGuide(unittest.TestCase):
    """Tier 4: Cenários reais do inventário patrimonial e auditoria do Guia SEI."""

    @classmethod
    def setUpClass(cls):
        if not GUIA_DOC.exists():
            raise unittest.SkipTest("GUIA_INSTRUCAO_PATRIMONIAL_SEI.md ainda não criado na raiz do projeto")
        cls.guia_content = GUIA_DOC.read_text(encoding="utf-8")

    # --------------------------------------------------------------------------
    # Cenários Reais de Pesquisa com sei_search.py
    # --------------------------------------------------------------------------

    def test_tier4_scenario_servidor_floripa_spotware(self):
        """SCE-01: Localização do Servidor Spotware-M (Contrato 068/2022 / Proc 202100020006687)."""
        if not SEI_SCRIPT.exists():
            self.skipTest("sei_search.py não disponível")
        proc = run_cli(["--mock", "--term", "Spotware", "--serial", "008479010011225", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)
        r0 = records[0]
        self.assertEqual(r0.get("process_number"), "202100020006687")
        self.assertIn("Floripa", r0.get("interested", "") + r0.get("supplier", ""))

    def test_tier4_scenario_yamaha_mg12xu(self):
        """SCE-02: Localização da Mesa Yamaha MG12XU (S/N BRACVX01071 / Estoque Now 000215)."""
        if not SEI_SCRIPT.exists():
            self.skipTest("sei_search.py não disponível")
        proc = run_cli(["--mock", "--model", "MG12XU", "--serial", "BRACVX01071", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertEqual(len(records), 1)
        self.assertIn("BRACVX01071", str(records[0]))

    def test_tier4_scenario_novastar_vx400(self):
        """SCE-03: Localização do Controlador NovaStar VX400 (S/N 21MB44422N0A10002120)."""
        if not SEI_SCRIPT.exists():
            self.skipTest("sei_search.py não disponível")
        proc = run_cli(["--mock", "--model", "VX400", "--serial", "21MB44422N0A10002120", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertEqual(len(records), 1)
        self.assertIn("21MB44422N0A10002120", str(records[0]))

    def test_tier4_scenario_sony_urx_p03(self):
        """SCE-04: Localização do Receptor Sony URX-P03 (S/N 115983 / Radioteledifusão)."""
        if not SEI_SCRIPT.exists():
            self.skipTest("sei_search.py não disponível")
        proc = run_cli(["--mock", "--model", "URX-P03", "--serial", "115983", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertEqual(len(records), 1)
        self.assertIn("115983", str(records[0]))

    def test_tier4_scenario_estoquenow_items(self):
        """SCE-05: Localização de itens operacionais do acervo Estoque Now (Atem Mini, Sony 24-70)."""
        if not SEI_SCRIPT.exists():
            self.skipTest("sei_search.py não disponível")
        proc = run_cli(["--mock", "--term", "Estoque Now", "--format", "json"])
        self.assertEqual(proc.returncode, 0)
        records = extract_json_results(proc.stdout)
        self.assertGreaterEqual(len(records), 1)

    # --------------------------------------------------------------------------
    # Validação Estrutural e Forense do GUIA_INSTRUCAO_PATRIMONIAL_SEI.md
    # --------------------------------------------------------------------------

    def test_tier4_guia_documental_file_exists(self):
        """GIA-01: Existência física e tamanho substantivo do Guia de Instrução Patrimonial."""
        self.assertTrue(GUIA_DOC.exists(), "GUIA_INSTRUCAO_PATRIMONIAL_SEI.md deve existir na raiz do projeto")
        size = GUIA_DOC.stat().st_size
        self.assertGreaterEqual(size, 10000, f"O Guia deve ser detalhado e substancial (>10KB), encontrado {size} bytes")

    def test_tier4_guia_processo_and_campus_reference(self):
        """GIA-02: Menção explícita ao Processo SEI 202600005037287 e Câmpus Goiânia-Laranjeiras."""
        self.assertIn("202600005037287", self.guia_content, "Guia deve referenciar o processo SEI central 202600005037287")
        self.assertTrue(
            "Laranjeiras" in self.guia_content or "Goiânia-Laranjeiras" in self.guia_content,
            "Guia deve contextualizar a Unidade Goiânia-Laranjeiras"
        )
        self.assertIn("CriaLab", self.guia_content, "Guia deve referenciar nominalmente o laboratório CriaLab")

    def test_tier4_guia_seven_document_types_complete(self):
        """GIA-03: Detalhamento exaustivo dos 7 tipos documentais essenciais e do TCA."""
        required_terms = [
            ("Nota Fiscal", "DANFE"),
            ("Processo", "Licitat"),
            ("Nota de Empenho", "44.90.52"),
            ("Ordem de Fornecimento", "Atesto"),
            ("Termo de Doação", "Transferência"),
            ("Termo de Responsabilidade", "Cautela"),
            ("Ficha de Apuração", "SPM"),
            ("Termo Circunstanciado", "TCA"),
        ]
        for term_a, term_b in required_terms:
            found = (term_a.lower() in self.guia_content.lower()) or (term_b.lower() in self.guia_content.lower())
            self.assertTrue(found, f"Tipo documental ou termo indispensável ausente no guia: {term_a} / {term_b}")

    def test_tier4_guia_uncataloged_items_dossier(self):
        """GIA-04: Dossiê específico para todos os equipamentos não tombados auditados."""
        required_items = [
            ("Spotware", "008479010011225"),  # Servidor Floripa
            ("MG12XU", "BRACVX01071"),        # Mesa Yamaha
            ("VX400", "21MB44422N0A10002120"), # Processador NovaStar
            ("URX-P03", "115983"),            # Receptor Sony
            ("DIR-615", "702226"),            # Roteador D-Link legado
            ("Estoque Now", "245"),           # Acervo Estoque Now
        ]
        for model, serial in required_items:
            self.assertIn(model, self.guia_content, f"Equipamento {model} ausente no Guia")
            self.assertIn(serial, self.guia_content, f"Identificador {serial} ausente no Guia")

    def test_tier4_guia_legal_and_regulatory_norms(self):
        """GIA-05: Citação expressa ao arcabouço normativo aplicável."""
        norms = [
            "4.320",      # Lei 4.320/1964
            "005/2019",   # IN 005/2019 SEAD
            "02/2023",    # IN 02/2023 CGE
            "1210/2026",  # Portaria UEG 1210/2026
        ]
        for norm in norms:
            self.assertIn(norm, self.guia_content, f"Norma jurídica essencial ausente no Guia: {norm}")

    def test_tier4_guia_administrative_units_and_deadlines(self):
        """GIA-06: Mapeamento de unidades administrativas e prazos fatais."""
        self.assertIn("14028", self.guia_content, "Código de unidade UEG/COPA-14028 ausente")
        self.assertTrue(
            "13/11/2026" in self.guia_content or "1049/2026" in self.guia_content,
            "Prazo fatal de 13/11/2026 (Despacho 1049/2026) ausente"
        )


# ==============================================================================
# RUNNER PRINCIPAL
# ==============================================================================

def main():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTests(loader.loadTestsFromTestCase(TestTier1FeatureCoverage))
    suite.addTests(loader.loadTestsFromTestCase(TestTier2BoundaryAndCornerCases))
    suite.addTests(loader.loadTestsFromTestCase(TestTier3CrossFeatureCombinations))
    suite.addTests(loader.loadTestsFromTestCase(TestTier4RealWorldScenariosAndGuide))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
