import numpy as np
import pandas as pd
import torch
import transformers as ppb

from sklearn.cluster import KMeans

def read_data():
    df = pd.read_csv('../data/sample_sentences.txt', delimiter='\t', header=None)
    return df

def load_bert():
    model_class, tokenize_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'bert-base-uncased')
    
    tokenizer = tokenize_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights, output_hidden_states=True)

    return model, tokenizer

def prepare_data(data, tokenizer):
    tokenized = data.apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))   
    
    max_len = 0
    
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)
            
    padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])

    attention_mask = np.where(padded != 0, 1, 0)
    
    return padded, attention_mask

def get_features(padded, attention_mask, model):
    """
    Return sentences vectors
    """
    input_ids = torch.tensor(padded)
    attention_mask = torch.tensor(attention_mask)
    
    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)
    
    # for classification only need CLS token of BERT 
    #
    # features = last_hidden_states[0][:, 0, :].numpy()
    # print(features.shape)
    
    # for token(word) vector extraction 
    #
    token_embeddings = torch.stack(last_hidden_states[2], dim=0)
    # print(token_embeddings.size())
    token_embeddings = token_embeddings.permute(1, 2, 0, 3)
    # print(token_embeddings.size())
    token_embeddings = token_embeddings[:, :, -4:, :]
    print(token_embeddings.size())
    
    # concat last 4 layers
    # (_s, _t, _l, _f) = token_embeddings.size()
    # token_embeddings = token_embeddings.reshape(_s, _t, (_l*_f))
    # temp = _l*_f
    # token_embeddings = token_embeddings.reshape(_s, (_t*temp))
    # print(token_embeddings.size())
    
    # sum last 4 layers
    token_embeddings = torch.sum(token_embeddings, dim=2)        
    print(token_embeddings.size())
    
    (_s, _t, _f) = token_embeddings.size()

    features = token_embeddings.reshape(_s, (_t*_f))
    
    # combine token-hidden layer vectors for each sentece  
    #
    # (_sent, _tok, _feat) = last_hidden_states[0][:, :, :].numpy().shape
    # print('{},{},{}'.format(_sent, _tok, _feat))
    # features = last_hidden_states[0].numpy().reshape(_sent, (_tok * _feat))
    
    
    print(features.shape)
    return features

def get_clusters(features):
    kmeans = KMeans(init='random', n_clusters=2, n_init=features.shape[0], max_iter=300, random_state=42)
    kmeans.fit(features)
    
    print(kmeans.labels_[:16])
    
def main():
    all_data = read_data()
    
    model, tokenizer = load_bert()
    
    lemma = 'glass'
    
    data = all_data[all_data[0].str.contains(lemma)]
    
    # sanity check
    # print(data[0])
    
    padded, attention_mask = prepare_data(data[0], tokenizer)
    
    features = get_features(padded, attention_mask, model)
    
    get_clusters(features)
    
if __name__ == '__main__':
    main()