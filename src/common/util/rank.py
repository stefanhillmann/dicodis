__author__ = 'stefan'


def min_rank(rank_lists):
    # first get minimum from each rank list (via map) and than get minimum or all minimum (via outer min)
    return min( map(min, rank_lists) )


def max_rank(rank_lists):
    # first get minimum from each rank list (via map) and than get minimum or all minimum (via outer min)
    return max( map(max, rank_lists) )
