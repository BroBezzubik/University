class Reflector(object):
    def __init__(self):
        self.reflector = None

    @staticmethod
    def generate_reflector(count_elements):
        tmp_reflector = {}
        list = range(count_elements)

