# BEST CLASSIFIER
# Remove common suffixes from words, so that only the stem is considered.
# Add both unigrams and bigrams to feature dictionaries, but in classification
# only consider the unigrams/bigrams that appeared more than a minimum number 
# of times in either the negative or positive training files.
# (Min set to 7, see classify function)

import math, os, pickle, re
import classdata

class Bayes_Classifier:

    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
        cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
        the system will proceed through training.  After running this method, the classifier 
        is ready to classify input text."""
        
        self.reviews_directory = "movies_reviews/"
        self.neg_data_filename = "neg_data_best.pickle"
        self.pos_data_filename = "pos_data_best.pickle"

        # Try to load saved data files
        try:
            self.neg_data = self.load(self.neg_data_filename)
            self.pos_data = self.load(self.pos_data_filename)

        # Couldn't load saved data files, so need to train
        except (OSError, IOError) as e:
            print e
            self.train(self.get_file_list())

        print "Num neg, pos files", self.neg_data.num_files, self.pos_data.num_files

    def get_file_list(self):
        """Get list of all files in reviews directory"""

        lFileList = []
        for fFileObj in os.walk(self.reviews_directory):
            lFileList = fFileObj[2]
            break
        return lFileList


    def get_true_class(self, file_name):
        """Return 0 for negative review, 1 for positive review"""

        if "-1-" in file_name:
            return 0
        elif "-5-" in file_name:
            return 1
        return -1


    def stem(self, word):
        """Remove common suffixes from words, returning just the stem"""

        stemmed_word = word.lower()
        endings = ["ing", "es", "ed", "er", "ly", "cy", "dom", "en", "tion",
                    "ence", "ent", "dom", "est", "ful", "fy", "ial", "ian",
                    "ic", "ine", "ish", "ism", "ist", "ite", "ity", "ive",
                    "ize", "less", "ment", "ness", "ology", "ty"]
        for ending in endings:
            if stemmed_word[-len(ending):] == ending:
                return stemmed_word[:-len(ending)]
        return stemmed_word


    def train(self, lTrainFiles=[]):   
        """Trains the Naive Bayes Sentiment Classifier."""

        if len(lTrainFiles) == 0:
            lTrainFiles = self.get_file_list()

        neg = classdata.ClassData()
        pos = classdata.ClassData()

        for sFilename in lTrainFiles:

            true_class = self.get_true_class(sFilename)
            word_list = self.tokenize(self.loadFile(self.reviews_directory + sFilename))

            # Negative
            if true_class == 0:
                neg.num_files += 1
                for i in range(len(word_list)):
                    # Unigram
                    unigram = self.stem(word_list[i])
                    neg.feature_dict[unigram] = 1 + (neg.feature_dict[unigram] if unigram in neg.feature_dict else 0)

                    # Bigram
                    if i+1 < len(word_list):
                        bigram = self.stem(word_list[i]) + ' ' + self.stem(word_list[i+1])
                        neg.feature_dict[bigram] = 1 + (neg.feature_dict[bigram] if bigram in neg.feature_dict else 0)

            # Positive
            elif true_class == 1:
                pos.num_files += 1
                for i in range(len(word_list)):
                    # Unigram
                    unigram = self.stem(word_list[i])
                    pos.feature_dict[unigram] = 1 + (pos.feature_dict[unigram] if unigram in pos.feature_dict else 0)
                    
                    # Bigram
                    if i+1 < len(word_list):
                        bigram = self.stem(word_list[i]) + ' ' + self.stem(word_list[i+1])
                        pos.feature_dict[bigram] = 1 + (pos.feature_dict[bigram] if bigram in pos.feature_dict else 0)

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

        min_feature_frequency = 7

        total_file_count = self.neg_data.num_files + self.pos_data.num_files
        prob_neg_prior = self.neg_data.num_files / float(total_file_count)
        prop_pos_prior = self.pos_data.num_files / float(total_file_count)

        # Prior Probabilities
        sum_of_logs_given_neg = math.log(prob_neg_prior, 2)
        sum_of_logs_given_pos = math.log(prop_pos_prior, 2)

        for i in range(len(lWordList)):
            cond_prob_neg = 0
            cond_prob_pos = 0

            # Unigrams
            unigram = self.stem(lWordList[i])

            if (unigram in self.neg_data.feature_dict and self.neg_data.feature_dict[unigram] > min_feature_frequency) \
              or (unigram in self.pos_data.feature_dict and self.pos_data.feature_dict[unigram] > min_feature_frequency):

                # Negative
                uni_freq_neg = 1 + (self.neg_data.feature_dict[unigram] if unigram in self.neg_data.feature_dict else 0)
                uni_cond_prob_neg = float(uni_freq_neg) / self.neg_data.sum_of_all_features
                cond_prob_neg += math.log(uni_cond_prob_neg, 2)

                # Positive
                uni_freq_pos = 1 + (self.pos_data.feature_dict[unigram] if unigram in self.pos_data.feature_dict else 0)
                uni_cond_prob_pos = float(uni_freq_pos) / self.pos_data.sum_of_all_features
                cond_prob_pos += math.log(uni_cond_prob_pos, 2)

            # Bigrams
            if i+1 < len(lWordList):
                bigram = self.stem(lWordList[i]) + ' ' + self.stem(lWordList[i+1])

                if (bigram in self.neg_data.feature_dict and self.neg_data.feature_dict[bigram] > min_feature_frequency) \
                  or (bigram in self.pos_data.feature_dict and self.pos_data.feature_dict[bigram] > min_feature_frequency):

                    # Negative
                    bi_freq_neg = 1 + (self.neg_data.feature_dict[bigram] if bigram in self.neg_data.feature_dict else 0)
                    bi_cond_prob_neg = float(bi_freq_neg) / self.neg_data.sum_of_all_features
                    cond_prob_neg += math.log(bi_cond_prob_neg, 2)

                    # Positive
                    bi_freq_pos = 1 + (self.pos_data.feature_dict[bigram] if bigram in self.pos_data.feature_dict else 0)
                    bi_cond_prob_pos = float(bi_freq_pos) / self.pos_data.sum_of_all_features
                    cond_prob_pos += math.log(bi_cond_prob_pos, 2)

            sum_of_logs_given_neg += cond_prob_neg
            sum_of_logs_given_pos += cond_prob_pos

        diff = sum_of_logs_given_pos - sum_of_logs_given_neg
        
        epsilon = 0 if never_neutral else 3
        
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
