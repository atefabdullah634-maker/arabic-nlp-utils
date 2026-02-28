"""
arabic_nlp_utils.normalizer
===========================
تطبيع النصوص العربية - توحيد الأحرف المتشابهة وإزالة التطويل.

Arabic text normalization - unify similar characters and remove tatweel.
"""

import re

# ───────── Character Maps ─────────

ALEF_VARIANTS = re.compile(r'[إأآٱٲٳا]')
TAA_MARBUTA = re.compile(r'ة')
ALEF_MAQSURA = re.compile(r'ى')
TATWEEL = re.compile(r'ـ+')
HAMZA_ABOVE = re.compile(r'[ؤئ]')


def normalize_alef(text: str) -> str:
    """
    توحيد جميع أشكال الألف إلى (ا).

    Normalize all Alef variants (أ إ آ ٱ ٲ ٳ) to plain Alef (ا).

    >>> normalize_alef("أحمد إبراهيم آمن")
    'احمد ابراهيم امن'
    """
    return ALEF_VARIANTS.sub('ا', text)


def normalize_taa_marbuta(text: str) -> str:
    """
    تحويل التاء المربوطة (ة) إلى هاء (ه).

    Normalize Taa Marbuta (ة) to Haa (ه).

    >>> normalize_taa_marbuta("مدرسة جامعة")
    'مدرسه جامعه'
    """
    return TAA_MARBUTA.sub('ه', text)


def normalize_alef_maqsura(text: str) -> str:
    """
    تحويل الألف المقصورة (ى) إلى ياء (ي).

    Normalize Alef Maqsura (ى) to Yaa (ي).

    >>> normalize_alef_maqsura("على موسى")
    'علي موسي'
    """
    return ALEF_MAQSURA.sub('ي', text)


def remove_tatweel(text: str) -> str:
    """
    إزالة التطويل (الكشيدة) من النص.

    Remove Tatweel/Kashida (ـ) characters.

    >>> remove_tatweel("العــــربية")
    'العربية'
    """
    return TATWEEL.sub('', text)


def normalize_hamza(text: str) -> str:
    """
    تطبيع الهمزة على الواو والياء.

    Normalize Hamza on Waw (ؤ) and Yaa (ئ) to plain Hamza (ء).

    >>> normalize_hamza("مسؤول رئيس")
    'مسءول رءيس'
    """
    return HAMZA_ABOVE.sub('ء', text)


def normalize(text: str,
              alef: bool = True,
              taa_marbuta: bool = False,
              alef_maqsura: bool = True,
              tatweel: bool = True,
              hamza: bool = False) -> str:
    """
    تطبيع شامل للنص العربي مع التحكم في كل خطوة.

    Full normalization pipeline with per-step control.

    Parameters
    ----------
    text : str
        النص المراد تطبيعه.
    alef : bool
        توحيد أشكال الألف (default True).
    taa_marbuta : bool
        تحويل التاء المربوطة لهاء (default False).
    alef_maqsura : bool
        تحويل الألف المقصورة لياء (default True).
    tatweel : bool
        إزالة التطويل (default True).
    hamza : bool
        تطبيع الهمزة (default False).

    Returns
    -------
    str
        النص بعد التطبيع.

    >>> normalize("أحمد على العــربية")
    'احمد علي العربية'
    """
    if alef:
        text = normalize_alef(text)
    if taa_marbuta:
        text = normalize_taa_marbuta(text)
    if alef_maqsura:
        text = normalize_alef_maqsura(text)
    if tatweel:
        text = remove_tatweel(text)
    if hamza:
        text = normalize_hamza(text)
    return text
