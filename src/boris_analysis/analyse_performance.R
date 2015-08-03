library(RMongo)
library(plyr)
library(ggplot2)

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)

performance <- dbGetQuery(cross_validation, "performance", '{}', 0, 0)
distances <- dbGetQuery(cross_validation, "distances", '{}', 0, 0)


ggplot(data = performance, aes(x=f_measure, fill=classifier_name)) +
  geom_histogram(binwidth=.01, alpha=.5, position="identity")

ggplot(data = performance, aes(x=f_measure, colour=classifier_name)) +
  geom_density()

boxplot(performance$f_measure ~ as.factor(performance$classifier_name))

ddply(performance, c('criteria', 'classifier_name'), summarise, min = min(f_measure), max = max(f_measure), mean = mean(f_measure), sd = sd(f_measure))




