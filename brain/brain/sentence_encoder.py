import torch
from sentence_transformers import SentenceTransformer
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentence_encoder")


class PerceptionModel:
    def __init__(self, 
                 device: str = None, 
                 model_name: str = "all-MiniLM-L6-v2", 
                 backend: str = "torch", 
                 model_kwargs = None):
        
        self.model = None
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.backend = backend
        self.model_kwargs = model_kwargs or {}
        self.is_ready = False

    def start_up(self):
        try:
            logger.info(f"Initializing Command Language Model: {self.model_name}...")
            
            if self.model_name:
                self.model = SentenceTransformer(
                    self.model_name, 
                    device=self.device,
                    model_kwargs=self.model_kwargs)
                
                self.is_ready = True 
                logger.info(f"Command Language Model loaded succesfully with model: {self.model_name}")
        
        except Exception as e:
            logger.error(f"Error loading Command Language Model: {str(e)}")
            self.is_ready = False
            raise
            
    
    def encode_command(self, command: str):
        if not self.is_ready:
            raise RuntimeError("Model is not loaded. Call start_up first.")
         
        return self.model.encode(command,
                                 convert_to_tensor=True)
        