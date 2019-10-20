
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/03_minibatch.ipynb
import torch
import torch.nn as nn

import requests
import pickle

import gzip
from pathlib import Path

MNIST_URL='http://deeplearning.net/data/mnist/mnist.pkl.gz'

def download_file(url:str, folder:str):
    folder = Path(folder)
    files = [x.name for x in folder.glob('**/*') if x.is_file()]
    filename = url.split('/')[-1]
    if filename in files:
        print(f"File {filename} already exists in {folder}")
        return folder / filename
    r = requests.get(url)
    with open(folder / filename, 'wb') as f:
        f.write(r.content)
    return folder / filename

def get_data():
    path = download_file(MNIST_URL, './data')
    with gzip.open(path, 'rb') as f:
        ((x_train, y_train), (x_valid, y_valid), _) = pickle.load(f, encoding='latin-1')
    return map(torch.tensor, (x_train,y_train,x_valid,y_valid))

def accuracy(preds, target):
    return (preds.argmax(axis=1) == target).float().mean()

import torch.optim as optim

class Dataset:
    def __init__(self, x, y):
        assert len(x)==len(y)
        self.x = x
        self.y = y
    def __len__(self):
        return len(self.x)
    def __getitem__(self, i):
        return self.x[i], self.y[i]

from torch.utils.data import DataLoader, SequentialSampler, RandomSampler

def get_dls(ds_train, ds_valid, bs, **kwargs):
    return (DataLoader(ds_train, batch_size=bs, shuffle=True, **kwargs),
            DataLoader(ds_valid, batch_size=bs*2, **kwargs))