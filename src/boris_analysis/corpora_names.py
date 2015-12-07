class CorporaNames:
    SUCCESSFUL = "successful"
    NOT_SUCCESSFUL = "not successful"
    DIALOGUES_SHORT = "dialogues short"
    DIALOGUES_LONG = "dialogues long"
    WORD_ACCURACY_100 = "word accuracy 100"
    WORD_ACCURACY_60 = "word accuracy 60"
    USER_JUDGMENT_GOOD = "user judgment good"
    USER_JUDGMENT_BAD = "user judgment bad"
    SIMULATION_GOOD = "simulation good"
    SIMULATION_BAD = "simulation bad"
    REAL_USER = "real user"


def get_all_names():
    return [
        CorporaNames.SUCCESSFUL,
        CorporaNames.NOT_SUCCESSFUL,
        CorporaNames.DIALOGUES_SHORT,
        CorporaNames.DIALOGUES_LONG,
        CorporaNames.WORD_ACCURACY_100,
        CorporaNames.WORD_ACCURACY_60,
        CorporaNames.USER_JUDGMENT_GOOD,
        CorporaNames.USER_JUDGMENT_BAD,
        CorporaNames.SIMULATION_GOOD,
        CorporaNames.SIMULATION_BAD,
        CorporaNames.REAL_USER
    ]

