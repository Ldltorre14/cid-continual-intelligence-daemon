from brain.rl_agent.ppo_model import PPONetwork
from memory.batch_memory import BatchMemory
from schemas.memory_schemas import InferenceSchema

from torch import nn
import torch 
import logging 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ppo_agent")


class PPOAgent:
    def __init__(self, in_embed_dim: int, out_embed_dim: int):
        self.ppo_network = PPONetwork(in_embed_dim=in_embed_dim, out_embed_dim=out_embed_dim)
        self.memory = BatchMemory(batch_size=10)
    
    def store_memory(self, inference_record: InferenceSchema):
        logger.info("Storing Inference memory for the PPOAgent")
        self.memory.store_inference(inference_record=inference_record)

    def select_action(self, state_embedding):
        with torch.no_grad():
            dist, value = self.ppo_network(state_embedding)
            
            action = dist.sample()
            log_prob = dist.log_prob(action)

        return action.item(), log_prob, value