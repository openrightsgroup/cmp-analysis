library(zoo)
# Preamble: set the path to the directory that the checkedout git repo is in - need to do this in order to load the data
gitRepoPath <- "/home/rowem/Documents/Git/cmp-analysis"

# list the per-isp blocked domain files in the directory
perISPRequestCountFiles <- list.files(path = paste(gitRepoPath, "/data/per-isp-filter/requests/", sep=""))

for (ispFile in perISPRequestCountFiles) {
  # Get the name of the filter by stripping out the trailing content
  filterName <- gsub("_dateToRequestCount.tsv","",ispFile)    
  print(filterName)
  
  # Read in each filter's block counts to date
  z <- read.zoo(paste(gitRepoPath,"/data/per-isp-filter/requests/", ispFile, sep=""), sep="\t", fill=T, header=T)
  
  # Plot the number of blocks per domain to date
  print(pdf(paste(gitRepoPath, "/plotting-scripts/plots/per-isp-filter/", filterName, "-ts-requests.pdf", sep=""), height=2.5, width=10))
  print(par(mfrow=c(1,1), mar=c(4.5,5,1.5,0.5), oma=c(0.5,0.5,0.5,0.5)))
  plot(z, col="darkgreen", xlab="Time", ylab="Request Count", lwd=1,cex=1.5, cex.axis=1.5, cex.lab=1.5, xaxt="n", main=filterName)
  ticks <- seq(time(z)[1], time(z)[length(z)], by = "1 month") #I make some ticks
  axis(1, at = ticks, labels = format(ticks, "%b-%y"), )
  print(dev.off())
}

# 
# # Read in the export file
# 
# 
# print(pdf(paste(gitRepoPath, "/plotting-scripts/plots/ts_global_requests.pdf", sep=""), height=2.5, width=10))
# print(par(mfrow=c(1,1), mar=c(4.5,5,1.5,0.5), oma=c(0.5,0.5,0.5,0.5)))
# plot(z, col="darkgreen", xlab="Time", ylab="Request Count", lwd=1,cex=1.5, cex.axis=1.5, cex.lab=1.5, xaxt="n")
# ticks <- seq(time(z)[1], time(z)[length(z)], by = "1 month") #I make some ticks
# axis(1, at = ticks, labels = format(ticks, "%b-%y"), )
# print(dev.off())