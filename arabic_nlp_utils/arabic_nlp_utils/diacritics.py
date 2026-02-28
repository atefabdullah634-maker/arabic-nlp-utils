"""
arabic_nlp_utils.diacritics
============================
معالجة التشكيل (الحركات) في النصوص العربية.

Handle Arabic diacritics (tashkeel / harakat).
"""

import re

# ───────── Diacritics Constants ─────────

FATHATAN = '\u064B'   # ً
DAMMATAN = '\u064C'   # ٌ
KASRATAN = '\u064D'   # ٍ
FATHA    = '\u064E'   # َ
DAMMA    = '\u064F'   # ُ
KASRA    = '\u0650'   # ِ
SHADDA   = '\u0651'   # ّ
SUKUN    = '\u0652'   # ْ
MADDAH   = '\u0653'   # ٓ
HAMZA_ABOVE_MARK = '\u0654'  # ٔ
HAMZA_BELOW_MARK = '\u0655'  # ٕ
SUPERSCRIPT_ALEF = '\u0670'  # ٰ

ALL_DIACRITICS = [
    FATHATAN, DAMMATAN, KASRATAN,
    FATHA, DAMMA, KASRA,
    SHADDA, SUKUN, MADDAH,
    HAMZA_ABOVE_MARK, HAMZA_BELOW_MARK,
    SUPERSCRIPT_ALEF,
]

DIACRITICS_PATTERN = re.compile(r'[\u064B-\u0655\u0670]')

HARAKAT_ONLY = re.compile(r'[\u064E-\u0650]')        # فتحة ضمة كسرة
TANWEEN_ONLY = re.compile(r'[\u064B-\u064D]')         # تنوين
SHADDA_PATTERN = re.compile(r'\u0651')
SUKUN_PATTERN = re.compile(r'\u0652')

DIACRITICS_NAMES = {
    FATHATAN: 'فتحتان (تنوين فتح)',
    DAMMATAN: 'ضمتان (تنوين ضم)',
    KASRATAN: 'كسرتان (تنوين كسر)',
    FATHA:    'فتحة',
    DAMMA:    'ضمة',
    KASRA:    'كسرة',
    SHADDA:   'شدة',
    SUKUN:    'سكون',
    MADDAH:   'مدة',
}


def remove_diacritics(text: str) -> str:
    """
    إزالة جميع الحركات والتشكيل من النص.

    Remove all diacritics (tashkeel) from text.

    >>> remove_diacritics("بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ")
    'بسم الله الرحمن الرحيم'
    """
    return DIACRITICS_PATTERN.sub('', text)


def remove_harakat(text: str) -> str:
    """
    إزالة الحركات الأساسية فقط (فتحة، ضمة، كسرة) بدون التنوين أو الشدة.

    Remove only basic harakat (fatha, damma, kasra).

    >>> remove_harakat("كَتَبَ")
    'كتب'
    """
    return HARAKAT_ONLY.sub('', text)


def remove_tanween(text: str) -> str:
    """
    إزالة التنوين فقط.

    Remove only tanween marks.

    >>> remove_tanween("كتابًا")
    'كتابا'
    """
    return TANWEEN_ONLY.sub('', text)


def remove_shadda(text: str) -> str:
    """
    إزالة الشدة فقط.

    Remove only shadda marks.
    """
    return SHADDA_PATTERN.sub('', text)


def has_diacritics(text: str) -> bool:
    """
    فحص هل النص يحتوي على تشكيل.

    Check if text contains any diacritics.

    >>> has_diacritics("بِسْمِ اللَّهِ")
    True
    >>> has_diacritics("بسم الله")
    False
    """
    return bool(DIACRITICS_PATTERN.search(text))


def count_diacritics(text: str) -> int:
    """
    عد الحركات في النص.

    Count total number of diacritics in text.

    >>> count_diacritics("بِسْمِ")
    3
    """
    return len(DIACRITICS_PATTERN.findall(text))


def diacritics_stats(text: str) -> dict:
    """
    إحصائيات تفصيلية عن أنواع الحركات في النص.

    Detailed statistics of diacritic types in the text.

    Returns
    -------
    dict
        Dictionary with diacritic names (Arabic) as keys and counts as values.

    >>> stats = diacritics_stats("بِسْمِ اللَّهِ")
    >>> stats['كسرة']
    3
    """
    result = {}
    for diac in ALL_DIACRITICS:
        count = text.count(diac)
        if count > 0:
            name = DIACRITICS_NAMES.get(diac, f'U+{ord(diac):04X}')
            result[name] = count
    return result


def extract_diacritized_words(text: str) -> list:
    """
    استخراج الكلمات المشكّلة فقط من النص.

    Extract only words that contain diacritics.

    >>> extract_diacritized_words("بِسْمِ الله الرَّحْمَنِ الرحيم")
    ['بِسْمِ', 'الرَّحْمَنِ']
    """
    words = text.split()
    return [w for w in words if has_diacritics(w)]
