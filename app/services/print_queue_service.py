class PrintQueueService:
    def __init__(self):
        self.queue = []

    def add_to_queue(self, item):
        if not any(x['linha'] == item['linha'] for x in self.queue):
            self.queue.append(item)
            return True
        return False

    def clear_queue(self):
        self.queue = []

    def get_queue(self):
        return self.queue

    def queue_count(self):
        return len(self.queue)

    def remove_from_queue(self, linha):
        self.queue = [x for x in self.queue if x['linha'] != linha]
