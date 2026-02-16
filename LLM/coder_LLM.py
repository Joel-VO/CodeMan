import torch
import ollama

device = "cuda" if torch.cuda.is_available() else "cpu"

print(device) # debugging

def llm_response():
    pass