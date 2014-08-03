# Preamble: set the path to the directory that the checkedout git repo is in - need to do this in order to load the data
gitRepoPath <- "/Users/mrowe/Documents/Git/cmp-analysis"

# list the per-isp blocked domain files in the directory
perISPBlockFiles <- list.files(path = paste(gitRepoPath, "/data/per-isp-filter/", sep=""))

for (ispBlockFile in perISPBlockFiles) {
  # Get the name of the filter by stripping out the trailing content
  filterName <- gsub("_domainToBlockCount.tsv","",ispBlockFile)    
  print(filterName)
  
  # Read in each filter's block counts to date
  perDomainBlockCounts <- read.table(paste(gitRepoPath,"/data/per-isp-filter/", ispBlockFile, sep=""), sep="\t", fill=T, header=T)
  
  # Plot the number of blocks per domain to date
  print(png(paste(gitRepoPath, "/plotting-scripts/plots/per-isp-filter/", filterName, "-blocked-pages-to-date.png", sep="")), height=5, width=5)
  par(mfrow=c(1,1),mar=c(2,10,2,1))  
  rankedPerDomainBlockCounts <- perDomainBlockCounts[with(perDomainBlockCounts, order(-Block.Count)),]
  barplot(rankedPerDomainBlockCounts[1:40,2], names.arg=rankedPerDomainBlockCounts[1:40,1], horiz=T, las=1, main=paste(filterName, ": Per-domain Blocks To Date - Top-", n, sep=""))
  print(dev.off())  
}


# # Read in the export file
# 
# 
# # Plot 3: show the distribution of blocks per ISP

