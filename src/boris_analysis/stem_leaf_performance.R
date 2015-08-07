library(RMongo)

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)


classifier <- dbGetDistinct(cross_validation, "performance", key = 'classifier_name')

for (c in classifier) {
  print(sprintf("Classifier: %s", c))
  query = sprintf('{"classifier_name": "%s"}', c)
  p.c <- dbGetQuery(cross_validation, "performance", query, 0, 0)
  stem(p.c$f_measure)
}
