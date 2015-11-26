library(RMongo)
library(plyr)
library(ggplot2)
library(scatterplot3d)

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)

performance <- dbGetQuery(cross_validation, "performance", '{}', 0, 0)
distances <- dbGetQuery(cross_validation, "distances", '{}', 0, 0)


ggplot(data = performance, aes(x=f_measure, fill=classifier_name)) +
  geom_histogram(binwidth=.01, alpha=.5, position="identity")

ggplot(data = performance, aes(x=f_measure, colour=classifier_name)) +
  geom_density()

boxplot(performance$f_measure ~ as.factor(performance$classifier_name))

ddply(performance, c('criteria', 'classifier_name'), summarise, min = min(f_measure), max = max(f_measure), mean = mean(f_measure), sd = sd(f_measure))

# f vs n
performance.cosine = dbGetQuery(cross_validation, "performance", '{"classifier_name": "cosine"}', 0, 0)
performance.cosine$frequency_threshold <- as.factor(performance.cosine$frequency_threshold)

ggplot(data = performance.cosine, aes(x = n_gram_size, y = f_measure, fill = frequency_threshold)) + 
  geom_bar(stat="identity", position=position_dodge())


performance.cosine = dbGetQuery(cross_validation, "performance", '{"classifier_name": "cosine", "smoothing_value": 0.05}', 0, 0)
performance.cosine$frequency_threshold <- as.factor(performance.cosine$frequency_threshold)
d <- summarySE(performance.cosine, "f_measure", c("n_gram_size","criteria"))
d$n_gram_size <- factor(d$n_gram_size)

ggplot(d, aes(x=criteria, y=f_measure, fill=n_gram_size)) + 
  geom_bar(position=position_dodge(), stat="identity") +
  geom_errorbar(aes(ymin=f_measure-sd, ymax=f_measure+sd),
                width=.2,                    # Width of the error bars
                position=position_dodge(.9))


# f vs t ans s
with(performance.cosine, {
  scatterplot3d(x = frequency_threshold, y = smoothing_value, z = f_measure, color = n_gram_size)
})

ddply(performance.cosine, c('frequency_threshold', 'smoothing_value', 'n_gram_size'), summarize, mean = mean(f_measure), sd = sd(f_measure))

boxplot(performance.cosine$f_measure ~ as.factor(performance.cosine$n_gram_size))



ggplot(data = d, aes(x = n_gram_size, y = f_measure, fill = frequency_threshold)) + 
  geom_bar(stat="identity", position=position_dodge())