import re
from rapidfuzz import fuzz
from ocr_utils import extract_text_from_pdf


EDUCATION_LEVELS = {
    "10th": ["SSC", "SECONDARY SCHOOL", "10TH"],
    "12th": ["HSC", "HIGHER SECONDARY", "12TH"],
    "diploma": ["DIPLOMA"],
    "graduation": [
        "BACHELOR",
        "BACHELOR DEGREE",
        "BTECH",
        "BE",
        "BSC",
        "BCOM",
        "BA",
        "BCA"
    ],
    "postgraduation": [
        "POSTGRADUATE",
        "MASTER",
        "MASTER DEGREE",
        "MBA",
        "MCA",
        "MTECH",
        "M.SC",
        "MSC",
        "MCOM",
        "LLM"
    ]
}


def fuzzy_name_match(value: str, text: str, threshold=80):
    value = value.lower()
    text = text.lower()

    score = fuzz.partial_ratio(value, text)

    if score >= threshold:
        return True, score

    return False, score


def detect_result(text: str) -> str:
    text = text.lower()

    if re.search(r"\b(pass|passed)\b", text):
        return "pass"

    if re.search(r"\b(fail|failed)\b", text):
        return "fail"

    return "unknown"


def validate_education_level(extracted_text: str, education_level: str):

    text = extracted_text.lower()
    keywords = EDUCATION_LEVELS.get(education_level.lower(), [])

    for keyword in keywords:
        pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
        if re.search(pattern, text):
            return True, keyword

    return False, None


def verify_marksheet(file_bytes, name, surname, education_level):

    extracted_text = extract_text_from_pdf(file_bytes)

    if not extracted_text:
        return {"error": "Text extraction failed"}

    name_match, name_score = fuzzy_name_match(name, extracted_text)
    surname_match, surname_score = fuzzy_name_match(surname, extracted_text)

    education_match, matched_keyword = validate_education_level(
        extracted_text,
        education_level
    )

    result_status = detect_result(extracted_text)

    verified = name_match and surname_match and education_match

    return {
        "name_match": name_match,
        "surname_match": surname_match,
        "education_match": education_match,
        "matched_keyword": matched_keyword,
        "result": result_status,
        "verified": verified,
        "name_score": name_score,
        "surname_score": surname_score
    }
