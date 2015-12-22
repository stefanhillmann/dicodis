library(RMongo)
library(plyr)
library(reshape2)

dialogue_db <- mongoDbConnect("dialogues", "localhost", 27017)
all <- dbGetQuery(dialogue_db, "dialogues", "", 0, 0)

real_user <- subset(all, corpora == "real user")
simulation_good <- subset(all, corpora == "simulation good")
simulation_bad <- subset(all, corpora == "simulation bad")

print("Unique values  for real user")
sort(unique(real_user$sysSA))
sort(unique(real_user$sysRep_field))
sort(unique(real_user$userSA))
sort(unique(real_user$userFields))

print("Unique values  for simulation good")
sort(unique(simulation_good$sysSA))
sort(unique(simulation_good$sysRep_field))
sort(unique(simulation_good$userSA))
sort(unique(simulation_good$userFields))

print("Unique values  for simulation bad")
sort(unique(simulation_bad$sysSA))
sort(unique(simulation_bad$sysRep_field))
sort(unique(simulation_bad$userSA))
sort(unique(simulation_bad$userFields))