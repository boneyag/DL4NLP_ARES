import numpy as np
import pandas as pd
import torch
import transformers as ppb

def load_bert():
    model_class, tokenize_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'bert-base-cased')
    
    tokenizer = tokenize_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights, output_hidden_states=True)

    return model, tokenizer

def prepare_data(data, tokenizer):
    tokenized = tokenizer.encode(data, add_special_tokens=True)
    segment_ids = [1] * len(tokenized)
    return tokenized, segment_ids

def get_feeaturs(tokenized, segment_ids, model, pos):
    token_tensor = torch.tensor([tokenized])
    segment_tensor = torch.tensor([segment_ids])
    
    with torch.no_grad():
        output = model(token_tensor, segment_tensor)   
        hidden_states = output[2]
        
        token_embeddings = torch.stack(hidden_states, dim=0)
        token_embeddings = torch.squeeze(token_embeddings, dim=1)
        token_embeddings = token_embeddings.permute(1, 0, 2)
        
        # creating token embeddings by summing last 4 layers
        sum_vec = torch.sum(token_embeddings[pos][-4:], dim=0)
        
        return sum_vec
