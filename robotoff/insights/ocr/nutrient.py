import re
from typing import List, Dict

from robotoff.insights.ocr.dataclass import OCRResult, OCRRegex, OCRField


def generate_nutrient_regex(nutrient_names: List[str], units: List[str]):
    nutrient_names_str = '|'.join(nutrient_names)
    units_str = '|'.join(units)
    return re.compile(r"(?<!\w)({}) ?(?:[:-] ?)?([0-9]+[,.]?[0-9]*) ?({})(?!\w)".format(nutrient_names_str,
                                                                                          units_str))


NUTRIENT_VALUES_REGEX = {
    'energy': OCRRegex(
        generate_nutrient_regex(["[ée]nergie", "energy", "calories"], ["kj", "kcal"]),
        field=OCRField.full_text_contiguous,
        lowercase=True),
    'saturated_fat': OCRRegex(
        generate_nutrient_regex(["mati[èe]res? grasses? satur[ée]s?", "saturated fat"], ["g"]),
        field=OCRField.full_text_contiguous,
        lowercase=True),
    'trans_fat': OCRRegex(
        generate_nutrient_regex(["mati[èe]res? grasses? trans", "trans fat"], ["g"]),
        field=OCRField.full_text_contiguous,
        lowercase=True),
    'fat': OCRRegex(
        generate_nutrient_regex(["mati[èe]res? grasses?", "total fat"], ["g"]),
        field=OCRField.full_text_contiguous,
        lowercase=True),
    'glucid': OCRRegex(
        generate_nutrient_regex(["glucides?", "glucid"], ["g"]),
        field=OCRField.full_text_contiguous,
        lowercase=True),
    'carbohydrate': OCRRegex(
        generate_nutrient_regex(["sucres?", "total carbohydrate", "sugars?"], ["g"]),
        field=OCRField.full_text_contiguous,
        lowercase=True),
    'protein': OCRRegex(
        generate_nutrient_regex(["prot[ée]ines?", "protein"], ["g"]),
        field=OCRField.full_text_contiguous,
        lowercase=True),
}


def find_nutrient_values(ocr_result: OCRResult) -> List[Dict]:
    results = []

    for regex_code, ocr_regex in NUTRIENT_VALUES_REGEX.items():
        text = ocr_result.get_text(ocr_regex)

        if not text:
            continue

        for match in ocr_regex.regex.finditer(text):
            value = match.group(2).replace(',', '.')
            unit = match.group(3)
            results.append({
                "raw": match.group(0),
                "nutrient": regex_code,
                'value': value,
                'unit': unit,
                'notify': ocr_regex.notify,
            })

    return results
