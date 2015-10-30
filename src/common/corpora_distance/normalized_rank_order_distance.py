__author__ = 'stefan'

import common.ngram.model_generator as mg
import common.util.rank as ru


def rank_order_normalized_distance(p, q, distance_p_q):

    p_r = mg.create_rank_model(p)  # rank model of p
    q_r = mg.create_rank_model(q)  # rank model of q

    min_rank = ru.min_rank([p_r.values(), q_r.values()])  # get minimum rank from both models (probably always 1)
    max_rank = ru.max_rank([p_r.values(), q_r.values()])  # get the maximum rank from both models

    default_distance = max_rank - min_rank + 1  # distance for an n-gram which is contained by only one model (p or q)

    # maximum possible distance between p and q (all n-grams are only part of either p or q)
    max_distance = (len(p_r) + len(q_r)) * default_distance

    normalized_distance = float(distance_p_q) / max_distance
    return normalized_distance
