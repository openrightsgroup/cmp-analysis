library(zoo)

# Preamble: set the path to the directory that the checkedout git repo is in - need to do this in order to load the data
gitRepoPath <- "/home/rowem/Documents/Git/cmp-analysis"

# Read in the export file
z <- read.zoo(paste(gitRepoPath,"/data/dateToRequestCount.tsv", sep=""), sep="\t", fill=T, header=T)

print(pdf(paste(gitRepoPath, "/plotting-scripts/plots/ts-global-requests.pdf", sep=""), height=2.5, width=10))
print(par(mfrow=c(1,1), mar=c(4.5,5,1.5,0.5), oma=c(0.5,0.5,0.5,0.5)))
plot(z, col="darkgreen", xlab="Time", ylab="Request Count", lwd=1,cex=1.5, cex.axis=1.5, cex.lab=1.5, xaxt="n", main="Global")
ticks <- seq(time(z)[1], time(z)[length(z)], by = "1 month") #I make some ticks
axis(1, at = ticks, labels = format(ticks, "%b-%y"), )
print(dev.off())