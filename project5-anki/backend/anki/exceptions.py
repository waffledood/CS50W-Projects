class StringLengthTooLongError(Exception):
    def __init__(self, length, max_length):
        self.length = length
        self.max_length = max_length
        super().__init__(
            f"String length {length} exceeds the maximum length of {max_length}"
        )
