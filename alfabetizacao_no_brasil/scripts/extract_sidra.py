"""Extrai respostas brutas previamente definidas das tabelas SIDRA."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


TIMEOUT_SECONDS = 30
MODULE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = MODULE_DIR / "dados" / "brutos" / "sidra"

QUERIES = {
    "9542_brasil_total": {
        "endpoint": (
            "https://servicodados.ibge.gov.br/api/v3/agregados/9542/"
            "periodos/2022/variaveis/950"
        ),
        "parameters": {
            "localidades": "N1[all]",
            "classificacao": (
                "59[93024,1023,1024]|2[6794]|86[95251]|287[100362]"
            ),
        },
        "filename": "9542_2022_brasil_total.json",
    },
    "9543_brasil_total": {
        "endpoint": (
            "https://servicodados.ibge.gov.br/api/v3/agregados/9543/"
            "periodos/2022/variaveis/2513"
        ),
        "parameters": {
            "localidades": "N1[all]",
            "classificacao": "2[6794]|86[95251]|287[100362]",
        },
        "filename": "9543_2022_brasil_total.json",
    },
    "9542_regioes_total": {
        "endpoint": (
            "https://servicodados.ibge.gov.br/api/v3/agregados/9542/"
            "periodos/2022/variaveis/950"
        ),
        "parameters": {
            "localidades": "N2[all]",
            "classificacao": (
                "59[93024,1023,1024]|2[6794]|86[95251]|287[100362]"
            ),
        },
        "filename": "9542_2022_regioes_total.json",
    },
}


def parse_args() -> argparse.Namespace:
    """Lê a chave da consulta que deverá ser executada."""
    parser = argparse.ArgumentParser(
        description="Extrai uma resposta bruta do SIDRA sem sobrescrever arquivos."
    )
    parser.add_argument(
        "query",
        choices=QUERIES,
        help="consulta cadastrada que será executada",
    )
    return parser.parse_args()


def build_url(endpoint: str, parameters: dict[str, str]) -> str:
    """Monta a URL codificando os parâmetros da consulta."""
    return f"{endpoint}?{urlencode(parameters)}"


def fetch_json_bytes(url: str) -> bytes:
    """Obtém a resposta e confirma que seu conteúdo é um JSON válido."""
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "censo-2022-retratos-do-brasil/0.1",
        },
    )

    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        content_type = response.headers.get_content_type()
        if content_type != "application/json":
            raise ValueError(f"tipo de conteúdo inesperado: {content_type}")

        content = response.read()

    json.loads(content)
    return content


def write_new_file(destination: Path, content: bytes) -> None:
    """Grava os bytes originais sem permitir a sobrescrita do destino."""
    with destination.open("xb") as file:
        file.write(content)


def main() -> int:
    """Executa somente a consulta escolhida e preserva sua resposta bruta."""
    args = parse_args()
    query = QUERIES[args.query]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    destination = OUTPUT_DIR / query["filename"]
    if destination.exists():
        print(f"Extração cancelada: arquivo já existente: {destination.name}", file=sys.stderr)
        return 1

    url = build_url(query["endpoint"], query["parameters"])
    content = fetch_json_bytes(url)
    write_new_file(destination, content)
    print(f"Gravado: {destination.relative_to(MODULE_DIR)} ({len(content)} bytes)")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError) as error:
        print(f"Falha na extração: {error}", file=sys.stderr)
        raise SystemExit(1) from error
