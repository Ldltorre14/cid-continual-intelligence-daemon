import torch
from torch import nn 



class PPONetwork(nn.Module):
    def __init__(self, in_embed_dim: int, out_embed_dim):
        super().__init__()

        self.layers = nn.Sequential(
            # Input Layer where the embed_dim represents the encoder's output
            nn.Linear(in_features=in_embed_dim, out_features=384),
            nn.ReLU(),

            nn.Linear(in_features=384, out_features=196),
            nn.ReLU(),
            nn.Linear(in_features=196, out_features=98),
            nn.ReLU(),
        )

        # Actor Linear head for mapping to the len(k) where k is the number of controllers/functions
        self.actor_head = nn.Linear(in_features=98, out_features=out_embed_dim)

        # Critic Linear head to output the values 
        self.critic_head = nn.Linear(in_features=98, out_features=1)
    
    def forward(self, input_embedding):
        x = self.layers(input_embedding)

        critic_val = self.critic_head(x)
        actor_dist = self.actor_head(x)
        
        actor_dist = torch.distributions.Categorical(logits=actor_dist)
        return actor_dist, critic_val
    
