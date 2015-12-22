class Criteria:

    def __init__(self, name):
        self.name = name


TASK_SUCCESS = Criteria("task success")
USER_JUDGEMENT = Criteria("user judgement")
SIMULATION_QUALITY = Criteria("simulation quality")
DIALOGUE_LENGTH = Criteria("dialogue length")
WORD_ACCURACY = Criteria("word accuracy")
SIM_GOOD_VS_REAL = Criteria("sim. good vs real")
SIM_BAD_VS_REAL = Criteria("sim. bad vs real")
SIM_NO_SUCCESS_VS_REAL = Criteria("sim. no succ. vs real")
SIM_SAMPlED_VS_REAL = Criteria("sim. samp. vs real")
SIM_SAMPLED_VS_SIM_NO_SUCCESS = Criteria("sim. samp. vs sim. no succ.")
