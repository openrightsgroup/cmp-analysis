# Preamble: set the path to the directory that the checkedout git repo is in - need to do this in order to load the data
gitRepoPath <- "/home/rowem/Documents/Git/cmp-analysis"

# list the per-isp blocked domain files in the directory
perISPUnblocksFiles <- list.files(path = paste(gitRepoPath, "/data/per-isp-filter/unblocks/", sep=""))
options(digits=10)

for (ispFile in perISPUnblocksFiles) {
  # Get the name of the filter by stripping out the trailing content
  filterName <- gsub("_unblock_dist.csv","",ispFile)    
  print(filterName)
  
  # Read in each filter's block counts to date
  data_r <- read.table(paste(gitRepoPath,"/data/per-isp-filter/unblocks/", ispFile, sep=""), sep=",", header=F, stringsAsFactors=F)  
  data_m <- data.matrix(data_r) / 60
    
#   # Plot the number of blocks per domain to date
   print(pdf(paste(gitRepoPath, "/plotting-scripts/plots/per-isp-filter/", filterName, "-unblock-dist.pdf", sep=""), height=5, width=5))
   print(par(mfrow=c(1,1), mar=c(4.5,4.5,1.5,1), oma=c(0.5,0.5,0.5,0.5)))
   plot(density(data_m), 
        col="darkgreen", 
        xlab=expression(Delta), 
        ylab="Density", 
        lwd=1,cex=1.5, 
        cex.axis=1.5, cex.lab=1.5, 
        main=filterName)   
   
   print(dev.off())
}
