class Queue:
    def __init__(self, start_size: int = 1):
        self.size = start_size
        self.fill = 0

    def add_request(self) -> bool:
        self.fill += 1
        ret = False
        if self.fill > self.size:
            self.size += 1
            ret = True
        return ret

    def remove_request(self):
        if self.fill > 0:
            self.fill -= 1