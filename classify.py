import simplejson
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import nltk
import os



def generate_sparse_matrix(filename):

    X = []
    Y = []
    with open(filename, 'rb') as input_file:
        for line in input_file.readlines()[:2]:

            posts = simplejson.loads(line)
            for post in posts[:2]:
                if 'ups' not in post or 'downs' not in post:
                    continue
                if int(post['ups']) - int(post['downs']) > 2:
                    Y.append(1)
                else:
                    Y.append(0)
                X.append(post['body'].split(' '))
    return np.array(X), np.array(Y)

def generate_labeled_featuresets(filename):
    out = []
    with open(filename, 'rb') as input_file:
        for line in input_file.readlines()[:2]:
            posts = simplejson.loads(line)
            for post in posts[:2]:
                if 'ups' not in post or 'downs' not in post:
                    continue
                if int(post['ups']) - int(post['downs']) > 2:
                    out.append( (post['body'],1))
                else:
                    out.append((post['body'],0))
    return out

def explode_dump(filename):
    if not os.path.exists('up'):
        os.makedirs('up')
    if not os.path.exists('down'):
        os.makedirs('down')
    doc_id = 0
    with open(filename, 'rb') as input_file:
        for line in input_file.readlines():
            posts = simplejson.loads(line)
            for post in posts:
                if 'ups' not in post or 'downs' not in post:
                    continue
                if int(post['ups']) - int(post['downs']) > 2:
                    dirname = 'up'
                else:
                    dirname = 'down'
                with open(os.path.join(dirname, 'doc_id' + str(doc_id)), 'w') as doc_file:
                    doc_file.write(post['body'].encode('utf-8'))
                doc_id += 1




def train_scikit(filename):
    X, Y = generate_sparse_matrix(filename)
    import ipdb;ipdb.set_trace()

    classifier = MultinomialNB()
    classifier.fit(X,Y)

    return classifier

def train(filename):
    feature_sets = generate_labeled_featuresets(filename)
    import pdb;pdb.set_trace()
    classifier = nltk.NaiveBayesClassifier.train(feature_sets)
    return classifier


