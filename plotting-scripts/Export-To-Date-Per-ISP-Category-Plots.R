# Preamble: set the path to the directory that the checkedout git repo is in - need to do this in order to load the data
gitRepoPath <- "/Users/mrowe/Documents/Git/cmp-analysis"

# list the per-isp blocked domain files in the directory
perISPBlockFiles <- list.files(path = paste(gitRepoPath, "/data/per-isp-filter/categories/", sep=""))
n = 20

# ispBlockFile = "BT_categoriesToBlockCount4.tsv"
for (ispBlockFile in perISPBlockFiles) {
  # Get the name of the filter by stripping out the trailing content
  
  filterName <- gsub("_categoriesToBlockCount"," d=",ispBlockFile)    
  filterName <- gsub(".tsv", "", filterName)
  print(filterName)
  
  # Read in each filter's block counts to date
  perCategoryBlockCounts <- read.table(paste(gitRepoPath,"/data/per-isp-filter/categories/", ispBlockFile, sep=""), sep="\t", fill=T, header=T)
  
  # Plot the number of blocks per domain to date
  print(png(paste(gitRepoPath, "/plotting-scripts/plots/per-isp-filter/", filterName, "-blocked-categories-to-date.png", sep="")), height=10, width=10, units="px", pointsize=12)
  par(mfrow=c(1,1),mar=c(2,25,2,1))  
  rankedPerCategoryBlockCounts <- perCategoryBlockCounts[with(perCategoryBlockCounts, order(-Block.Count)),]
  cat_names = rankedPerCategoryBlockCounts[1:40,1]
  cat_names <- strtrim(cat_names, 55)
  X <- barplot(rankedPerCategoryBlockCounts[1:40,2], 
          names.arg=cat_names, horiz=T, las=1,
               main=paste(filterName, sep=""), adj=0,
               space=c(1, 1, 1, 1), 
               col=rainbow(5))
#   text(cex=1, x=x, y=-10, rankedPerCategoryBlockCounts[1:40,1], xpd=TRUE, srt=60, adj=c(1,0))
#   x <- barplot(rankedPerCategoryBlockCounts[1:40,2], 
#           horiz=F, las=1, 
#           main=paste(filterName, " Top-", n, sep=""),
#           xaxt="n")
#   text(cex=1, x=x, y=-10, rankedPerCategoryBlockCounts[1:40,1], xpd=TRUE, srt=60, adj=c(1,0))
  print(dev.off())  
}