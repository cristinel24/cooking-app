from authentication.utils.base_36_convert import base_36_encode
from db.counters_collection import CountersCollection

counters_db = CountersCollection()


def generate_name():
    value = counters_db.get_name_incrementor_value()
    name = base_36_encode(value)
    return name
