"""Extrai as respostas nacionais mínimas das tabelas SIDRA 9542 e 9543."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


TIMEOUT_SECONDS = 30
MODULE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = MODULE_DIR / "dados" / "brutos" / "sidra"

QUERIES = (
    {
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
    {
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
)


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
    """Executa as duas consultas validadas e preserva suas respostas brutas."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    destinations = [OUTPUT_DIR / query["filename"] for query in QUERIES]
    existing_files = [path for path in destinations if path.exists()]
    if existing_files:
        names = ", ".join(path.name for path in existing_files)
        print(f"Extração cancelada: arquivo(s) já existente(s): {names}", file=sys.stderr)
        return 1

    responses: list[tuple[Path, bytes]] = []
    for query, destination in zip(QUERIES, destinations, strict=True):
        url = build_url(query["endpoint"], query["parameters"])
        responses.append((destination, fetch_json_bytes(url)))

    for destination, content in responses:
        write_new_file(destination, content)
        print(f"Gravado: {destination.relative_to(MODULE_DIR)} ({len(content)} bytes)")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError) as error:
        print(f"Falha na extração: {error}", file=sys.stderr)
        raise SystemExit(1) from error
