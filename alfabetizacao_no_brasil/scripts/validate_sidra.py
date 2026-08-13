"""Valida as respostas nacionais mínimas extraídas do SIDRA."""

from __future__ import annotations

import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any


MODULE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = MODULE_DIR / "dados" / "brutos" / "sidra"
FILE_9542 = DATA_DIR / "9542_2022_brasil_total.json"
FILE_9543 = DATA_DIR / "9543_2022_brasil_total.json"

EXPECTED_LITERACY_CATEGORIES = {"93024", "1023", "1024"}
EXPECTED_TOTAL_CATEGORIES = {"2": "6794", "86": "95251", "287": "100362"}


class ValidationError(Exception):
    """Indica que um arquivo não atende ao contrato mínimo esperado."""


def require(condition: bool, message: str) -> None:
    """Interrompe a validação quando uma regra não é satisfeita."""
    if not condition:
        raise ValidationError(message)


def load_single_variable(path: Path) -> dict[str, Any]:
    """Carrega um JSON bruto que deve conter exatamente uma variável."""
    require(path.is_file(), f"arquivo não encontrado: {path}")

    with path.open(encoding="utf-8") as file:
        payload = json.load(file)

    require(isinstance(payload, list), f"{path.name}: raiz do JSON não é uma lista")
    require(len(payload) == 1, f"{path.name}: esperado 1 item na raiz, obtido {len(payload)}")
    require(isinstance(payload[0], dict), f"{path.name}: variável não é um objeto")
    return payload[0]


def classification_codes(result: dict[str, Any], context: str) -> dict[str, str]:
    """Obtém um código de categoria para cada classificação do resultado."""
    classifications = result.get("classificacoes")
    require(isinstance(classifications, list), f"{context}: classificações ausentes")

    codes: dict[str, str] = {}
    for classification in classifications:
        require(isinstance(classification, dict), f"{context}: classificação não é um objeto")
        classification_id = str(classification.get("id"))
        categories = classification.get("categoria")
        require(isinstance(categories, dict), f"{context}: categoria inválida")
        require(len(categories) == 1, f"{context}: esperado 1 código por classificação")
        require(classification_id not in codes, f"{context}: classificação {classification_id} duplicada")
        codes[classification_id] = str(next(iter(categories)))

    return codes


def series_value(result: dict[str, Any], context: str) -> str:
    """Obtém o valor de Brasil em 2022 e valida sua granularidade territorial."""
    series = result.get("series")
    require(isinstance(series, list), f"{context}: séries ausentes")
    require(len(series) == 1, f"{context}: esperado 1 território, obtido {len(series)}")
    require(isinstance(series[0], dict), f"{context}: série não é um objeto")

    locality = series[0].get("localidade", {})
    level = locality.get("nivel", {})
    require(str(locality.get("id")) == "1", f"{context}: código do Brasil inválido")
    require(level.get("id") == "N1", f"{context}: nível territorial diferente de N1")
    require(locality.get("nome") == "Brasil", f"{context}: nome da localidade inválido")

    values = series[0].get("serie")
    require(isinstance(values, dict), f"{context}: série temporal ausente")
    require(set(values) == {"2022"}, f"{context}: período diferente de 2022")
    return str(values["2022"])


def validate_9542(variable: dict[str, Any]) -> dict[str, int]:
    """Valida os três contingentes e retorna valores por categoria."""
    require(str(variable.get("id")) == "950", "9542: variável diferente de 950")
    require(variable.get("unidade") == "Pessoas", "9542: unidade diferente de Pessoas")

    results = variable.get("resultados")
    require(isinstance(results, list), "9542: resultados ausentes")
    require(len(results) == 3, f"9542: esperados 3 resultados, obtidos {len(results)}")

    counts: dict[str, int] = {}
    for result in results:
        require(isinstance(result, dict), "9542: resultado não é um objeto")
        codes = classification_codes(result, "9542")
        require(set(codes) == {"59", *EXPECTED_TOTAL_CATEGORIES}, "9542: classificações inesperadas")
        for classification_id, category_id in EXPECTED_TOTAL_CATEGORIES.items():
            require(codes[classification_id] == category_id, f"9542: recorte total inválido em {classification_id}")

        literacy_category = codes["59"]
        require(literacy_category in EXPECTED_LITERACY_CATEGORIES, "9542: categoria de alfabetização inválida")
        require(literacy_category not in counts, f"9542: categoria {literacy_category} duplicada")

        raw_value = series_value(result, f"9542 categoria {literacy_category}")
        require(raw_value.isdecimal(), f"9542 categoria {literacy_category}: valor não inteiro")
        counts[literacy_category] = int(raw_value)

    require(set(counts) == EXPECTED_LITERACY_CATEGORIES, "9542: conjunto de categorias incompleto")
    require(counts["93024"] > 0, "9542: população total deve ser positiva")
    require(
        counts["93024"] - counts["1023"] == counts["1024"],
        "9542: total menos alfabetizadas difere de não alfabetizadas",
    )
    return counts


def validate_9543(variable: dict[str, Any]) -> Decimal:
    """Valida e retorna a taxa oficial nacional de alfabetização."""
    require(str(variable.get("id")) == "2513", "9543: variável diferente de 2513")
    require(variable.get("unidade") == "%", "9543: unidade diferente de %")

    results = variable.get("resultados")
    require(isinstance(results, list), "9543: resultados ausentes")
    require(len(results) == 1, f"9543: esperado 1 resultado, obtidos {len(results)}")
    require(isinstance(results[0], dict), "9543: resultado não é um objeto")

    codes = classification_codes(results[0], "9543")
    require(codes == EXPECTED_TOTAL_CATEGORIES, "9543: recortes demográficos diferentes do total")

    official_rate = Decimal(series_value(results[0], "9543"))
    require(Decimal("0") <= official_rate <= Decimal("100"), "9543: taxa fora do intervalo de 0 a 100")
    return official_rate


def main() -> int:
    """Executa as validações estruturais e as regras analíticas nacionais."""
    counts = validate_9542(load_single_variable(FILE_9542))
    official_rate = validate_9543(load_single_variable(FILE_9543))

    calculated_rate = Decimal(counts["1023"]) / Decimal(counts["93024"]) * 100
    rounded_rate = calculated_rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    require(rounded_rate == official_rate, "taxa calculada arredondada difere da taxa oficial")

    print("Validação concluída: 2 arquivos, 4 resultados e nenhuma inconsistência.")
    print(
        "Contingentes: "
        f"total={counts['93024']}, alfabetizadas={counts['1023']}, "
        f"não alfabetizadas={counts['1024']}"
    )
    print(f"Taxa calculada={calculated_rate:.6f}% | taxa oficial={official_rate:.2f}%")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, json.JSONDecodeError, InvalidOperation, OSError) as error:
        print(f"Falha na validação: {error}", file=sys.stderr)
        raise SystemExit(1) from error
