Collecting Data
===============

Perform cross validation
------------------------

* Script: run_cross_validation_smoothing_variable.py
* Create data about performance of each classifier for each criteria
* results are written in collection *documents_result*
    * *classifier_name*: id of the used distance measure
    * *frequency_threshold*: the minimal allowed frequency of an n-gram (n-grams with lower frequency are removed from the
    n-gram models)
    * *n_gram_size*: number of sequent system- and user-turns which are used for on n-gram
    * 
    
    
2. compute_performance_from_database.py
  * compute f-value, precision and recall for each classifier-criteria pair in *documents_result*
  * results are written into collection *performance*
   