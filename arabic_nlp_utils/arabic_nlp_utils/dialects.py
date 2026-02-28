"""
arabic_nlp_utils.dialects
==========================
كشف اللهجات العربية بناءً على كلمات مميزة.

Detect Arabic dialect based on distinctive vocabulary.
Supported dialects: MSA, Egyptian, Gulf, Levantine, Maghrebi, Iraqi.
"""

import re
from collections import Counter

# ───────── Dialect Keyword Lists ─────────

DIALECT_KEYWORDS = {
    'msa': {
        'name_ar': 'الفصحى',
        'name_en': 'Modern Standard Arabic',
        'words': {
            'الذي', 'التي', 'الذين', 'اللذان', 'اللتان',
            'هؤلاء', 'ذلك', 'تلك', 'حيث', 'إذ', 'لكن',
            'بيد', 'غير', 'سوف', 'لن', 'لم', 'ليس',
            'كان', 'أصبح', 'أضحى', 'ظل', 'بات', 'صار',
            'إن', 'أن', 'كأن', 'لعل', 'ليت', 'لكنّ',
            'يجب', 'ينبغي', 'يتعين', 'يتوجب', 'بالتالي',
            'فضلاً', 'علاوة', 'نظراً', 'وفقاً', 'استناداً',
            'يُعد', 'يُعتبر', 'يتضمن', 'يشمل', 'يستلزم',
            'المذكور', 'المشار', 'السالف', 'الآنف',
        }
    },
    'egyptian': {
        'name_ar': 'المصرية',
        'name_en': 'Egyptian',
        'words': {
            'ده', 'دي', 'دول', 'كده', 'ازاي', 'ليه', 'فين',
            'عايز', 'عايزة', 'مش', 'بتاع', 'بتاعت', 'بتاعي',
            'حاجة', 'حاجات', 'كتير', 'اوي', 'خالص', 'بس',
            'يعني', 'طب', 'ماشي', 'تمام', 'حلو', 'بقى',
            'عشان', 'علشان', 'دلوقتي', 'امبارح', 'بكره',
            'ايوه', 'لأ', 'اهو', 'اهي', 'اهم',
            'ايه', 'مين', 'امتى', 'فاكر', 'فاكرة',
            'هنا', 'هناك', 'عندي', 'عندك',
            'بيقول', 'بتقول', 'بنقول', 'هيروح', 'هتيجي',
            'نفسي', 'بأه', 'والنبي', 'يلا', 'خلاص',
        }
    },
    'gulf': {
        'name_ar': 'الخليجية',
        'name_en': 'Gulf',
        'words': {
            'وش', 'ايش', 'شلون', 'ليش', 'وين', 'متى',
            'ابي', 'ابغى', 'يبي', 'يبغى', 'أبا',
            'حق', 'حقي', 'حقك', 'مال', 'مالي',
            'يالله', 'هالحين', 'الحين', 'توه', 'توها',
            'زين', 'حيل', 'وايد', 'مرة', 'هب',
            'جذي', 'كذا', 'هيك', 'اي', 'لا',
            'يمكن', 'خلاص', 'مادري', 'ادري', 'تدري',
            'اكو', 'ماكو', 'شفيك', 'شفيها', 'شسم',
            'يعل', 'طال', 'عساك', 'عساه',
            'بعد', 'عيل', 'هالشكل',
        }
    },
    'levantine': {
        'name_ar': 'الشامية',
        'name_en': 'Levantine',
        'words': {
            'شو', 'كيف', 'وين', 'ليش', 'مين', 'قديش',
            'هلق', 'هلأ', 'هلا', 'لسا', 'بعدين',
            'بدي', 'بدك', 'بدو', 'بدها', 'بدنا',
            'هيك', 'هيدا', 'هيدي', 'هودي', 'هوني',
            'كتير', 'هيدا', 'يعني', 'طيب',
            'منيح', 'حلو', 'زاكي', 'مليح',
            'شب', 'صبية', 'ختيارة', 'زلمة',
            'عنجد', 'والله', 'يلعن',
            'بكير', 'هاللحظة', 'اليوم', 'بكرا',
            'خليني', 'عطيني', 'وريني', 'قلي',
        }
    },
    'maghrebi': {
        'name_ar': 'المغاربية',
        'name_en': 'Maghrebi',
        'words': {
            'واش', 'علاش', 'فاش', 'كيفاش', 'فين', 'شحال',
            'بغيت', 'بغا', 'بغات', 'نبغي', 'تبغي',
            'ديال', 'ديالي', 'ديالك', 'ديالو', 'ديالها',
            'هاد', 'هادي', 'هادو', 'داك', 'ديك',
            'بزاف', 'شوية', 'مزيان', 'واعر', 'خايب',
            'زعما', 'بصح', 'والو', 'حتى',
            'كيدير', 'كيديري', 'كنقول', 'كنمشي',
            'دابا', 'دروك', 'غدا', 'البارح',
            'لابأس', 'يسهل', 'ساهل', 'ماشي',
            'خويا', 'ختي', 'صاحبي', 'لمرا', 'راجل',
        }
    },
    'iraqi': {
        'name_ar': 'العراقية',
        'name_en': 'Iraqi',
        'words': {
            'شلونك', 'شكو', 'ماكو', 'شنو', 'لويش',
            'اريد', 'يريد', 'تريد', 'نريد',
            'هسه', 'هسع', 'هسة',
            'اكو', 'ماكو', 'شكو', 'ماكو',
            'زين', 'حيل', 'هواية', 'كلش',
            'جا', 'راح', 'يمعود', 'ابوي', 'يمه',
            'چان', 'چا', 'گال', 'يگول',
            'خوش', 'باشا', 'اوادم',
            'بالله', 'والله', 'لا', 'اي',
        }
    },
}


def detect_dialect(text: str, top_n: int = 3) -> list:
    """
    كشف اللهجة العربية بناءً على الكلمات المميزة.

    Detect Arabic dialect from text using keyword matching.

    Parameters
    ----------
    text : str
        النص المراد تحليله.
    top_n : int
        عدد أعلى اللهجات المرشحة (default 3).

    Returns
    -------
    list of dict
        قائمة مرتبة بالنتائج، كل عنصر يحتوي:
        - dialect: رمز اللهجة
        - name_ar: الاسم بالعربي
        - name_en: الاسم بالإنجليزي
        - score: درجة التطابق (0-1)
        - matched_words: الكلمات المتطابقة

    >>> results = detect_dialect("انا عايز اروح البيت دلوقتي عشان تعبان اوي")
    >>> results[0]['dialect']
    'egyptian'
    """
    words = set(re.findall(r'[\u0600-\u06FF]+', text))
    scores = []

    for dialect_key, dialect_data in DIALECT_KEYWORDS.items():
        matched = words & dialect_data['words']
        if len(words) > 0:
            score = len(matched) / max(len(words), 1)
        else:
            score = 0.0

        scores.append({
            'dialect': dialect_key,
            'name_ar': dialect_data['name_ar'],
            'name_en': dialect_data['name_en'],
            'score': round(score, 4),
            'matched_words': list(matched),
        })

    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores[:top_n]


def is_dialect(text: str, dialect: str) -> bool:
    """
    فحص هل النص ينتمي للهجة معينة.

    Check if text likely belongs to a specific dialect.

    Parameters
    ----------
    text : str
        النص.
    dialect : str
        رمز اللهجة (egyptian, gulf, levantine, maghrebi, iraqi, msa).

    Returns
    -------
    bool

    >>> is_dialect("انا عايز اروح", "egyptian")
    True
    """
    results = detect_dialect(text, top_n=1)
    if results:
        return results[0]['dialect'] == dialect and results[0]['score'] > 0
    return False


def get_dialect_words(dialect: str) -> set:
    """
    الحصول على قائمة الكلمات المميزة للهجة معينة.

    Get the set of distinctive words for a dialect.

    >>> len(get_dialect_words("egyptian")) > 0
    True
    """
    if dialect in DIALECT_KEYWORDS:
        return DIALECT_KEYWORDS[dialect]['words'].copy()
    raise ValueError(
        f"Unknown dialect '{dialect}'. "
        f"Available: {', '.join(DIALECT_KEYWORDS.keys())}"
    )


def list_dialects() -> list:
    """
    سرد جميع اللهجات المدعومة.

    List all supported dialects.

    >>> dialects = list_dialects()
    >>> len(dialects) >= 6
    True
    """
    return [
        {
            'key': k,
            'name_ar': v['name_ar'],
            'name_en': v['name_en'],
            'word_count': len(v['words']),
        }
        for k, v in DIALECT_KEYWORDS.items()
    ]
