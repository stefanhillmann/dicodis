library(RMongo)
library(plyr)

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)

d <- dbGetQuery(cross_validation, 
                "documents_result", 
                '{"classifier_name": "cosine", "frequency_threshold": 1, "n_gram_size": 1, "criteria": "short_interactions", "smoothing_value": 0.5}',
                0, 0)

#d$response <- 0
#d$response[which(d$true_class == 'positive')] <- 1
d$score <- d$positive_class_distance - d$negative_class_distance
d$score[which(d$score < 0)] <- 0

d <- arrange(d, document_id)

roc <- roc(d$true_class,
          d$score,
          levels = c('positive', 'negative'),
          percent=FALSE)
auc(roc)
plot(roc)

rd <- dbGetQuery(cross_validation, 
                 "documents_result", 
                 '{"classifier_name": "cosine", "frequency_threshold": 1, "n_gram_size": 1, "criteria": "long_interactions", "smoothing_value": 0.5}',
                 0, 0)

#rd$response <- 0
#rd$response[which(rd$true_class == 'positive')] <- 1
rd$score <- rd$positive_class_distance - rd$negative_class_distance
#rd$score[which(rd$score < 0)] <- 0

plot(roc(rd$true_class,
         rd$score,
         levels = c('positive', 'negative'),
         percent=FALSE))


compute_auc <- function(classifier_name, frequency_threshold, n_gram_size, criteria, smoothing_value, db_connection) {
  query <- sprintf('{"classifier_name": "%s", "frequency_threshold": %d, "n_gram_size": %d, "criteria": "%s", "smoothing_value": %f}',
                   classifier_name, frequency_threshold, n_gram_size, criteria, smoothing_value)
  
  sceanrio <- dbGetQuery(db_connection, "documents_result", query, 0, 0)
  
  roc <- roc(sceanrio$true_class,
             sceanrio$positive_class_distance - sceanrio$negative_class_distance,
             levels = c('positive', 'negative'))
  
  return(roc$auc)
  
}

cross_validation <- mongoDbConnect("classification_cross_validation", "localhost", 27017)
auc <- compute_auc('cosine', 1, 1, 'long_interactions', 0.5, cross_validation)
auc






