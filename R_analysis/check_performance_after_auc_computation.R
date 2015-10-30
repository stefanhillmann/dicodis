# Mit dem Script wird gepüft, ob sich nach dem Berechnen der Performancewerte mit AUC alle anderen Werte gleich geblieben sind.
# Es geht als darum, ob tatsächlich nur jeweils die AUC für jedes Szenario zusätlich berechnet wurde.
# Es wird geprüft, ob die Werte für false_positives, true_positives, precisions, false_negative, 
# f_measure und recall in distance_performance ("alte Werte") und auc_test_performance ("neue Werte") gleich sind.
# Beides sind collections in der Datenbank classification_cross_validation.

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)

old <- dbGetQuery(cross_validation, "performance", '{}', 0, 0)
new <- dbGetQuery(cross_validation, "auc_test_performance", '{}', 0, 0)

# have 'new' same number of rows as 'old'?
sprintf("%s (rows of old) == %s (rows of unique): %s", nrow(old), nrow(new), nrow(old) == nrow(new))

# check if we really use the complete set of identifying (unique) parameters
unique <- old[, c(2, 4, 6, 11, 12, 13)]
# size of unique should be equal of size of old
sprintf("%s (rows of old) == %s (rows of unique): %s", nrow(old), nrow(unique), nrow(old) == nrow(unique))

# run through the 'old' and cpmpare with values in 'new'
for (i in 1:nrow(old)) {
  o <- old[i,]
  n <- new[which(new$criteria == o$criteria
               & new$classifier_name == o$classifier_name 
               & new$evaluation_id == o$evaluation_id 
               & new$n_gram_size == o$n_gram_size 
               & new$frequency_threshold == o$frequency_threshold 
               & new$smoothing_value == o$smoothing_value), ]
  
  d_fn <- o$false_negatives - n$false_negatives
  d_fp <- o$false_positives - n$false_positives
  d_tp <- o$true_positives - n$true_positives
  d_f <- o$f_measure - n$f_measure
  
  if(sum(c(d_fn, d_fp, d_tp, d_f)) != 0.0) {
    print('old:')
    print(o)
    print('new:')
    print(n)
    stop('Difference not equal to zero.')
  }
}
