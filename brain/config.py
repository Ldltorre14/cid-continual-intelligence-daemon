import torch 


device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "all-mpnet-base-v2"