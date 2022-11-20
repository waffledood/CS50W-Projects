
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

def categoryDict():
    """
    Returns CATEGORY_CHOICES tuples as a Dictionary.
    """
    return dict((value, option) for value, option in CATEGORY_CHOICES)

def getOption(value):
    """
    Returns the Option for a given Category Value.
    """
    catDict = categoryDict()
    return catDict[value]
