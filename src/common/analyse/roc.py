"""
Created on Tue Jul 22 14:37:10 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import matplotlib.pyplot as plt


def get_roc_points(example_ids, positive_probability_dict, true_class_dict, positive_class, negative_class):
    """

    :param example_ids:
    :param positive_probability_dict:
    :param true_class_dict:
    :param positive_class:
    :param negative_class:
    :return:
    """
    sorted_ids = sorted(example_ids, key=lambda x: positive_probability_dict[x], reverse=True)

    n_of_positives = true_class_dict.values().count(positive_class)
    n_of_negatives = true_class_dict.values().count(negative_class)

    score_previous = float("inf")
    fp = 0.0  # false positives counter and x axis
    tp = 0.0  # true positives counter and y axis
    fp_rate = []
    tp_rate = []

    for example_id in sorted_ids:
        score = positive_probability_dict[example_id]
        if score != score_previous:
            fp_rate.append(fp / n_of_negatives)
            tp_rate.append(tp / n_of_positives)
            score_previous = score

        if true_class_dict[example_id] == positive_class:
            tp += 1
        else:
            fp += 1

    # add last example (will be (1, 1)
    fp_rate.append(fp / n_of_negatives)
    tp_rate.append(tp / n_of_positives)

    roc_points = dict()
    roc_points['fp_rate'] = fp_rate
    roc_points['tp_rate'] = tp_rate

    return roc_points


def create_plot(roc_points):
    plt.xlabel("FPR", fontsize=14)
    plt.ylabel("TPR", fontsize=14)
    plt.title("ROC Curve", fontsize=14)


    tpr = roc_points['tp_rate']
    fpr = roc_points['fp_rate']

    plt.fill_between(fpr, tpr, facecolor='gray', alpha=0.5)

    plt.plot(fpr, tpr)
    plt.plot([0, 1], [0, 1], linestyle='--', color='black')

    return plt


def trapezoid_area(fp, fp_prev, tp, tp_prev):
    base = abs(fp - fp_prev)
    height = (tp + tp_prev) / 2
    return base * height


def get_auc(example_ids, positive_probability_dict, true_class_dict, positive_class, negative_class):
    """

    :param example_ids:
    :param positive_probability_dict:
    :param true_class_dict:
    :param positive_class:
    :param negative_class:
    :return:
    """
    sorted_ids = sorted(example_ids, key=lambda x: positive_probability_dict[x], reverse=True)

    n_of_positives = true_class_dict.values().count(positive_class)
    if n_of_positives == 0:
        print('Zero positives.')

    n_of_negatives = true_class_dict.values().count(negative_class)
    if n_of_negatives == 0:
        print('Zero negatives.')



    fp = 0.0
    tp = 0.0
    fp_prev = 0.0
    tp_prev = 0.0
    auc = 0.0
    score_prev = float("inf")

    for example_id in sorted_ids:
        score = positive_probability_dict[example_id]
        if score != score_prev:
            auc = auc + trapezoid_area(fp, fp_prev, tp, tp_prev)
            score_prev = score
            fp_prev = fp
            tp_prev = tp

        if true_class_dict[example_id] == positive_class:
            tp += 1
        else:
            fp += 1

    auc = auc + trapezoid_area(n_of_negatives, fp_prev, n_of_negatives, tp_prev)
    auc = auc / (n_of_positives * n_of_negatives)  # scale from n_of_positives times n_of_negatives onto the unit square

    return auc





