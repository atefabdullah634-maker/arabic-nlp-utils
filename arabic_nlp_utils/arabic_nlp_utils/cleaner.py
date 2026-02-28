"""
arabic_nlp_utils.cleaner
=========================
تنظيف النصوص العربية من الشوائب.

Clean Arabic text by removing URLs, emails, mentions, HTML tags,
extra whitespace, and non-Arabic characters.
"""

import re
from .diacritics import remove_diacritics
from .normalizer import normalize, remove_tatweel

# ───────── Patterns ─────────

URL_PATTERN = re.compile(
    r'https?://\S+|www\.\S+|ftp://\S+', re.IGNORECASE
)
EMAIL_PATTERN = re.compile(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
)
MENTION_PATTERN = re.compile(r'@\w+')
HASHTAG_PATTERN = re.compile(r'#\w+', re.UNICODE)
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
EXTRA_SPACES = re.compile(r'\s+')
NEWLINES = re.compile(r'[\r\n]+')
PUNCTUATION_PATTERN = re.compile(
    r'[!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~'
    r'،؛؟٪٫٬«»…––]'
)
NON_ARABIC_PATTERN = re.compile(
    r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF'
    r'\uFB50-\uFDFF\uFE70-\uFEFF\s\d]'
)
EMOJIS_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE,
)
REPEATED_CHARS = re.compile(r'(.)\1{2,}')


def remove_urls(text: str) -> str:
    """إزالة الروابط (URLs) من النص."""
    return URL_PATTERN.sub('', text)


def remove_emails(text: str) -> str:
    """إزالة عناوين البريد الإلكتروني."""
    return EMAIL_PATTERN.sub('', text)


def remove_mentions(text: str) -> str:
    """إزالة المنشنات (@username)."""
    return MENTION_PATTERN.sub('', text)


def remove_hashtags(text: str) -> str:
    """إزالة الهاشتاقات (#tag)."""
    return HASHTAG_PATTERN.sub('', text)


def remove_html_tags(text: str) -> str:
    """إزالة وسوم HTML."""
    return HTML_TAG_PATTERN.sub('', text)


def remove_extra_spaces(text: str) -> str:
    """إزالة المسافات الزائدة وتوحيدها."""
    return EXTRA_SPACES.sub(' ', text).strip()


def remove_punctuation(text: str) -> str:
    """إزالة علامات الترقيم العربية والإنجليزية."""
    return PUNCTUATION_PATTERN.sub('', text)


def remove_non_arabic(text: str) -> str:
    """
    إزالة جميع الأحرف غير العربية (مع الاحتفاظ بالمسافات والأرقام).

    Remove all non-Arabic characters (keeps spaces and digits).
    """
    return NON_ARABIC_PATTERN.sub('', text)


def remove_emojis(text: str) -> str:
    """إزالة الرموز التعبيرية (Emojis)."""
    return EMOJIS_PATTERN.sub('', text)


def reduce_repeated_chars(text: str, max_repeat: int = 2) -> str:
    """
    تقليل الأحرف المكررة (مثلاً: "هههههه" → "هه").

    Reduce consecutive repeated characters to at most `max_repeat`.

    >>> reduce_repeated_chars("هههههه", 2)
    'هه'
    """
    return re.sub(r'(.)\1{' + str(max_repeat) + r',}',
                  r'\1' * max_repeat, text)


def clean_text(text: str,
               remove_urls_flag: bool = True,
               remove_emails_flag: bool = True,
               remove_mentions_flag: bool = True,
               remove_hashtags_flag: bool = True,
               remove_html_flag: bool = True,
               remove_emojis_flag: bool = True,
               remove_punctuation_flag: bool = True,
               remove_diacritics_flag: bool = True,
               normalize_flag: bool = True,
               remove_tatweel_flag: bool = True,
               keep_only_arabic: bool = False) -> str:
    """
    تنظيف شامل للنص العربي مع التحكم في كل خطوة.

    Full cleaning pipeline with per-step control.

    Parameters
    ----------
    text : str
        النص المراد تنظيفه.
    remove_urls_flag : bool
        إزالة الروابط.
    remove_emails_flag : bool
        إزالة الإيميلات.
    remove_mentions_flag : bool
        إزالة المنشنات.
    remove_hashtags_flag : bool
        إزالة الهاشتاقات.
    remove_html_flag : bool
        إزالة وسوم HTML.
    remove_emojis_flag : bool
        إزالة الإيموجي.
    remove_punctuation_flag : bool
        إزالة علامات الترقيم.
    remove_diacritics_flag : bool
        إزالة التشكيل.
    normalize_flag : bool
        تطبيع النص.
    remove_tatweel_flag : bool
        إزالة التطويل.
    keep_only_arabic : bool
        الاحتفاظ فقط بالأحرف العربية.

    Returns
    -------
    str
        النص بعد التنظيف.

    >>> clean_text("مرحبا   بالعالم!! @user https://example.com 😊")
    'مرحبا بالعالم'
    """
    if remove_html_flag:
        text = remove_html_tags(text)
    if remove_urls_flag:
        text = remove_urls(text)
    if remove_emails_flag:
        text = remove_emails(text)
    if remove_mentions_flag:
        text = remove_mentions(text)
    if remove_hashtags_flag:
        text = remove_hashtags(text)
    if remove_emojis_flag:
        text = remove_emojis(text)
    if remove_diacritics_flag:
        text = remove_diacritics(text)
    if normalize_flag:
        text = normalize(text)
    if remove_tatweel_flag:
        text = remove_tatweel(text)
    if remove_punctuation_flag:
        text = remove_punctuation(text)
    if keep_only_arabic:
        text = remove_non_arabic(text)

    text = remove_extra_spaces(text)
    return text
