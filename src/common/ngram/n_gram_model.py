import pandas


class NGramModel:
    model = pandas.Series()

    def __init__(self, n_grams):
        if type(n_grams) == list:
            # create model (count n_grams)
            temp = pandas.Series(n_grams)
            self.model = temp.groupby(temp.values).count()
        elif type(n_grams) == dict:
            # create model (transform dict to Series
            self.model = pandas.Series(n_grams)
        else:
            raise TypeError("Cannot create model from {0}.".format(type(n_grams)))

    def sort_by_frequencies(self):
        self.model.sort_values(inplace=True)

    def sort_by_n_grams(self):
        self.model.sort_index(inplace=True)

    def get_frequencies(self):
        return list(self.model.values)

    def get_frequencies_as_array(self):
        return self.model.values

    def get_frequency(self, n_gram):
        return self.model[n_gram]

    def get_n_grams(self):
        return list(self.model.index)

    def get_rank_model(self):
        return self.model.rank(method="dense", ascending=False)

    def contains_n_gram(self, n_gram):
        return n_gram in self.model.index

    def replace_frequencies(self, replace):
        self.model = self.model.apply(lambda x: replace[x])

    def transform_to_relative_frequencies(self):
        freq_sum = self.model.sum()
        self.model = self.model.apply(lambda x: x / freq_sum)

    def add_n_grams_if_new(self, n_grams, frequency):
        for ng in n_grams:
            if ng not in self.model.index:
                self.model[ng] = frequency

    def remove_rare_n_grams(self, f_min):
        m = self.model
        m.drop(m[m < f_min].index, inplace=True)

    def copy(self):
        copy = NGramModel([])
        copy.model = self.model.copy()

        return copy
