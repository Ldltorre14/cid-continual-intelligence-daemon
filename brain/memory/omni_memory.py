from collections import deque
from schemas.memory_schemas import InferenceSchema



class OmniMemoryModule:
    
    def __init__(self, memory_size):
        self.storage = deque(maxlen=memory_size)

    def get_count(self):
        return len(self.storage)

    def store_memory(self, inference: InferenceSchema):
        self.storage.append(inference)
        

    def retrieve_memory(self):
        pass