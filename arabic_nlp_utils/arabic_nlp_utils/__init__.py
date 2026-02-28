"""
arabic_nlp_utils
=================
مكتبة شاملة لمعالجة النصوص العربية.

A comprehensive Arabic NLP utilities library for:
- Text cleaning
- Number conversion
- Diacritics handling
- Dialect detection
- Phonetic transliteration
- Text normalization
- Tokenization
- Stopwords filtering
"""

__version__ = '1.0.0'
__author__ = 'Arabic NLP Utils'

# ─── Normalizer ───
from .normalizer import (
    normalize,
    normalize_alef,
    normalize_taa_marbuta,
    normalize_alef_maqsura,
    normalize_hamza,
    remove_tatweel,
)

# ─── Diacritics ───
from .diacritics import (
    remove_diacritics,
    remove_harakat,
    remove_tanween,
    remove_shadda,
    has_diacritics,
    count_diacritics,
    diacritics_stats,
    extract_diacritized_words,
)

# ─── Cleaner ───
from .cleaner import (
    clean_text,
    remove_urls,
    remove_emails,
    remove_mentions,
    remove_hashtags,
    remove_html_tags,
    remove_extra_spaces,
    remove_punctuation,
    remove_non_arabic,
    remove_emojis,
    reduce_repeated_chars,
)

# ─── Numbers ───
from .numbers import (
    to_western_numerals,
    to_arabic_numerals,
    to_eastern_numerals,
    extract_numbers,
    number_to_words,
    words_to_number,
)

# ─── Dialects ───
from .dialects import (
    detect_dialect,
    is_dialect,
    get_dialect_words,
    list_dialects,
)

# ─── Phonetics ───
from .phonetics import (
    to_buckwalter,
    from_buckwalter,
    to_franco,
    to_phonetic,
    transliterate,
)

# ─── Tokenizer ───
from .tokenizer import (
    word_tokenize,
    simple_word_tokenize,
    sentence_tokenize,
    char_tokenize,
    remove_prefixes,
    remove_suffixes,
    segment,
    ngrams,
    char_ngrams,
)

# ─── Stopwords ───
from .stopwords import (
    is_stopword,
    remove_stopwords,
    filter_stopwords,
    get_stopwords,
    add_stopwords,
    remove_from_stopwords,
    stopword_count,
    stopword_ratio,
)
