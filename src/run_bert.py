from inspect import Parameter
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.utils import class_weight
import torch
import transformers as ppb
import warnings

warnings.filterwarnings('ignore')


def read_data():
    df = pd.read_csv('https://github.com/clairett/pytorch-sentiment-classification/raw/master/data/SST2/train.tsv', delimiter='\t', header=None)
    return df

def load_bert():
    model_class, tokenize_class, pretrained_weights = (ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')
    
    # for bert instead of distilbert
    # model_class, tokenize_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'bert-base-uncased')
    
    tokenizer = tokenize_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights)

    return model, tokenizer

def prepare_data(data, tokenizer):
    tokenized = data.apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))   
    
    max_len = 0
    
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)
            
    padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])
    
    # sanity check 
    # print(padded.shape)
    
    attention_mask = np.where(padded != 0, 1, 0)
    
    # sanity check
    print(attention_mask.shape)
    
    return padded, attention_mask

def get_features(padded, attention_mask, model):
    input_ids = torch.tensor(padded)
    attention_mask = torch.tensor(attention_mask)
    
    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)
        
    features = last_hidden_states[0][:, 0, :].numpy()
    
    return features

def grid_search_params(X, y):
    parameters = {'C': np.linspace(0.0001, 100, 20)}
    grid_search = GridSearchCV(LogisticRegression(), parameters)
    grid_search.fit(X, y)
    
    print('Best parameters:{}'.format(grid_search.best_params_))
    
    return grid_search.best_params_

def train_logistic_regression(train_X, train_y, test_X, test_y, params):
    lr_clf = LogisticRegression(C=params, class_weight=None, dual=False)
    lr_clf.fit(train_X, train_y)

    print(lr_clf.score(test_X, test_y))    
    
          
def main():
    df = read_data()
    
    batch1 = df[:2000]
    
    # sanity check
    # print(batch1[1].value_counts())
    
    model, tokenizer = load_bert()
    
    padded, attention_mask = prepare_data(batch1[0], tokenizer)
    
    features = get_features(padded, attention_mask, model)
    labels = batch1[1]
    
    train_X, test_X, train_y, test_y = train_test_split(features, labels)
    
    params = grid_search_params(train_X, train_y)
    
    train_logistic_regression(train_X, train_y, test_X, test_y, params['C'])
    
    
    
if __name__ == '__main__':
    main()