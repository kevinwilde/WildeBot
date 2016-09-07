"""
This module implements the bayes classifier trained with movie reviews.

Remove common suffixes from words, so that only the stem is considered.
Add both unigrams and bigrams to feature dictionaries, but in classification
only consider the unigrams/bigrams that appeared more than a minimum number
of times in either the negative or positive training files.
(Min set to 7, see classify function)
"""

import math
import os
import pickle
import re

from . import classdata

class BayesClassifier(object):

    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment
        Classifier.  If a cache of a trained classifier has been
        stored, it loads this cache.  Otherwise, the system will
        proceed through training.  After running this method, the
        classifier is ready to classify input text.
        """
        self.reviews_directory = "src/bayes/movies_reviews/"
        self.neg_data_filename = "src/bayes/neg_data_best.pickle"
        self.pos_data_filename = "src/bayes/pos_data_best.pickle"

        # Try to load saved data files
        try:
            self.neg_data = self.load(self.neg_data_filename)
            self.pos_data = self.load(self.pos_data_filename)

        # Couldn't load saved data files, so need to train
        except (OSError, IOError):
            self.train(self.get_file_list())


    def get_file_list(self):
        """Get list of all files in reviews directory"""
        file_list = []
        for file_obj in os.walk(self.reviews_directory):
            file_list = file_obj[2]
            break
        return file_list


    def get_true_class(self, filename):
        """Return 0 for negative review, 1 for positive review"""
        if "-1-" in filename:
            return 0
        elif "-5-" in filename:
            return 1
        return -1


    def stem(self, word):
        """Remove common suffixes from words, returning just the stem"""
        stemmed_word = word.lower()
        endings = [
            "ing", "es", "ed", "er", "ly", "cy", "dom", "en", "tion",
            "ence", "ent", "dom", "est", "ful", "fy", "ial", "ian",
            "ic", "ine", "ish", "ism", "ist", "ite", "ity", "ive",
            "ize", "less", "ment", "ness", "ology", "ty"
        ]
        for ending in endings:
            if stemmed_word.endswith(ending):
                return stemmed_word[:-len(ending)]
        return stemmed_word


    def train(self, train_files=[]):
        """Trains the Naive Bayes Sentiment Classifier."""
        if len(train_files) == 0:
            train_files = self.get_file_list()

        neg = classdata.ClassData()
        pos = classdata.ClassData()

        for filename in train_files:

            true_class = self.get_true_class(filename)
            word_list = self.tokenize(self.load_file(self.reviews_directory
                                                     + filename))

            # Negative
            if true_class == 0:
                neg.num_files += 1
                for i in range(len(word_list)):
                    # Unigram
                    unigram = self.stem(word_list[i])
                    neg.feature_dict[unigram] = 1 + neg.feature_dict.get(unigram, 0)

                    # Bigram
                    if i+1 < len(word_list):
                        bigram = self.stem(word_list[i]) + ' ' + self.stem(word_list[i+1])
                        neg.feature_dict[bigram] = 1 + neg.feature_dict.get(bigram, 0)

            # Positive
            elif true_class == 1:
                pos.num_files += 1
                for i in range(len(word_list)):
                    # Unigram
                    unigram = self.stem(word_list[i])
                    pos.feature_dict[unigram] = 1 + pos.feature_dict.get(unigram, 0)

                    # Bigram
                    if i+1 < len(word_list):
                        bigram = self.stem(word_list[i]) + ' ' + self.stem(word_list[i+1])
                        pos.feature_dict[bigram] = 1 + pos.feature_dict.get(bigram, 0)

        neg.sum_of_all_features = sum([neg.feature_dict[f] for f in neg.feature_dict])
        pos.sum_of_all_features = sum([pos.feature_dict[f] for f in pos.feature_dict])

        self.neg_data = neg
        self.pos_data = pos

        # Cache results for next time
        self.save(neg, self.neg_data_filename)
        self.save(pos, self.pos_data_filename)


    def classify(self, text):
        """Given a target string text, this function returns the most likely
        document class to which the target string belongs (i.e., positive,
        negative or neutral).
        """
        word_list = self.tokenize(text)

        min_feature_frequency = 7

        total_file_count = self.neg_data.num_files + self.pos_data.num_files
        prob_neg_prior = self.neg_data.num_files / float(total_file_count)
        prop_pos_prior = self.pos_data.num_files / float(total_file_count)

        # Prior Probabilities
        sum_of_logs_given_neg = math.log(prob_neg_prior, 2)
        sum_of_logs_given_pos = math.log(prop_pos_prior, 2)

        for i in range(len(word_list)):
            cond_prob_neg = 0
            cond_prob_pos = 0

            # Unigrams
            unigram = self.stem(word_list[i])

            if ((unigram in self.neg_data.feature_dict and
                 self.neg_data.feature_dict[unigram] > min_feature_frequency) or
                    (unigram in self.pos_data.feature_dict and
                     self.pos_data.feature_dict[unigram] > min_feature_frequency)):

                # Negative
                uni_freq_neg = 1 + self.neg_data.feature_dict.get(unigram, 0)
                uni_cond_prob_neg = float(uni_freq_neg) / self.neg_data.sum_of_all_features
                cond_prob_neg += math.log(uni_cond_prob_neg, 2)

                # Positive
                uni_freq_pos = 1 + self.pos_data.feature_dict.get(unigram, 0)
                uni_cond_prob_pos = float(uni_freq_pos) / self.pos_data.sum_of_all_features
                cond_prob_pos += math.log(uni_cond_prob_pos, 2)

            # Bigrams
            if i+1 < len(word_list):
                bigram = self.stem(word_list[i]) + ' ' + self.stem(word_list[i+1])

                if ((bigram in self.neg_data.feature_dict and
                     self.neg_data.feature_dict[bigram] > min_feature_frequency) or
                        (bigram in self.pos_data.feature_dict and
                         self.pos_data.feature_dict[bigram] > min_feature_frequency)):

                    # Negative
                    bi_freq_neg = 1 + self.neg_data.feature_dict.get(bigram, 0)
                    bi_cond_prob_neg = float(bi_freq_neg) / self.neg_data.sum_of_all_features
                    cond_prob_neg += math.log(bi_cond_prob_neg, 2)

                    # Positive
                    bi_freq_pos = 1 + self.pos_data.feature_dict.get(bigram, 0)
                    bi_cond_prob_pos = float(bi_freq_pos) / self.pos_data.sum_of_all_features
                    cond_prob_pos += math.log(bi_cond_prob_pos, 2)

            sum_of_logs_given_neg += cond_prob_neg
            sum_of_logs_given_pos += cond_prob_pos

        diff = sum_of_logs_given_pos - sum_of_logs_given_neg
        return diff


    def load_file(self, filename):
        """Given a file name, return the contents of the file as a
        string.
        """
        with open(filename, "r") as f:
            contents = f.read()
        return contents

    def save(self, obj, filename):
        """Given an object and a file name, write the object to the
        file using pickle.
        """
        with open(filename, "w") as f:
            p = pickle.Pickler(f)
            p.dump(obj)

    def load(self, filename):
        """Given a file name, load and return the object stored in the
        file.
        """
        with open(filename, "r") as f:
            u = pickle.Unpickler(f)
            obj = u.load()
        return obj

    def tokenize(self, text):
        """Given a string of text text, returns a list of the
        individual tokens that occur in that string (in order).
        """
        tokens = []
        token = ""
        for c in text:
            if (re.match("[a-zA-Z0-9]", str(c)) is not None or
                    c == "\"" or c == "_" or c == "-"):
                token += c
            else:
                if token != "":
                    tokens.append(token)
                    token = ""
                if c.strip() != "":
                    tokens.append(str(c.strip()))

        if token != "":
            tokens.append(token)

        return tokens
