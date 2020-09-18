library(reshape2)
library(ggplot2)

# get data
d1 <- read.table("sample_3.csv", header=T, sep=",")

# plot
g1 <- ggplot(d1, aes(x=MatrixSize, y=NumberOfThreads, color=OptimalBlockSize))
g2 <- g1 + layer(geom="point", stat="identity", position="identity")
g3 <- g2 + scale_x_log10()

g3


