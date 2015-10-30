library(RMongo)

to_file <- TRUE

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)
classifier <- dbGetDistinct(cross_validation, "performance", key = 'classifier_name')

for (c in classifier) {
  print(sprintf("Classifier: %s", c))
  query = sprintf('{"classifier_name": "%s", "f_measure": {$gte: 0.5}}', c)
  p.c <- dbGetQuery(cross_validation, "performance", query, 0, 0)
  if (to_file) {
    file_name <- sprintf('stem_leaf_%s.txt', c)
    
    fileConn<-file(file_name)
    # content <- latexTranslate(capture.output(stem(p.c$f_measure)))
    content <- capture.output(stem(p.c$f_measure))
    writeLines(content, fileConn)
    close(fileConn)
  } else {
    stem(p.c$f_measure)
  }
}
