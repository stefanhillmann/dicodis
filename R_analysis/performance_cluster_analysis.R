library(RMongo)
library(reshape2)
library(car)

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)
p <- dbGetQuery(cross_validation, "performance", '{}', 0, 0)


# Einleitung
# ============
# Hinweise und Funktion wssplot von hier: http://www.r-statistics.com/2013/08/k-means-clustering-from-r-in-action/

wssplot <- function(data, nc=15, seed=1234){
  wss <- (nrow(data)-1)*sum(apply(data,2,var))
  for (i in 2:nc){
    set.seed(seed)
    wss[i] <- sum(kmeans(data, centers=i)$withinss)}
  plot(1:nc, wss, type="b", xlab="Number of Clusters",
       ylab="Within groups sum of squares")}


# Clustern über f-wert, smoothing value, n und frequeny threshold
# ===============================================================
p.features <- data.frame(f = p$f_measure, sv = p$smoothing_value, n = p$n_gram_size, ft = p$frequency_threshold)
mydata <- p.features
set.seed(1234)
wssplot(mydata)
r <- kmeans(mydata, 8)
t <- table(mydata$n, r$cluster)
randIndex(t)
plot3d(jitter(mydata$n), jitter(mydata$sv), mydata$ft, col=r$cluster)
# Es zeigt sich, dass der smoothing value wohl keinen Einfluß auf die Cluseterung hat

# Clustern über f-wert, n und frequeny threshold
# und OHNE smoothing value
# danach f-mass auf die Z-Achse bringen
# ===============================================================
p.features <- data.frame(f = p$f_measure, n = p$n_gram_size, ft = p$frequency_threshold)
mydata <- p.features
set.seed(1234)
wssplot(mydata)
r <- kmeans(mydata, 8)
t <- table(mydata$n, r$cluster)
randIndex(t)
plot(jitter(p.features$n), jitter(p.features$ft), col=r$cluster)
plot3d(jitter(mydata$n), mydata$ft, mydata$f, col=r$cluster)

# Clustern über f-wert, n und frequeny threshold, smoothing value und classifier
# ===============================================================
p.features <- data.frame(f = p$f_measure, n = p$n_gram_size, ft = p$frequency_threshold, c = p$classifier_name, sv = p$smoothing_value)
p.features$c <- as.numeric(factor(p.features$c))
mydata <- p.features

set.seed(1234)
wssplot(mydata)
r <- kmeans(mydata, 8)
t <- table(mydata$n, r$cluster)
randIndex(t)
plot3d(jitter(mydata$n), mydata$ft, jitter(mydata$c), col=r$cluster)