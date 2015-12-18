class CorpusData:

    def __init__(self, name, is_static, constraints):
        self.name = name
        self.is_static = is_static
        self.constraints = constraints

    def __str__(self):
        return self.name


SUCCESSFUL = CorpusData("successful", True, {})
NOT_SUCCESSFUL = CorpusData("not successful", True, {})
DIALOGUES_SHORT = CorpusData("dialogues short", True, {})
DIALOGUES_LONG = CorpusData("dialogues long", True, {})
WORD_ACCURACY_100 = CorpusData("word accuracy 100", True, {})
WORD_ACCURACY_60 = CorpusData("word accuracy 60", True, {})
USER_JUDGMENT_GOOD = CorpusData("user judgment good", True, {})
USER_JUDGMENT_BAD = CorpusData("user judgment bad", True, {})
SIMULATION_GOOD = CorpusData("simulation good", True, {})
SIMULATION_BAD = CorpusData("simulation bad", True, {})
REAL_USER = CorpusData("real user", True, {})
GOOD_SIMULATION_SUCCESSFUL = CorpusData("good simulation successful", False, {})
GOOD_SIMULATION_NOT_SUCCESSFUL = CorpusData("good simulation not successful", False, {})
GOOD_SIMULATION_SUB_SET_SAMPLE = CorpusData("good simulation sub set sample", False, {})


def get_all_corpus_data():
    return [
        SUCCESSFUL,
        NOT_SUCCESSFUL,
        DIALOGUES_SHORT,
        DIALOGUES_LONG,
        WORD_ACCURACY_100,
        WORD_ACCURACY_60,
        USER_JUDGMENT_GOOD,
        USER_JUDGMENT_BAD,
        SIMULATION_GOOD,
        SIMULATION_BAD,
        REAL_USER
    ]

