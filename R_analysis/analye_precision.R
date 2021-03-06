library(RMongo)
library(plyr)
library(ggplot2)
library(reshape2)

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)

####
# Auflistung aller Maße die ale Klassifikator einen Wert größer 0.5 haben

f_05 <- dbGetQuery(cross_validation, "distance_performance", '{"precision": {$gte: 0.5, $lt: 0.6}}', 0, 0)
f_06 <- dbGetQuery(cross_validation, "distance_performance", '{"precision": {$gte: 0.6, $lt: 0.7}}', 0, 0)
f_07 <- dbGetQuery(cross_validation, "distance_performance", '{"precision": {$gte: 0.7, $lt: 0.8}}', 0, 0)
f_08 <- dbGetQuery(cross_validation, "distance_performance", '{"precision": {$gte: 0.8, $lt: 0.9}}', 0, 0)
f_09 <- dbGetQuery(cross_validation, "distance_performance", '{"precision": {$gte: 0.9}}', 0, 0)

f_05 <- f_05[, c(4,8)]
f_05$range <- '05'
f_06 <- f_06[, c(4,8)]
f_06$range <- '06'
f_07 <- f_07[, c(4,8)]
f_07$range <- '07'
f_08 <- f_08[, c(4,8)]
f_08$range <- '08'
f_09 <- f_09[, c(4,8)]
f_09$range <- '09'

counts <- rbind(f_05, f_06, f_07, f_08, f_09)

# Ausgabe wieviel Klassifikatoren mit f > [0.6 - 1.0] exisitieren
counts_summarized <- count(counts, c('data_set', 'classifier', 'range'))
precision_results <- dcast(counts_summarized, data_set+classifier~range, fill=0)

# bar graph: frequency for range, grouped by data_set
ggplot(data = count(counts, c('data_set', 'range')), aes(x=range, y=freq, fill=data_set)) +
  geom_bar(stat="identity", position=position_dodge(), colour="black")

