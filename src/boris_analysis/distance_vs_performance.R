library(RMongo)
library(plyr)
library(ggplot2)

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)

####
# Auflistung aller Maße die ale Klassifikator einen Wert größer 0.5 haben

f_05 <- dbGetQuery(cross_validation, "distance_performance", '{"f_measure": {$gte: 0.5, $lt: 0.6}}', 0, 0)
f_06 <- dbGetQuery(cross_validation, "distance_performance", '{"f_measure": {$gte: 0.6, $lt: 0.7}}', 0, 0)
f_07 <- dbGetQuery(cross_validation, "distance_performance", '{"f_measure": {$gte: 0.7, $lt: 0.8}}', 0, 0)
f_08 <- dbGetQuery(cross_validation, "distance_performance", '{"f_measure": {$gte: 0.8, $lt: 0.9}}', 0, 0)
f_09 <- dbGetQuery(cross_validation, "distance_performance", '{"f_measure": {$gte: 0.9}}', 0, 0)

f_05 <- f_05[, c(4,6)]
f_05$range <- '05'
f_06 <- f_06[, c(4,6)]
f_06$range <- '06'
f_07 <- f_07[, c(4,6)]
f_07$range <- '07'
f_08 <- f_08[, c(4,6)]
f_08$range <- '08'
f_09 <- f_09[, c(4,6)]
f_09$range <- '09'

counts <- rbind(f_05, f_06, f_07, f_08, f_09)

# Ausgabe wieviel Klassifikatoren mit f > [0.6 - 1.0] exisitieren
cast( count(counts, c('data_set', 'classifier', 'range') ), data_set+classifier~range, fill=0)




####
# Exemaplarisch für Klassifikation für Nutzerbewertung ein Historamm für alle Klassifikatoren > 0.5
query = '{"data_set": "user_judgement", "f_measure": {$gt: 0.5}}' 
dp <- dbGetQuery(cross_validation, "distance_performance", query, 0, 0)

ggplot(dp, aes(x = f_measure, y = distance, color=classifier)) + 
  geom_point()
  #xlim(0, 1) +
  #ylim(0, 1)

ggplot(data = dp, aes(x=f_measure, fill=classifier)) +
  geom_histogram(binwidth=.01, alpha=.5, position="dodge")


