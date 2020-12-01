import sys
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random
import os


def run_vader(file_path, sent_analyzer):
    '''
    run VADER sentiment analysis on files neg.csv and pos.csv
    at file_path and return confusion matrix
    '''
    print('#' * 20)
    true_pos = true_neg = false_pos = false_neg = 0

    with open(os.path.join(file_path, 'pos.csv')) as posfile:
        for text in posfile:
            score = sent_analyzer.polarity_scores(text)['compound']
            if score < 0.0:
                false_neg += 1
            elif score > 0.0:
                true_pos += 1
            else:
                if random.randint(1, 2) == 1:
                    false_neg += 1
                else:
                    true_pos += 1

    with open(os.path.join(file_path, 'neg.csv')) as negfile:
        for text in negfile:
            score = sent_analyzer.polarity_scores(text)['compound']
            if score < 0.0:
                true_neg += 1
            elif score > 0.0:
                false_pos += 1
            else:
                #Sentiment could not be deduced! select a random class
                if random.randint(1, 2) == 1:
                    false_pos += 1
                else:
                    true_neg += 1

    print('true positives:' + str(true_pos))
    print('true negatives:' + str(true_neg))
    print('false positives:' + str(false_pos))
    print('false negatives:' + str(false_neg))
    print('#' * 20)
    return([true_pos, false_neg, false_pos, true_neg])

# Print usage info
# if len(sys.argv) == 1:
#    print('vader.py <pos. sent. csv> <neg. sent. csv>')
#    quit()

# Make sure lexicon is installed or install as required
nltk.download('vader_lexicon')

sa = SentimentIntensityAnalyzer()

# For each run of experiment
with open('results_vader.csv', 'w') as results_vader:
    results_vader.write('RUN_NO, TP, FN, FP, TN\n')

for i in range(1, 50 + 1):
    print('run no ' + str(i))
    results = run_vader(os.path.join(sys.argv[1], 'run_' + str(i), 'test' ) , sa)
    with open('results_vader.csv', 'a') as results_vader:
        results_vader.write('RUN_' + str(i) + ',' 
                        + str(results[0]) + ',' 
                        + str(results[1]) + ',' 
                        + str(results[2]) + ','
                        + str(results[3]) + '\n')




