# Bayes Classifier

import csv, math, os, pickle, re
import classdata

class Bayes_Classifier:

    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
        cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
        the system will proceed through training.  After running this method, the classifier 
        is ready to classify input text."""
        
        self.data_file = "data_twitter.csv"
        self.neg_data_filename = "neg_data_twitter.pickle"
        self.pos_data_filename = "pos_data_twitter.pickle"

        # Try to load saved data files
        try:
            self.neg_data = self.load(self.neg_data_filename)
            self.pos_data = self.load(self.pos_data_filename)

        # Couldn't load saved data files, so need to train
        except (OSError, IOError):
            self.train()


    def get_true_class(self, line):
        """Return 0 for negative review, 1 for positive review"""
        if int(line[1]) != 1 and int(line[1]) != 0:
            print line[1], line
            raise Exception("WAT")
        return int(line[1])


    def train(self):   
        """Trains the Naive Bayes Sentiment Classifier."""

        neg = classdata.ClassData()
        pos = classdata.ClassData()

        with open(self.data_file, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:

                true_class = self.get_true_class(row)
                words = row[3]
                word_list = self.tokenize(words)

                # Negative
                if true_class == 0:
                    neg.num_files += 1
                    for i in range(len(word_list)):
                        unigram = word_list[i].lower()
                        neg.feature_dict[unigram] = 1 + (neg.feature_dict[unigram] if unigram in neg.feature_dict else 0)

                # Positive
                elif true_class == 1:
                    pos.num_files += 1
                    for i in range(len(word_list)):
                        unigram = word_list[i].lower()
                        pos.feature_dict[unigram] = 1 + (pos.feature_dict[unigram] if unigram in pos.feature_dict else 0)

        neg.sum_of_all_features = sum([neg.feature_dict[f] for f in neg.feature_dict])
        pos.sum_of_all_features = sum([pos.feature_dict[f] for f in pos.feature_dict])

        self.neg_data = neg
        self.pos_data = pos

        # Cache results for next time
        self.save(neg, self.neg_data_filename)
        self.save(pos, self.pos_data_filename)


    def classify(self, sText, never_neutral=False):
        """Given a target string sText, this function returns the most likely
        document class to which the target string belongs (i.e., positive,
        negative or neutral). If never_neutral is set to True, it will never
        output neutral."""
        
        lWordList = self.tokenize(sText)

        total_file_count = self.neg_data.num_files + self.pos_data.num_files
        prob_neg_prior = self.neg_data.num_files / float(total_file_count)
        prop_pos_prior = self.pos_data.num_files / float(total_file_count)

        # Prior Probabilities
        sum_of_logs_given_neg = math.log(prob_neg_prior, 2)
        sum_of_logs_given_pos = math.log(prop_pos_prior, 2)

        for i in range(len(lWordList)):
            unigram = lWordList[i].lower()

            # Negative
            word_freq_neg = 1 + (self.neg_data.feature_dict[unigram] if unigram in self.neg_data.feature_dict else 0)
            cond_prob_neg = float(word_freq_neg) / self.neg_data.sum_of_all_features
            sum_of_logs_given_neg += math.log(cond_prob_neg, 2)

            # Positive
            word_freq_pos = 1 + (self.pos_data.feature_dict[unigram] if unigram in self.pos_data.feature_dict else 0)
            cond_prob_pos = float(word_freq_pos) / self.pos_data.sum_of_all_features
            sum_of_logs_given_pos += math.log(cond_prob_pos, 2)

        diff = sum_of_logs_given_pos - sum_of_logs_given_neg

        epsilon = 0 if never_neutral else 1

        if abs(diff) < epsilon: # too close to call
            return "neutral"
        elif diff > 0:  # P(pos) > P(neg)
            return "positive"
        else:           # P(pos) < P(neg)
            return "negative"


    def loadFile(self, sFilename):
        """Given a file name, return the contents of the file as a string."""

        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt
   
    def save(self, dObj, sFilename):
        """Given an object and a file name, write the object to the file using pickle."""

        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()
   
    def load(self, sFilename):
        """Given a file name, load and return the object stored in the file."""

        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj

    def tokenize(self, sText): 
        """Given a string of text sText, returns a list of the individual tokens that 
        occur in that string (in order)."""

        lTokens = []
        sToken = ""
        for c in sText:
            if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
                sToken += c
            else:
                if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
                if c.strip() != "":
                    lTokens.append(str(c.strip()))
               
        if sToken != "":
            lTokens.append(sToken)

        return lTokens
