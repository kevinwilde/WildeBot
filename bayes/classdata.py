# Class to hold class data. Necessary to define in separate module because
# I will be pickling instances of this class

class ClassData:
    def __init__(self):
        """Used to keep track of data for each class in training"""
        
        self.num_files = 0
        self.feature_dict = {}
        self.sum_of_all_features = 0
