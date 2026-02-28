"""
اختبارات شاملة لمكتبة arabic_nlp_utils
Comprehensive tests for arabic_nlp_utils library.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from arabic_nlp_utils import (
    # Normalizer
    normalize, normalize_alef, normalize_taa_marbuta,
    normalize_alef_maqsura, normalize_hamza, remove_tatweel,
    # Diacritics
    remove_diacritics, remove_harakat, remove_tanween, remove_shadda,
    has_diacritics, count_diacritics, diacritics_stats,
    extract_diacritized_words,
    # Cleaner
    clean_text, remove_urls, remove_emails, remove_mentions,
    remove_hashtags, remove_html_tags, remove_extra_spaces,
    remove_punctuation, remove_non_arabic, remove_emojis,
    reduce_repeated_chars,
    # Numbers
    to_western_numerals, to_arabic_numerals, to_eastern_numerals,
    extract_numbers, number_to_words, words_to_number,
    # Dialects
    detect_dialect, is_dialect, get_dialect_words, list_dialects,
    # Phonetics
    to_buckwalter, from_buckwalter, to_franco, to_phonetic, transliterate,
    # Tokenizer
    word_tokenize, simple_word_tokenize, sentence_tokenize,
    char_tokenize, remove_prefixes, remove_suffixes, segment,
    ngrams, char_ngrams,
    # Stopwords
    is_stopword, remove_stopwords, filter_stopwords, get_stopwords,
    stopword_count, stopword_ratio,
)


# ════════════════════════════════════════════
#  Normalizer Tests
# ════════════════════════════════════════════

class TestNormalizer:

    def test_normalize_alef(self):
        assert normalize_alef("أحمد إبراهيم آمن") == "احمد ابراهيم امن"

    def test_normalize_taa_marbuta(self):
        assert normalize_taa_marbuta("مدرسة جامعة") == "مدرسه جامعه"

    def test_normalize_alef_maqsura(self):
        assert normalize_alef_maqsura("على موسى") == "علي موسي"

    def test_remove_tatweel(self):
        assert remove_tatweel("العــــربية") == "العربية"
        assert remove_tatweel("حـــروف") == "حروف"

    def test_normalize_hamza(self):
        assert normalize_hamza("مسؤول رئيس") == "مسءول رءيس"

    def test_normalize_pipeline(self):
        result = normalize("أحمد على العــربية")
        assert "ا" in result  # alef normalized
        assert "ـ" not in result  # tatweel removed

    def test_normalize_empty(self):
        assert normalize("") == ""

    def test_normalize_no_arabic(self):
        assert normalize("Hello World") == "Hello World"


# ════════════════════════════════════════════
#  Diacritics Tests
# ════════════════════════════════════════════

class TestDiacritics:

    def test_remove_diacritics(self):
        assert remove_diacritics("بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ") == \
            "بسم الله الرحمن الرحيم"

    def test_remove_harakat(self):
        assert remove_harakat("كَتَبَ") == "كتب"

    def test_remove_tanween(self):
        assert remove_tanween("كتابًا") == "كتابا"

    def test_has_diacritics_true(self):
        assert has_diacritics("بِسْمِ اللَّهِ") is True

    def test_has_diacritics_false(self):
        assert has_diacritics("بسم الله") is False

    def test_count_diacritics(self):
        assert count_diacritics("بِسْمِ") == 3

    def test_diacritics_stats(self):
        stats = diacritics_stats("بِسْمِ اللَّهِ")
        assert 'كسرة' in stats
        assert stats['كسرة'] >= 1

    def test_extract_diacritized_words(self):
        words = extract_diacritized_words("بِسْمِ الله الرَّحْمَنِ الرحيم")
        assert "بِسْمِ" in words
        assert "الله" not in words

    def test_remove_diacritics_empty(self):
        assert remove_diacritics("") == ""


# ════════════════════════════════════════════
#  Cleaner Tests
# ════════════════════════════════════════════

class TestCleaner:

    def test_remove_urls(self):
        text = "زوروا https://example.com للمزيد"
        assert "https://example.com" not in remove_urls(text)

    def test_remove_emails(self):
        text = "تواصل معنا test@example.com"
        assert "test@example.com" not in remove_emails(text)

    def test_remove_mentions(self):
        text = "مرحبا @user كيف حالك"
        assert "@user" not in remove_mentions(text)

    def test_remove_hashtags(self):
        text = "مرحبا #عربي"
        assert "#عربي" not in remove_hashtags(text)

    def test_remove_html_tags(self):
        text = "<p>مرحبا <b>بالعالم</b></p>"
        assert remove_html_tags(text) == "مرحبا بالعالم"

    def test_remove_extra_spaces(self):
        assert remove_extra_spaces("مرحبا    بالعالم") == "مرحبا بالعالم"

    def test_remove_punctuation(self):
        result = remove_punctuation("مرحبا! كيف حالك؟")
        assert "!" not in result
        assert "؟" not in result

    def test_remove_non_arabic(self):
        text = "مرحبا Hello بالعالم World"
        result = remove_non_arabic(text)
        assert "Hello" not in result
        assert "مرحبا" in result

    def test_reduce_repeated_chars(self):
        assert reduce_repeated_chars("هههههه", 2) == "هه"
        assert reduce_repeated_chars("ييييي", 1) == "ي"

    def test_clean_text_pipeline(self):
        text = "مرحبا   بالعالم!! @user https://example.com 😊"
        result = clean_text(text)
        assert "@user" not in result
        assert "https://" not in result
        assert "😊" not in result
        assert "  " not in result  # no double spaces

    def test_clean_text_empty(self):
        assert clean_text("") == ""


# ════════════════════════════════════════════
#  Numbers Tests
# ════════════════════════════════════════════

class TestNumbers:

    def test_to_western_numerals(self):
        assert to_western_numerals("١٢٣") == "123"
        assert to_western_numerals("٤٥٦٧٨٩٠") == "4567890"

    def test_to_arabic_numerals(self):
        assert to_arabic_numerals("123") == "١٢٣"

    def test_to_eastern_numerals(self):
        assert to_eastern_numerals("123") == "۱۲۳"

    def test_extract_numbers(self):
        nums = extract_numbers("لدي ٢٣ تفاحة و 15 برتقالة")
        assert 23 in nums
        assert 15 in nums

    def test_number_to_words_zero(self):
        assert number_to_words(0) == "صفر"

    def test_number_to_words_ones(self):
        assert number_to_words(1) == "واحد"
        assert number_to_words(5) == "خمسة"

    def test_number_to_words_teens(self):
        assert number_to_words(15) == "خمسة عشر"

    def test_number_to_words_tens(self):
        assert number_to_words(20) == "عشرون"

    def test_number_to_words_hundreds(self):
        result = number_to_words(123)
        assert "مئة" in result

    def test_number_to_words_thousands(self):
        result = number_to_words(1000)
        assert "ألف" in result

    def test_number_to_words_negative(self):
        result = number_to_words(-5)
        assert result.startswith("سالب")

    def test_words_to_number(self):
        assert words_to_number("ثلاثة") == 3
        assert words_to_number("صفر") == 0
        assert words_to_number("خمسة عشر") == 15

    def test_mixed_digits(self):
        text = "العدد ١٢٣ أو ۴۵۶"
        result = to_western_numerals(text)
        assert "123" in result
        assert "456" in result


# ════════════════════════════════════════════
#  Dialects Tests
# ════════════════════════════════════════════

class TestDialects:

    def test_detect_egyptian(self):
        text = "انا عايز اروح البيت دلوقتي عشان تعبان اوي"
        results = detect_dialect(text)
        assert results[0]['dialect'] == 'egyptian'
        assert results[0]['score'] > 0

    def test_detect_gulf(self):
        text = "وش تبي الحين وين رايح"
        results = detect_dialect(text)
        assert results[0]['dialect'] == 'gulf'

    def test_detect_levantine(self):
        text = "شو بدك هلق كتير منيح"
        results = detect_dialect(text)
        assert results[0]['dialect'] == 'levantine'

    def test_detect_maghrebi(self):
        text = "واش بغيت ديالي بزاف مزيان"
        results = detect_dialect(text)
        assert results[0]['dialect'] == 'maghrebi'

    def test_is_dialect(self):
        assert is_dialect("انا عايز اروح", "egyptian") is True

    def test_list_dialects(self):
        dialects = list_dialects()
        assert len(dialects) >= 6
        names = [d['key'] for d in dialects]
        assert 'egyptian' in names
        assert 'gulf' in names

    def test_get_dialect_words(self):
        words = get_dialect_words("egyptian")
        assert len(words) > 0
        assert "عايز" in words

    def test_invalid_dialect(self):
        with pytest.raises(ValueError):
            get_dialect_words("unknown_dialect")

    def test_empty_text(self):
        results = detect_dialect("")
        assert len(results) > 0


# ════════════════════════════════════════════
#  Phonetics Tests
# ════════════════════════════════════════════

class TestPhonetics:

    def test_to_buckwalter(self):
        assert to_buckwalter("بسم الله") == "bsm Allh"

    def test_from_buckwalter(self):
        assert from_buckwalter("bsm Allh") == "بسم الله"

    def test_buckwalter_roundtrip(self):
        original = "كتاب"
        assert from_buckwalter(to_buckwalter(original)) == original

    def test_to_franco(self):
        result = to_franco("مرحبا")
        assert result == "mr7ba"

    def test_to_franco_with_7(self):
        result = to_franco("حب")
        assert "7" in result

    def test_to_phonetic(self):
        result = to_phonetic("كتب")
        assert result == "ktb"

    def test_transliterate_buckwalter(self):
        assert transliterate("بسم", "buckwalter") == "bsm"

    def test_transliterate_franco(self):
        assert transliterate("مرحبا", "franco") == "mr7ba"

    def test_transliterate_invalid(self):
        with pytest.raises(ValueError):
            transliterate("مرحبا", "invalid_system")


# ════════════════════════════════════════════
#  Tokenizer Tests
# ════════════════════════════════════════════

class TestTokenizer:

    def test_word_tokenize(self):
        tokens = word_tokenize("مرحبا بالعالم العربي!")
        assert tokens == ['مرحبا', 'بالعالم', 'العربي']

    def test_simple_word_tokenize(self):
        tokens = simple_word_tokenize("مرحبا بالعالم!")
        assert tokens == ['مرحبا', 'بالعالم!']

    def test_sentence_tokenize(self):
        text = "مرحبا بالعالم. كيف حالك؟ أنا بخير!"
        sents = sentence_tokenize(text)
        assert len(sents) == 3

    def test_char_tokenize(self):
        assert char_tokenize("كتاب") == ['ك', 'ت', 'ا', 'ب']

    def test_char_tokenize_with_spaces(self):
        result = char_tokenize("ك ت", include_spaces=True)
        assert ' ' in result

    def test_remove_prefixes(self):
        assert remove_prefixes("والكتاب") == "كتاب"
        assert remove_prefixes("بالعلم") == "علم"

    def test_remove_suffixes(self):
        assert remove_suffixes("كتابات") == "كتاب"
        assert remove_suffixes("مدرسون") == "مدرس"

    def test_segment(self):
        result = segment("والكتابات")
        assert result['prefix'] == "وال"
        assert result['stem'] == "كتاب"
        assert result['suffix'] == "ات"

    def test_ngrams(self):
        result = ngrams("أنا أحب اللغة العربية", 2)
        assert len(result) == 3
        assert result[0] == ('أنا', 'أحب')

    def test_char_ngrams(self):
        result = char_ngrams("كتاب", 2)
        assert result == ['كت', 'تا', 'اب']

    def test_word_tokenize_empty(self):
        assert word_tokenize("") == []


# ════════════════════════════════════════════
#  Stopwords Tests
# ════════════════════════════════════════════

class TestStopwords:

    def test_is_stopword(self):
        assert is_stopword("في") is True
        assert is_stopword("كتاب") is False

    def test_remove_stopwords(self):
        text = "أنا ذهبت إلى المدرسة في الصباح"
        result = remove_stopwords(text)
        assert "أنا" not in result
        assert "في" not in result
        assert "المدرسة" in result

    def test_filter_stopwords(self):
        words = ["أنا", "أحب", "اللغة", "العربية"]
        filtered = filter_stopwords(words)
        assert "أنا" not in filtered
        assert "أحب" in filtered

    def test_get_stopwords(self):
        sw = get_stopwords()
        assert len(sw) > 100
        assert "في" in sw
        assert "من" in sw

    def test_stopword_count(self):
        text = "أنا ذهبت إلى المدرسة في الصباح"
        count = stopword_count(text)
        assert count >= 3

    def test_stopword_ratio(self):
        text = "أنا ذهبت إلى المدرسة"
        ratio = stopword_ratio(text)
        assert 0.0 <= ratio <= 1.0

    def test_stopword_ratio_empty(self):
        assert stopword_ratio("") == 0.0


# ════════════════════════════════════════════
#  Integration Tests
# ════════════════════════════════════════════

class TestIntegration:
    """Test that modules work together."""

    def test_clean_and_tokenize(self):
        text = "مرحبا!! @user https://x.com بالعالم العربي 😊"
        cleaned = clean_text(text)
        tokens = word_tokenize(cleaned)
        assert len(tokens) >= 2

    def test_clean_and_stopwords(self):
        text = "أنا أحب اللغة العربية في كل مكان"
        cleaned = clean_text(text, remove_diacritics_flag=False)
        result = remove_stopwords(cleaned)
        assert "أنا" not in result
        assert "في" not in result

    def test_normalize_and_diacritics(self):
        text = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"
        no_diac = remove_diacritics(text)
        normalized = normalize(no_diac)
        assert "ِ" not in normalized
        assert "ـ" not in normalized

    def test_numbers_and_clean(self):
        text = "لدي ٢٣ تفاحة و١٥ برتقالة"
        western = to_western_numerals(text)
        nums = extract_numbers(western)
        assert 23 in nums
        assert 15 in nums

    def test_dialect_on_cleaned_text(self):
        text = "انا عايز اروح البيت @home دلوقتي"
        cleaned = clean_text(text)
        results = detect_dialect(cleaned)
        assert results[0]['dialect'] == 'egyptian'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
