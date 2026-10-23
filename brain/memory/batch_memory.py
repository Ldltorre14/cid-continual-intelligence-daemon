from collections import deque 
from dataclasses import dataclass, field
import logging 
import torch
import numpy as np
from schemas.memory_schemas import InferenceSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("memory")


class BatchMemory:
    def __init__(self, memory_size: int = 100, batch_size: int = 5):
        self.memory_size = memory_size
        self.batch_size = batch_size   # Batch size should be at least bigger than 100 as this batch will then be split into mini batches
        
        self.full = False
        self.processed_batches: list[InferenceSchema] = []
        self.memory_batch: list[InferenceSchema] = []       
    
    def get_buffer_status(self):
        return self.full
    
    def generate_minibatches(self):
        pass
        
    
    def reset_batch(self):
        logger.info("Memory buffer was reset")
        self.memory_batch = []

        self.full = False 
    
    def store_inference(self, inference_record: InferenceSchema):
        logger.info("Appending a memory unit to the memory buffer")
        self.memory_batch.append(inference_record)
        
        if len(self.memory_batch) == self.memory_size:
            self.full = True
    
    def get_generalized_advantage_estimation(self, next_value, gamma_value, lambda_value):
        advantages = []
        target_returns = []
        running_advantage = 0
        rewards, values = torch.tensor(self.rewards), torch.tensor(self.values)

        for t in range(len(self.rewards) - 1, -1, -1):
            td_error = rewards[t] + (gamma_value * next_value) - values[t]
            advantage_t = td_error + (gamma_value * lambda_value * running_advantage) 

            running_advantage = advantage_t
            next_value = values[t]

            advantages.append(advantage_t)
            target_returns.append(advantage_t + values[t])
        
        return target_returns[::-1], advantages[::-1]        
    


            
            
