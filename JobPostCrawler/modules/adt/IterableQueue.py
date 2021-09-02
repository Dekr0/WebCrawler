import queue


class IterableQueue(queue.Queue):

    def __init__(self):
        super(IterableQueue, self).__init__()

    def __len__(self):
        return self.qsize()

    def __iter__(self):
        return self

    def __next__(self):
        if self.empty():
            raise StopIteration()
        else:
            return self.get()