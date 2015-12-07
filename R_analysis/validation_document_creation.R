library(RMongo)
library(ggplot2)
library(plyr)
library(reshape2)

db <- mongoDbConnect("cross_validation_mixed_2015_12_03", "localhost", 27017)

neu <- dbGetQuery(db, "corpus_ngram_model_TEST", "", 0, 0)
alt <- dbGetQuery(db, "corpus_ngram_model", "", 0, 0)

alt$corpus <- revalue(alt$corpus, c("interaction long" = "a",
                               "interaction short" = "b",
                                "judged bad" = "c",
                               "judged good" = "d",
                               "real user" = "e",
                               "simulation bad" = "f",
                               "simulation good" = "g",
                               "task failed" = "h",
                               "task success" = "i",
                               "word accuracy 100" = "j",
                               "word accuracy 60" = "k" ))

neu$corpus <- revalue(neu$corpus, c("dialogues long" = "a",
                                    "dialogues short" = "b",
                                    "not successful" = "h",
                                    "real user" = "e",
                                    "simulation bad" = "f",
                                    "simulation good" = "g",
                                    "successful" = "i",
                                    "user judgment bad" = "c",
                                    "user judgment good" = "d",
                                    "word accuracy 100" = "j",
                                    "word accuracy 60" = "k"))

neu.sorted <- arrange(neu, corpus, n_gram, freq, n, f_min)
alt.sorted <- arrange(alt, corpus, n_gram, freq, n, f_min)

table(neu.sorted$n_gram == alt.sorted$n_gram)
