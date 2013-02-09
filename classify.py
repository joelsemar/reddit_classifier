from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


categories = (
             (100, float('inf'), '101+'),
             (50, 99, '51 to 100'),
             (20, 49, '21 to 50'),
             (10, 19, '11 to 20'),
             (0, 9, '1 to 10'),
             (-20, -1, '-19 to 0'),
             (-50, -21, '-50 to -20'),
             (float('-inf'), -50, 'Downvoted to shit'))

pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('tfidf', TfidfTransformer),
    ('classifier', MultinomialNB())
])







def train(subreddit):



    classifier = MultinomialNB()
    classifier.fit(X,Y)

    return classifier



