#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Code tables
"""

# an (incomplete) list of ISO 639-3 language codes. these codes are used in Extended Open Multilingual Wordnet
# (see e.g. http://compling.hss.ntu.edu.sg/omw/summx.html) and in Tesseract (see e.g.
# https://github.com/tesseract-ocr/tessdata). For the complete list, see http://www-01.sil.org/iso639-3/codes.asp

iso639_3 = {
    'Afar': 'aar',
    'Afrikaans': 'afr',
    'Akan': 'aka',
    'Albanian': 'als',
    'Amharic': 'amh',
    'Old English': 'ang',
    'Arabic': 'arb',
    'Egyptian Arabic': 'arz',
    'Assamese': 'asm',
    'Asturian': 'ast',
    'Azerbaijani': 'aze',
    'Bambara': 'bam',
    'Belarusian': 'bel',
    'Bengali': 'ben',
    'Tibetan': 'bod',
    'Bosnian': 'bos',
    'Breton': 'bre',
    'Bulgarian': 'bul',
    'Catalan': 'cat',
    'Czech': 'ces',
    'Cherokee': 'chr',
    'Simplified Chinese': 'cmn',
    'Cornish': 'cor',
    'Welsh': 'cym',
    'Danish': 'dan',
    'German': 'deu',
    'Dzongkha': 'dzo',
    'Greek': 'ell',
    'English': 'eng',
    'Esperanto': 'epo',
    'Estonian': 'est',
    'Basque': 'eus',
    'Ewe': 'ewe',
    'Faroese': 'fao',
    'Farsi': 'fas',
    'Finnish': 'fin',
    'French': 'fra',
    'Western Frisian': 'fry',
    'Fulah': 'ful',
    'Friulian': 'fur',
    'Scottish Gaelic': 'gla',
    'Irish': 'gle',
    'Galician': 'glg',
    'Manx': 'glv',
    'Ancient Greek': 'grc',
    'Gujarati': 'guj',
    'Haitian': 'hat',
    'Hausa': 'hau',
    'Serbo-Croatian': 'hbs',
    'Hebrew': 'heb',
    'Hindi': 'hin',
    'Croatian': 'hrv',
    'Hungarian': 'hun',
    'Armenian': 'hye',
    'Igbo': 'ibo',
    'Ido': 'ido',
    'Sichuan Yi': 'iii',
    'Interlingua': 'ina',
    'Indonesian': 'ind',
    'Icelandic': 'isl',
    'Italian': 'ita',
    'Japanese': 'jpn',
    'Kalaallisut': 'kal',
    'Kannada': 'kan',
    'Georgian': 'kat',
    'Kazakh': 'kaz',
    'Central Khmer': 'khm',
    'Kikuyu': 'kik',
    'Kinyarwanda': 'kin',
    'Kirghiz': 'kir',
    'Korean': 'kor',
    'Kurdish': 'kur',
    'Lao': 'lao',
    'Latin': 'lat',
    'Latvian': 'lav',
    'Lingala': 'lin',
    'Lithuanian': 'lit',
    'Latgalian': 'ltg',
    'Luxembourgish': 'ltz',
    'Luba-Katanga': 'lub',
    'Ganda': 'lug',
    'Malayalam': 'mal',
    'Marathi': 'mar',
    'Macedonian': 'mkd',
    'Malagasy': 'mlg',
    'Maltese': 'mlt',
    'Mongolian': 'mon',
    'Maori': 'mri',
    'Burmese': 'mya',
    'Min Nan Chinese': 'nan',
    'Navajo': 'nav',
    'South Ndebele': 'nbl',
    'North Ndebele': 'nde',
    'Nepali': 'nep',
    'Dutch': 'nld',
    'Nynorsk': 'nno',
    'Bokmål': 'nob',
    'Occitan': 'oci',
    'Oriya': 'ori',
    'Oromo': 'orm',
    'Panjabi': 'pan',
    'Polish': 'pol',
    'Portuguese': 'por',
    'Pushto': 'pus',
    'Traditional Chinese': 'qcn',
    'Romansh': 'roh',
    'Romanian': 'ron',
    'Rundi': 'run',
    'Macedo-Romanian': 'rup',
    'Russian': 'rus',
    'Sango': 'sag',
    'Sanskrit': 'san',
    'Sicilian': 'scn',
    'Sinhala': 'sin',
    'Slovak': 'slk',
    'Slovene': 'slv',
    'Northern Sami': 'sme',
    'Shona': 'sna',
    'Somali': 'som',
    'Southern Sotho': 'sot',
    'Spanish': 'spa',
    'Sardinian': 'srd',
    'Serbian': 'srp',
    'Swati': 'ssw',
    'Swahili': 'swa',
    'Swedish': 'swe',
    'Tamil': 'tam',
    'Tatar': 'tat',
    'Telugu': 'tel',
    'Tajik': 'tgk',
    'Tagalog': 'tgl',
    'Thai': 'tha',
    'Tigrinya': 'tir',
    'Tonga': 'ton',
    'Tswana': 'tsn',
    'Tsonga': 'tso',
    'Turkmen': 'tuk',
    'Turkish': 'tur',
    'Ukrainian': 'ukr',
    'Urdu': 'urd',
    'Uzbek': 'uzb',
    'Venda': 'ven',
    'Vietnamese': 'vie',
    'Volapük': 'vol',
    'Xhosa': 'xho',
    'Yiddish': 'yid',
    'Yoruba': 'yor',
    'Yue Chinese': 'yue',
    'Malaysian': 'zsm',
    'Zulu': 'zul',
}

unit_short_term = {
    'Meters':'m',
    "Centimeters":'cm',
    'Kilogram':'kg',
    }