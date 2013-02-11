import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn import metrics
from sklearn.datasets import load_files
from sklearn.grid_search import GridSearchCV
import numpy as np


categories = ((100, float('inf'), '101+'),
             (50, 99, '51_to_100'),
             (20, 49, '21_to_50'),
             (10, 19, '11_to_20'),
             (0, 9, '1_to_10'),
             (-20, -1, 'neg19_to_0'),
             (-50, -21, 'neg50_to_neg20'),
             (float('-inf'), -50, 'Downvoted_to_shit'))

category_names = [cat[-1] for cat in categories]



def train(subreddit, classifier='NB'):

    pipeline = get_pipeline(classifier)
    training_set, test_set = get_training_and_test_data(subreddit)
    pipeline.fit(training_set.data, training_set.target)
    predicted = pipeline.predict(test_set.data)

    print "Accuracy: %s" % np.mean(predicted == test_set.target)
    print metrics.classification_report(test_set.target, predicted, target_names=test_set.target_names)
    print metrics.confusion_matrix(test_set.target, predicted)
    return pipeline

def gridsearch(subreddit, classifier="NB"):
    pipeline = get_pipeline(classifier)
    parameters = {
        'vectorizer__ngram_range': ((1,1), (1,2), (1,3)),
        'tfidf__use_idf': (True, False)
    }
    if classifier == 'NB':
        parameters['classifier__fit_prior']  = (True, False)
    else:
        parameters['classifier__C'] =  (100, 1000)

    gridsearch_classifier = GridSearchCV(pipeline, parameters, n_jobs=-1)
    training_set, _ = get_training_and_test_data(subreddit)
    gridsearch_classifier = gridsearch_classifier.fit(training_set.data[:500], training_set.target[:500])
    best_parameters, _, scores =  max(gridsearch_classifier.grid_scores_, key=lambda x: x[1])
    for param_name in sorted(parameters.keys()):
         print "%s: %r" % (param_name, best_parameters[param_name])


def get_training_and_test_data(subreddit):
    test_data_path = os.path.join('labeled_data', subreddit, 'test')
    training_data_path = os.path.join('labeled_data', subreddit, 'training')

    test_set = load_files(test_data_path, categories=category_names, shuffle=True, random_state=42)
    training_set = load_files(training_data_path, categories=category_names, shuffle=True, random_state=42)
    return training_set, test_set



def get_pipeline(classifier="NB"):
    if classifier == 'NB':
        classifier_object = MultinomialNB(fit_prior=False)
    elif classifier == 'SVC':
        classifier_object = LinearSVC()

    return  Pipeline([
        ('vectorizer', CountVectorizer(ngram_range=(1,3))),
        ('tfidf', TfidfTransformer(use_idf=True)),
        ('classifier', classifier_object)
    ])







