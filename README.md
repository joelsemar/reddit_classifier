reddit_classifier
=================


V1 of the reddit classifier i mentioned at the last few meetups. (Finally stopped procrastinating and did it)


To use:


You'll need

scikit-learn
scipy
numpy
requests

I've included a requirements file (pip install -r requirements.txt)

Should get you going but...but maybe not, since I didn't use virtualenv for this...(sorry)

there's not much of an interface, but here goes

'''
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
'''


for classify.predict, the second argument is the name of the subreddit. I've included data for /r/funny.

To 'discover' another subreddit, do

'''
import scrape
scrape.traverse_subreddit('technology')
'''
This can take a while due to rate limiting.
If you just want a few thousand comments quickly to try something out (basically hit the rate limit immediately then give up)
do
'''
scrape.traverse_subreddit('technology', burst=True)
'''
