from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="arabic-nlp-utils",
    version="1.0.0",
    author="Arabic NLP Utils",
    description="مكتبة شاملة لمعالجة النصوص العربية - Comprehensive Arabic NLP utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arabic-nlp-utils/arabic-nlp-utils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Arabic",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "pytest-cov"],
    },
    keywords=[
        "arabic", "nlp", "text-processing", "arabic-nlp",
        "diacritics", "tashkeel", "transliteration", "buckwalter",
        "dialect-detection", "tokenizer", "stopwords", "normalization",
    ],
)
