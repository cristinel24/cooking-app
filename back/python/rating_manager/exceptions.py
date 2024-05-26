class InternalError(Exception):
    def __init__(self):
        self.value = 20500


class ExternalError(Exception):
    def __init__(self):
        self.value = 20520


class DatabaseError(Exception):
    def __init__(self):
        self.value = 20540


class DatabaseNotFoundDataError(Exception):
    def __init__(self):
        self.value = 20544


class InvalidDataError(Exception):
    def __init__(self):
        self.value = 20580
