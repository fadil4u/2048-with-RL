import torch
import torch.nn as nn
import torch.optim as optim

class LinearQNet(nn.Module):
    """
    Simple 2-layer feed-forward neural network for Q-learning.
    Input: flattened game state (e.g., 16 for 4x4 grid)
    Output: Q-values for each action (left, right, up, down)
    """
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.linear1(x))
        return self.linear2(x)