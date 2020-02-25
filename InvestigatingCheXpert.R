library(stringr)

df = read.csv('~/GitHub/statistical_simulation/data/train.csv')
path = str_split_fixed(df$Path,'/',5)
barplot(table(path[,3]))

patientStudies = as.numeric(str_remove_all(path[,3],'[patient]'))

hist(patientStudies,breaks=100)

