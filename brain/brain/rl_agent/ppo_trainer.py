from brain.rl_agent.ppo_agent import PPOAgent
import torch 

class Trainer:
    def __init__(self, actor_network, critic_network, learning_rate=3e-4, epochs = 5):
        self.optimizer = torch.optim.Adam([
            {"params": actor_network.parameters()},
            {"params": critic_network.parameters()}
        ], learning_rate)

        self.epochs = epochs
    
    @staticmethod
    def critic_loss_function(target_return, critic_prediction):
        value_loss = (0.5 * (critic_prediction - target_return) ** 2).mean()
        return value_loss 
    
    @staticmethod
    def clip_loss_function(new_log_probs, old_log_probs, advantages, epsilon=0.2):
        ratio = torch.exp(new_log_probs - old_log_probs)
        obj_unclipped = ratio * advantages

        obj_clipped = torch.clamp(ratio, 1 - epsilon, 1 + epsilon) * advantages

        clip_loss = torch.min(obj_unclipped, obj_clipped)

        return -clip_loss.mean()
    
    """def training_loop(self, actor_network, critic_network, memory_batch, state, gamma_value, lambda_value):
        next_value = critic_network(state)
        target_returns, advantages  = memory.get_generalized_advantage_estimation(next_value, gamma_value, lambda_value)
        normalized_advantages = (advantages - torch.mean(advantages)) / torch.std_mean(advantages) 

        for epoch in range(self.epochs):
            for memory in memory_batch:
                actor_pred = actor_network(state)
                critic_pred = critic_network(state)

                actor_loss = self.clip_loss_function()"""


    
    