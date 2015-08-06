library(RMongo)

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)


classifier <- dbGetDistinct(cross_validation, "performance", key = 'classifier_name')

for (c in classifier) {
  print(c)
  query = sprintf('{"classifier_name": "%s"}', c)
  print(query)
  #p.c <- dbGetQuery(cross_validation, "performance", '{}', 0, 0)
  #stem()
}
