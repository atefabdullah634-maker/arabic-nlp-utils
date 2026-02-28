"""
arabic_nlp_utils.tokenizer
============================
تقطيع النصوص العربية إلى كلمات وجمل وأحرف.

Arabic text tokenization: word, sentence, and character level.
"""

import re

# ───────── Patterns ─────────

WORD_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
SENTENCE_DELIMITERS = re.compile(r'[.!?؟،؛\n]+')

# Common Arabic prefixes and suffixes for basic morphological segmentation
PREFIXES = ['وال', 'فال', 'بال', 'كال', 'لل', 'ال', 'و', 'ف', 'ب', 'ك', 'ل']
SUFFIXES = [
    'هم', 'هن', 'ها', 'كم', 'كن', 'نا', 'ه',
    'ون', 'ين', 'ان', 'ات', 'ية', 'ة', 'ي', 'ك',
]


def word_tokenize(text: str) -> list:
    """
    تقطيع النص إلى كلمات عربية.

    Tokenize text into Arabic words (only Arabic characters).

    >>> word_tokenize("مرحبا بالعالم العربي!")
    ['مرحبا', 'بالعالم', 'العربي']
    """
    return WORD_PATTERN.findall(text)


def simple_word_tokenize(text: str) -> list:
    """
    تقطيع بسيط بناءً على المسافات (يحتفظ بعلامات الترقيم).

    Simple whitespace-based tokenization (keeps punctuation attached).

    >>> simple_word_tokenize("مرحبا بالعالم!")
    ['مرحبا', 'بالعالم!']
    """
    return text.split()


def sentence_tokenize(text: str) -> list:
    """
    تقطيع النص إلى جمل.

    Split text into sentences based on punctuation.

    >>> sentence_tokenize("مرحبا بالعالم. كيف حالك؟ أنا بخير!")
    ['مرحبا بالعالم', 'كيف حالك', 'أنا بخير']
    """
    sentences = SENTENCE_DELIMITERS.split(text)
    return [s.strip() for s in sentences if s.strip()]


def char_tokenize(text: str, include_spaces: bool = False) -> list:
    """
    تقطيع النص إلى أحرف.

    Tokenize text into individual characters.

    Parameters
    ----------
    text : str
        النص.
    include_spaces : bool
        تضمين المسافات (default False).

    >>> char_tokenize("كتاب")
    ['ك', 'ت', 'ا', 'ب']
    """
    if include_spaces:
        return list(text)
    return [c for c in text if c != ' ']


def remove_prefixes(word: str) -> str:
    """
    إزالة السوابق الشائعة من الكلمة (تجزئة مبسطة).

    Remove common prefixes (simplified segmentation).

    >>> remove_prefixes("والكتاب")
    'كتاب'
    >>> remove_prefixes("بالعلم")
    'علم'
    """
    for prefix in PREFIXES:
        if word.startswith(prefix) and len(word) > len(prefix) + 1:
            return word[len(prefix):]
    return word


def remove_suffixes(word: str) -> str:
    """
    إزالة اللواحق الشائعة من الكلمة (تجزئة مبسطة).

    Remove common suffixes (simplified segmentation).

    >>> remove_suffixes("كتابات")
    'كتاب'
    >>> remove_suffixes("مدرسون")
    'مدرس'
    """
    for suffix in SUFFIXES:
        if word.endswith(suffix) and len(word) > len(suffix) + 1:
            return word[:-len(suffix)]
    return word


def segment(word: str) -> dict:
    """
    تجزئة مبسطة للكلمة إلى سابقة + جذع + لاحقة.

    Simple segmentation into prefix + stem + suffix.

    >>> result = segment("والكتابات")
    >>> result['prefix']
    'وال'
    >>> result['stem']
    'كتاب'
    """
    original = word
    prefix = ''
    suffix = ''

    # Try to find prefix
    for p in PREFIXES:
        if word.startswith(p) and len(word) > len(p) + 1:
            prefix = p
            word = word[len(p):]
            break

    # Try to find suffix
    for s in SUFFIXES:
        if word.endswith(s) and len(word) > len(s) + 1:
            suffix = s
            word = word[:-len(s)]
            break

    return {
        'original': original,
        'prefix': prefix,
        'stem': word,
        'suffix': suffix,
    }


def ngrams(text: str, n: int = 2) -> list:
    """
    توليد N-grams من الكلمات.

    Generate word-level N-grams.

    >>> ngrams("أنا أحب اللغة العربية", 2)
    [('أنا', 'أحب'), ('أحب', 'اللغة'), ('اللغة', 'العربية')]
    """
    words = word_tokenize(text)
    return [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]


def char_ngrams(text: str, n: int = 3) -> list:
    """
    توليد N-grams على مستوى الأحرف.

    Generate character-level N-grams.

    >>> char_ngrams("كتاب", 2)
    ['كت', 'تا', 'اب']
    """
    clean = text.replace(' ', '')
    return [clean[i:i + n] for i in range(len(clean) - n + 1)]
