from brain.sentence_encoder import PerceptionModel
from brain.rl_agent.ppo_agent import PPOAgent
from memory.omni_memory import OmniMemoryModule
from schemas.memory_schemas import InferenceSchema

from datetime import datetime
import torch 
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cid_core")


class CID:
    def __init__(self, 
                 encoder_model_name: str, 
                 in_embedding_dim: int = 768,
                 out_embedding_dim: int = 3,
                 device: str = "cuda" if torch.cuda.is_available() else "cpu",
                 backend: str = "torch",
                 model_kwargs: dict = {"dtype": "float32"}):
        
        self.long_memory = OmniMemoryModule(
            memory_size = 10000
        )

        self.encoder = PerceptionModel(
            device = device,
            model_name = encoder_model_name,
            backend = backend, 
            model_kwargs = model_kwargs
        )
        
        self.agent = PPOAgent(
            in_embed_dim = in_embedding_dim,
            out_embed_dim = out_embedding_dim
        )
        
        self._start_up()
    
    
    def _start_up(self):
        logger.info("Initializing all the modules for CID...")
        self.encoder.start_up()

    def _store_memory(self, inference: InferenceSchema):
        logger.info("Storing current inference step into the memory modules...")
        self.long_memory.store_memory(inference = inference)
        self.agent.store_memory(inference_record = inference)

    
    def _read_command(self, command: str):
        try:
            logger.info("R...")
            encoded = self.encoder.encode_command(command=command)
            return encoded
        except Exception as e:
            logger.exception()
            raise
         

    def run_command(self, command: str):
        state_embedding = self._read_command(command=command)
        pred_action, log_prob, critic_value = self.agent.select_action(state_embedding=state_embedding)

        inference_record = InferenceSchema(
            id=f"AI-{self.long_memory.get_count() + 1}",
            command=command,
            state_embedding=state_embedding.tolist(),
            action_id=pred_action,
            log_prob=log_prob.item(),
            critic_value=critic_value.item(),
            reward=0.0,
            timestamp=datetime.now()
        )

        self._store_memory(inference=inference_record)

        return pred_action



