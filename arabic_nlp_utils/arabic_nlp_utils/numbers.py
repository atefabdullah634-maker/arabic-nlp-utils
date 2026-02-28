"""
arabic_nlp_utils.numbers
=========================
تحويل الأرقام بين العربية والهندية والغربية + تحويل رقم لكلمات عربية.

Convert numbers between Arabic-Indic, Eastern Arabic, and Western digits,
and convert integers to Arabic words.
"""

import re

# ───────── Digit Maps ─────────

ARABIC_INDIC_DIGITS = '٠١٢٣٤٥٦٧٨٩'
EASTERN_ARABIC_DIGITS = '۰۱۲۳۴۵۶۷۸۹'  # Persian/Urdu numerals
WESTERN_DIGITS = '0123456789'

_AR_TO_WEST = str.maketrans(ARABIC_INDIC_DIGITS, WESTERN_DIGITS)
_WEST_TO_AR = str.maketrans(WESTERN_DIGITS, ARABIC_INDIC_DIGITS)
_EAST_TO_WEST = str.maketrans(EASTERN_ARABIC_DIGITS, WESTERN_DIGITS)
_WEST_TO_EAST = str.maketrans(WESTERN_DIGITS, EASTERN_ARABIC_DIGITS)
_AR_TO_EAST = str.maketrans(ARABIC_INDIC_DIGITS, EASTERN_ARABIC_DIGITS)
_EAST_TO_AR = str.maketrans(EASTERN_ARABIC_DIGITS, ARABIC_INDIC_DIGITS)

ARABIC_DIGIT_PATTERN = re.compile(r'[٠-٩]+')
EASTERN_DIGIT_PATTERN = re.compile(r'[۰-۹]+')
WESTERN_DIGIT_PATTERN = re.compile(r'[0-9]+')
ANY_DIGIT_PATTERN = re.compile(r'[٠-٩۰-۹0-9]+')


def to_western_numerals(text: str) -> str:
    """
    تحويل الأرقام العربية والهندية إلى أرقام غربية.

    Convert Arabic-Indic and Eastern Arabic digits to Western digits.

    >>> to_western_numerals("العدد ١٢٣ أو ۴۵۶")
    'العدد 123 أو 456'
    """
    return text.translate(_AR_TO_WEST).translate(_EAST_TO_WEST)


def to_arabic_numerals(text: str) -> str:
    """
    تحويل الأرقام الغربية والهندية إلى أرقام عربية (٠-٩).

    Convert Western and Eastern Arabic digits to Arabic-Indic digits.

    >>> to_arabic_numerals("العدد 123")
    'العدد ١٢٣'
    """
    return text.translate(_WEST_TO_AR).translate(_EAST_TO_AR)


def to_eastern_numerals(text: str) -> str:
    """
    تحويل الأرقام الغربية والعربية إلى أرقام شرقية (فارسية/أردية).

    Convert to Eastern Arabic (Persian/Urdu) digits (۰-۹).

    >>> to_eastern_numerals("العدد 123")
    'العدد ۱۲۳'
    """
    return text.translate(_WEST_TO_EAST).translate(_AR_TO_EAST)


def extract_numbers(text: str) -> list:
    """
    استخراج جميع الأرقام (بكل الأنظمة) من النص كأعداد صحيحة.

    Extract all numbers from text as integers.

    >>> extract_numbers("لدي ٢٣ تفاحة و 15 برتقالة")
    [23, 15]
    """
    # First convert everything to western
    converted = to_western_numerals(text)
    return [int(m) for m in WESTERN_DIGIT_PATTERN.findall(converted)]


# ─────── Number to Arabic Words ───────

_ONES = [
    '', 'واحد', 'اثنان', 'ثلاثة', 'أربعة', 'خمسة',
    'ستة', 'سبعة', 'ثمانية', 'تسعة'
]
_TEENS = [
    'عشرة', 'أحد عشر', 'اثنا عشر', 'ثلاثة عشر', 'أربعة عشر',
    'خمسة عشر', 'ستة عشر', 'سبعة عشر', 'ثمانية عشر', 'تسعة عشر'
]
_TENS = [
    '', '', 'عشرون', 'ثلاثون', 'أربعون', 'خمسون',
    'ستون', 'سبعون', 'ثمانون', 'تسعون'
]
_HUNDREDS = [
    '', 'مئة', 'مئتان', 'ثلاثمئة', 'أربعمئة', 'خمسمئة',
    'ستمئة', 'سبعمئة', 'ثمانمئة', 'تسعمئة'
]
_SCALE = [
    ('', ''),
    ('ألف', 'آلاف'),
    ('مليون', 'ملايين'),
    ('مليار', 'مليارات'),
    ('تريليون', 'تريليونات'),
]


def _number_under_1000(n: int) -> str:
    """Convert a number 0-999 to Arabic words."""
    if n == 0:
        return ''

    parts = []

    hundreds = n // 100
    remainder = n % 100

    if hundreds:
        parts.append(_HUNDREDS[hundreds])

    if remainder >= 10 and remainder <= 19:
        parts.append(_TEENS[remainder - 10])
    else:
        tens = remainder // 10
        ones = remainder % 10
        if ones:
            parts.append(_ONES[ones])
        if tens:
            parts.append(_TENS[tens])

    return ' و'.join(parts)


def number_to_words(n: int) -> str:
    """
    تحويل عدد صحيح إلى كلمات عربية.

    Convert an integer to Arabic words.

    >>> number_to_words(0)
    'صفر'
    >>> number_to_words(1)
    'واحد'
    >>> number_to_words(15)
    'خمسة عشر'
    >>> number_to_words(123)
    'مئة وثلاثة وعشرون'
    >>> number_to_words(1000)
    'ألف'
    >>> number_to_words(2025)
    'ألفان وخمسة وعشرون'
    """
    if n == 0:
        return 'صفر'

    if n < 0:
        return 'سالب ' + number_to_words(-n)

    groups = []
    scale_idx = 0
    remaining = n

    while remaining > 0:
        group = remaining % 1000
        if group != 0:
            group_words = _number_under_1000(group)

            if scale_idx > 0:
                singular, plural = _SCALE[scale_idx]
                if group == 1:
                    group_words = singular
                elif group == 2:
                    group_words = singular.rstrip('ة') + 'ان' if singular.endswith('ة') else singular + 'ان'
                elif group >= 3 and group <= 10:
                    group_words = group_words + ' ' + plural
                else:
                    group_words = group_words + ' ' + singular
            groups.append(group_words)

        remaining //= 1000
        scale_idx += 1

    groups.reverse()
    return ' و'.join(groups)


def words_to_number(text: str) -> int:
    """
    محاولة تحويل كلمات عربية بسيطة إلى عدد.

    Attempt to convert simple Arabic number words to integer.

    >>> words_to_number("ثلاثة")
    3
    >>> words_to_number("خمسة عشر")
    15
    >>> words_to_number("صفر")
    0
    """
    text = text.strip()

    if text == 'صفر':
        return 0

    # Build reverse lookup
    word_map = {}
    for i, w in enumerate(_ONES):
        if w:
            word_map[w] = i
    for i, w in enumerate(_TEENS):
        word_map[w] = i + 10
    for i, w in enumerate(_TENS):
        if w:
            word_map[w] = i * 10
    for i, w in enumerate(_HUNDREDS):
        if w:
            word_map[w] = i * 100
    word_map['ألف'] = 1000
    word_map['ألفان'] = 2000
    word_map['مليون'] = 1000000
    word_map['مليار'] = 1000000000

    # Split by "و" and try matching
    parts = [p.strip() for p in text.replace(' و', ' و').split('و')]
    total = 0
    for part in parts:
        part = part.strip()
        if part in word_map:
            total += word_map[part]

    return total
