import pandas


class NGramModel:
    model = pandas.Series()

    def __init__(self, n_grams):
        # create model (count n_grams)
        temp = pandas.Series(n_grams)
        self.model = temp.groupby(temp.values).count()

    def sort_by_frequencies(self):
        self.model.sort_values(inplace=True)

    def sort_by_n_grams(self):
        self.model.sort_index(inplace=True)

    def get_frequencies(self):
        return list(self.model.values)

    def get_n_grams(self):
        return list(self.model.index)

    def contains_n_gram(self, n_gram):
        return n_gram in self.model.index

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
