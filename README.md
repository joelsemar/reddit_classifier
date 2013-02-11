reddit_classifier
=================


V1 of the reddit classifier i mentioned at the last few meetups. (Finally stopped procrastinating and did it)
This is very much proof of concept and very raw.


To use, You'll need:
```
scikit-learn
scipy
numpy
requests
```

I've included a requirements file: `pip install -r requirements.txt`

Should get you going but...but maybe not, since I didn't use virtualenv for this...(sorry).

I had trouble getting it running on a mac due to fortran compilers and Xcode requirements
(so i gave up after a few mintues). I only know for sure that it works on ubuntu 12.04


```
In [1]: import classify

In [2]: classify.predict('Test post please ignore', 'funny')
Accuracy: 0.654867256637
             precision    recall  f1-score   support

        11+       0.42      0.22      0.29       425
    1_to_10       0.69      0.89      0.78      1272
  Downvoted       0.44      0.12      0.20       224

avg / total       0.61      0.65      0.60      1921

[[  93  319   13]
 [ 113 1137   22]
 [  13  183   28]]
Out[2]: '1_to_10'
```


for `classify.predict`, the second argument is the name of the subreddit. I've included data for /r/funny.

To 'discover' another subreddit, do

```
import scrape
scrape.traverse_subreddit('technology')
```
This can take a while due to rate limiting.
If you just want a few thousand comments quickly to try something out (basically hit the rate limit immediately then give up)
do
```
scrape.traverse_subreddit('technology', burst=True)
```

If you want to use the classifier directly you can do (for a support vector machine classifier)

```
classifier = classify.train('funny', classifier='SVC')
```

or for Naive Bayes

```
classifier = classify.train('funny', classifier='NB')
```

You can also run the parameter tuning grid search via:

```
classify.gridsearch('comics')
```

Which *should* return the best parameters for that subreddit data.



