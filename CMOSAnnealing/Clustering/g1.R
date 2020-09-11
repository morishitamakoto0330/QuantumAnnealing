library(reshape2)
library(ggplot2)

# get data
d1 <- read.table("sample.csv", header=T, sep=",")

# plot
g1 <- ggplot(d1, aes(x=LoopSize, y=Operation, color=OptimalNumberOfThreads))
g2 <- g1 + layer(geom="point", stat="identity", position="identity")
g3 <- g2 + scale_x_log10() + scale_y_log10()

g3


