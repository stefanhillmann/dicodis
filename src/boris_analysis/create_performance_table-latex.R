library(RMongo)
library(reshape2)
library(car)

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)


data = c()
for (size in 1:8) {
  
  query = sprintf('{"n_gram_size": %s, "frequency_threshold": 1}', size)
  p.db <- dbGetQuery(cross_validation, "performance", query, 0, 0)
  
  p <- data.frame(c = p.db$classifier_name, s = p.db$criteria, n = p.db$n_gram_size, 
                  t = p.db$frequency_threshold, l = p.db$smoothing_value, f = round(p.db$f_measure, 2))
  
  data[[size]] <- dcast(p, s + c ~ l, value.var = "f")
}

# table for frequency_threshold = 1 (n = 1:8)
ft_1 <- cbind(data[[1]], data[[2]][,3:5], data[[3]][,3:5], data[[4]][,3:5], data[[5]][,3:5], data[[6]][,3:5], data[[7]][,3:5], data[[8]][,3:5])

ft_1$c <- revalue(ft_1$c, c("cosine"="cos", "jensen"="j", "mean kullback leibler"="mkl", "rank order"="ro"))

ft_1$pos <- revalue(ft_1$s, 
                    c("juged_bad"="bad", "juged_good"="good", "long_interactions"="long", "real"="real", "real_vs_simulated_worst"="real", 
                      "short_interactions"="short","simulated"="sim_best", "simulated_worst_vs_real"="sim_worst", "simulation_quality_best"="sim-best", 
                      "simulation_quality_worst"="sim-worst", "task_failed"="miss", "task_successful"="success", "word_accuracy_100"="wa-100", 
                      "word_accuracy_60"="wa-60"))

ft_1$neg <- revalue(ft_1$s,
                      c("juged_bad"="good", "juged_good"="bad", "long_interactions"="shor", "real"="sim_best", "real_vs_simulated_worst"="real",
                      "short_interactions"="long", "simulated"="real", "simulated_worst_vs_real"="real", "simulation_quality_best"="sim-worst",
                      "simulation_quality_worst"="sim-best", "task_failed"="success", "task_successful"="miss", "word_accuracy_100"="wa-60",
                      "word_accuracy_60"="wa-100"))
