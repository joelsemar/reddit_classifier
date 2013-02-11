import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn import metrics
from sklearn.datasets import load_files
from sklearn.grid_search import GridSearchCV
import scrape
import numpy as np


categories = ((10, float('inf'), '11+'),
             (0, 9, '1_to_10'),
             (float('-inf'), -0, 'Downvoted'))

category_names = [cat[-1] for cat in categories]

registered_classifiers = {}


def predict(comment, subreddit):
    global categories
    classifier = registered_classifiers.get(subreddit)
    if not classifier:
        classifier = train(subreddit)
    return categories[classifier.predict([comment])[0]][-1]


def train(subreddit, classifier='SVC'):
    if not os.path.exists('labeled_data/%s/train' % subreddit):
        success = scrape.unpack_data(subreddit)
        if not success:
            return

    pipeline = get_pipeline(classifier)
    training_set, test_set = get_training_and_test_data(subreddit)
    pipeline.fit(training_set.data, training_set.target)
    predicted = pipeline.predict(test_set.data)

    print "Accuracy: %s" % np.mean(predicted == test_set.target)
    print metrics.classification_report(test_set.target, predicted, target_names=test_set.target_names)
    print metrics.confusion_matrix(test_set.target, predicted)
    registered_classifiers[subreddit] = pipeline
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







