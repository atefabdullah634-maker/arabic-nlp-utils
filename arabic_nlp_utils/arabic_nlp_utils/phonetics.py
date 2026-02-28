"""
arabic_nlp_utils.phonetics
============================
تحويل صوتيات النصوص العربية (Buckwalter / Franco-Arab / IPA-like).

Arabic phonetic transliteration: Buckwalter, Arabizi (Franco), and simple IPA.
"""

# ───────── Buckwalter Transliteration ─────────

_BUCKWALTER_MAP = {
    'ء': "'", 'آ': '|', 'أ': '>', 'ؤ': '&', 'إ': '<',
    'ئ': '}', 'ا': 'A', 'ب': 'b', 'ة': 'p', 'ت': 't',
    'ث': 'v', 'ج': 'j', 'ح': 'H', 'خ': 'x', 'د': 'd',
    'ذ': '*', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': '$',
    'ص': 'S', 'ض': 'D', 'ط': 'T', 'ظ': 'Z', 'ع': 'E',
    'غ': 'g', 'ف': 'f', 'ق': 'q', 'ك': 'k', 'ل': 'l',
    'م': 'm', 'ن': 'n', 'ه': 'h', 'و': 'w', 'ي': 'y',
    'ى': 'Y', 'َ': 'a', 'ُ': 'u', 'ِ': 'i', 'ّ': '~',
    'ْ': 'o', 'ً': 'F', 'ٌ': 'N', 'ٍ': 'K',
    'ٰ': '`', 'ٓ': '#',
}

_BUCKWALTER_REVERSE = {v: k for k, v in _BUCKWALTER_MAP.items()}


def to_buckwalter(text: str) -> str:
    """
    تحويل النص العربي إلى ترميز Buckwalter.

    Convert Arabic text to Buckwalter transliteration.

    >>> to_buckwalter("بسم الله")
    'bsm Allh'
    """
    return ''.join(_BUCKWALTER_MAP.get(c, c) for c in text)


def from_buckwalter(text: str) -> str:
    """
    تحويل ترميز Buckwalter إلى عربي.

    Convert Buckwalter transliteration back to Arabic.

    >>> from_buckwalter("bsm Allh")
    'بسم الله'
    """
    return ''.join(_BUCKWALTER_REVERSE.get(c, c) for c in text)


# ───────── Franco-Arab (Arabizi) ─────────

_FRANCO_MAP = {
    'ء': '2', 'آ': '2a', 'أ': '2', 'ؤ': '2', 'إ': '2',
    'ئ': '2', 'ا': 'a', 'ب': 'b', 'ة': 'a', 'ت': 't',
    'ث': 'th', 'ج': 'g', 'ح': '7', 'خ': '5', 'د': 'd',
    'ذ': 'z', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh',
    'ص': 's', 'ض': 'd', 'ط': 't', 'ظ': 'z', 'ع': '3',
    'غ': '3\'', 'ف': 'f', 'ق': '2', 'ك': 'k', 'ل': 'l',
    'م': 'm', 'ن': 'n', 'ه': 'h', 'و': 'w', 'ي': 'y',
    'ى': 'a',
    # Diacritics
    'َ': 'a', 'ُ': 'o', 'ِ': 'e', 'ّ': '', 'ْ': '',
    'ً': 'an', 'ٌ': 'on', 'ٍ': 'en',
}


def to_franco(text: str) -> str:
    """
    تحويل النص العربي إلى فرانكو آراب (عربيزي).

    Convert Arabic text to Franco-Arab (Arabizi) representation.

    >>> to_franco("مرحبا")
    'mr7ba'
    >>> to_franco("كيف حالك")
    'kyf 7alk'
    """
    return ''.join(_FRANCO_MAP.get(c, c) for c in text)


# ───────── Simple Phonetic (IPA-like) ─────────

_PHONETIC_MAP = {
    'ء': 'ʔ', 'آ': 'ʔaː', 'أ': 'ʔ', 'ؤ': 'ʔ', 'إ': 'ʔi',
    'ئ': 'ʔ', 'ا': 'aː', 'ب': 'b', 'ة': 'a', 'ت': 't',
    'ث': 'θ', 'ج': 'dʒ', 'ح': 'ħ', 'خ': 'x', 'د': 'd',
    'ذ': 'ð', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'ʃ',
    'ص': 'sˤ', 'ض': 'dˤ', 'ط': 'tˤ', 'ظ': 'ðˤ', 'ع': 'ʕ',
    'غ': 'ɣ', 'ف': 'f', 'ق': 'q', 'ك': 'k', 'ل': 'l',
    'م': 'm', 'ن': 'n', 'ه': 'h', 'و': 'w', 'ي': 'j',
    'ى': 'aː',
    'َ': 'a', 'ُ': 'u', 'ِ': 'i', 'ّ': 'ː', 'ْ': '',
    'ً': 'an', 'ٌ': 'un', 'ٍ': 'in',
}


def to_phonetic(text: str) -> str:
    """
    تحويل النص العربي إلى تمثيل صوتي مبسط (IPA-like).

    Convert Arabic text to simplified IPA-like phonetic representation.

    >>> to_phonetic("كتب")
    'ktb'
    """
    return ''.join(_PHONETIC_MAP.get(c, c) for c in text)


# ───────── Utility Functions ─────────

def transliterate(text: str, system: str = 'buckwalter') -> str:
    """
    واجهة موحدة للتحويل الصوتي.

    Unified transliteration interface.

    Parameters
    ----------
    text : str
        النص العربي.
    system : str
        نظام التحويل: 'buckwalter', 'franco', or 'phonetic'.

    Returns
    -------
    str
        النص بعد التحويل.

    >>> transliterate("مرحبا", "franco")
    'mr7ba'
    """
    systems = {
        'buckwalter': to_buckwalter,
        'franco': to_franco,
        'phonetic': to_phonetic,
    }
    if system not in systems:
        raise ValueError(
            f"Unknown system '{system}'. "
            f"Available: {', '.join(systems.keys())}"
        )
    return systems[system](text)
