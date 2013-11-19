data <- read.csv(file="2013_08_08__11_04_49__results.csv")
data$n <- as.factor(data$n)
data$Freq..Threshold <- as.factor(data$Freq..Threshold)

length_of_interaction <- data[data$Criteria=='length_of_interaction',]
task_usccess <- data[data$Criteria=='task_success',]
word_accuracy <- data[data$Criteria=='word_accuracy',]
aggdata <- aggregate(word_accuracy$F.Measure, list(word_accuracy$n, word_accuracy$Freq..Threshold), mean)


# qplot(Classifier, F.Measure, data = length_of_interaction, geom = "boxplot") + facet_grid(~ Criteria)