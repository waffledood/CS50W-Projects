
BEAUTY = 'BT'
AUTOMOTIVE = 'AM'
ELECTRONICS = 'ER'
KIDS = 'KD'
BOOKS = 'BK'
MISC = 'MS'
CATEGORY_CHOICES = [
    (BEAUTY, 'Beauty'),
    (AUTOMOTIVE, 'Automotive'),
    (ELECTRONICS, 'Electronics'),
    (KIDS, 'Kids'),
    (BOOKS, 'Books'),
    (MISC, 'Misc'),
]
CATEGORY_VALUES = [values for (values, _) in CATEGORY_CHOICES]
CATEGORY_OPTIONS = [options for (_, options) in CATEGORY_CHOICES]
