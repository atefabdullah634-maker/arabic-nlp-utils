# Arabic NLP Utils 🔤

<div dir="rtl">

# مكتبة معالجة النصوص العربية 🔤

مكتبة Python شاملة لمعالجة وتنظيف وتحليل النصوص العربية.

</div>

## ✨ المميزات

| الموديول | الوصف |
|----------|-------|
| 🧹 **تنظيف النصوص** | إزالة الروابط، الإيميلات، المنشنات، HTML، الإيموجي، علامات الترقيم |
| 🔢 **تحويل الأرقام** | تحويل بين أرقام عربية/هندية/غربية + تحويل رقم لكلمات |
| ✏️ **التشكيل** | إزالة/فحص/عد الحركات والتشكيل |
| 🗣️ **كشف اللهجات** | كشف اللهجة (مصري، خليجي، شامي، مغاربي، عراقي، فصحى) |
| 🔊 **الصوتيات** | تحويل Buckwalter / فرانكو / IPA |
| 📐 **التطبيع** | توحيد الألف، التاء المربوطة، إزالة التطويل |
| ✂️ **التقطيع** | تقطيع كلمات وجمل وأحرف + N-grams |
| 🚫 **كلمات التوقف** | قائمة شاملة + تصفية كلمات التوقف |

## 📦 التثبيت

```bash
# من المجلد المحلي
cd arabic_nlp_utils
pip install -e .

# أو مباشرة
pip install arabic-nlp-utils
```

## 🚀 الاستخدام السريع

### تنظيف النصوص
```python
from arabic_nlp_utils import clean_text

text = "مرحبا   بالعالم!! @user https://example.com 😊"
result = clean_text(text)
print(result)  # مرحبا بالعالم
```

### إزالة التشكيل
```python
from arabic_nlp_utils import remove_diacritics, has_diacritics

text = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"
print(remove_diacritics(text))  # بسم الله الرحمن الرحيم
print(has_diacritics(text))     # True
```

### تحويل الأرقام
```python
from arabic_nlp_utils import (
    to_western_numerals, to_arabic_numerals,
    number_to_words, extract_numbers
)

print(to_western_numerals("١٢٣"))     # 123
print(to_arabic_numerals("456"))       # ٤٥٦
print(number_to_words(123))            # مئة وثلاثة وعشرون
print(extract_numbers("لدي ٢٣ كتاب")) # [23]
```

### كشف اللهجات
```python
from arabic_nlp_utils import detect_dialect

text = "انا عايز اروح البيت دلوقتي عشان تعبان اوي"
results = detect_dialect(text)
print(results[0]['name_ar'])  # المصرية
print(results[0]['score'])    # 0.5714
```

### الصوتيات
```python
from arabic_nlp_utils import to_buckwalter, to_franco, from_buckwalter

print(to_buckwalter("بسم الله"))  # bsm Allh
print(to_franco("مرحبا"))         # mr7ba
print(from_buckwalter("bsm"))     # بسم
```

### التطبيع
```python
from arabic_nlp_utils import normalize

text = "أحمد على العــربية"
print(normalize(text))  # احمد علي العربية
```

### التقطيع
```python
from arabic_nlp_utils import word_tokenize, sentence_tokenize, segment

print(word_tokenize("مرحبا بالعالم!"))
# ['مرحبا', 'بالعالم']

print(sentence_tokenize("مرحبا. كيف حالك؟"))
# ['مرحبا', 'كيف حالك']

print(segment("والكتابات"))
# {'original': 'والكتابات', 'prefix': 'وال', 'stem': 'كتاب', 'suffix': 'ات'}
```

### كلمات التوقف
```python
from arabic_nlp_utils import remove_stopwords, is_stopword

text = "أنا ذهبت إلى المدرسة في الصباح"
print(remove_stopwords(text))  # ذهبت المدرسة الصباح
print(is_stopword("في"))       # True
```

## 📋 جميع الدوال المتاحة

### cleaner.py
- `clean_text()` - تنظيف شامل
- `remove_urls()` - إزالة الروابط
- `remove_emails()` - إزالة الإيميلات
- `remove_mentions()` - إزالة المنشنات
- `remove_hashtags()` - إزالة الهاشتاقات
- `remove_html_tags()` - إزالة HTML
- `remove_extra_spaces()` - إزالة المسافات الزائدة
- `remove_punctuation()` - إزالة الترقيم
- `remove_non_arabic()` - إزالة غير العربي
- `remove_emojis()` - إزالة الإيموجي
- `reduce_repeated_chars()` - تقليل التكرار

### numbers.py
- `to_western_numerals()` - تحويل لأرقام غربية
- `to_arabic_numerals()` - تحويل لأرقام عربية
- `to_eastern_numerals()` - تحويل لأرقام شرقية
- `extract_numbers()` - استخراج الأرقام
- `number_to_words()` - رقم إلى كلمات
- `words_to_number()` - كلمات إلى رقم

### diacritics.py
- `remove_diacritics()` - إزالة كل التشكيل
- `remove_harakat()` - إزالة الحركات فقط
- `remove_tanween()` - إزالة التنوين
- `remove_shadda()` - إزالة الشدة
- `has_diacritics()` - فحص وجود تشكيل
- `count_diacritics()` - عد الحركات
- `diacritics_stats()` - إحصائيات التشكيل
- `extract_diacritized_words()` - استخراج الكلمات المشكلة

### dialects.py
- `detect_dialect()` - كشف اللهجة
- `is_dialect()` - فحص لهجة معينة
- `get_dialect_words()` - كلمات اللهجة
- `list_dialects()` - اللهجات المدعومة

### phonetics.py
- `to_buckwalter()` - تحويل Buckwalter
- `from_buckwalter()` - عكس Buckwalter
- `to_franco()` - تحويل فرانكو
- `to_phonetic()` - تحويل صوتي IPA
- `transliterate()` - واجهة موحدة

### normalizer.py
- `normalize()` - تطبيع شامل
- `normalize_alef()` - توحيد الألف
- `normalize_taa_marbuta()` - تطبيع التاء المربوطة
- `normalize_alef_maqsura()` - تطبيع الألف المقصورة
- `normalize_hamza()` - تطبيع الهمزة
- `remove_tatweel()` - إزالة التطويل

### tokenizer.py
- `word_tokenize()` - تقطيع كلمات
- `simple_word_tokenize()` - تقطيع بسيط
- `sentence_tokenize()` - تقطيع جمل
- `char_tokenize()` - تقطيع أحرف
- `remove_prefixes()` - إزالة السوابق
- `remove_suffixes()` - إزالة اللواحق
- `segment()` - تجزئة الكلمة
- `ngrams()` - N-grams كلمات
- `char_ngrams()` - N-grams أحرف

### stopwords.py
- `is_stopword()` - فحص كلمة توقف
- `remove_stopwords()` - إزالة كلمات التوقف
- `filter_stopwords()` - تصفية من قائمة
- `get_stopwords()` - الحصول على القائمة
- `add_stopwords()` - إضافة كلمات
- `remove_from_stopwords()` - حذف كلمات
- `stopword_count()` - عد كلمات التوقف
- `stopword_ratio()` - نسبة كلمات التوقف

## 🧪 تشغيل الاختبارات

```bash
cd arabic_nlp_utils
python -m pytest tests/test_all.py -v
```

## 📄 الرخصة

MIT License

## 🤝 المساهمة

المساهمات مرحب بها! افتح Issue أو Pull Request.
