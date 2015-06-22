library("TTR")

## Preamble: set the path to the directory that the checkedout git repo is in - need to do this in order to load the data
gitRepoPath <- "/Users/mrowe/Documents/Git/cmp-analysis"
outputFilesDir <- paste(gitRepoPath, "/data/output/", sep="")

# List the output files
perISPFiles <- list.files(path = outputFilesDir)

afterFirst = FALSE
for (file in perISPFiles) {
  # Read in the per ISP output
  pathToFile <- paste(outputFilesDir, file, sep="")  
  data <- read.table(pathToFile, sep=",")
  filterName <- gsub("_ts_accuracy.tsv","",file)
  
  print(pdf(paste(gitRepoPath, "/plotting-scripts/plots/accuracy/", filterName, "-ts-accuracy.pdf", sep=""), height=2.5, width=10))
  print(par(mfrow=c(1,1), mar=c(4.5,3,1.5,0.5), oma=c(0.5,0.5,0.5,0.5)))
  f1_ts <- SMA(data[,10], n=5)
  plot(f1_ts, xlab="Weeks", type="l", ylab="", ylim=c(0,1.1), col="darkgreen", cex=1.5, cex.axis=1.5, cex.lab=1.5, main=filterName, las=1)  
  if(!afterFirst) {
    print("Add legend")
    legend("topright", c("F1", "Precision", "Recall", "FPR", "MCC"), 
           col=c("darkgreen", "darkblue", "darkred", "darkred", "darkblue"), 
           lty=c(1,1,1,2,2), 
           horiz=T, 
           bty="n", 
           cex=1.2)
    afterFirst = TRUE
  }
  
  prec_ts <- SMA(data[,6], n=5)
  lines(prec_ts, col="darkblue")
  
  rec_ts <- SMA(data[,7], n=5)
  lines(rec_ts, col="darkred")
  
  fpr_ts <- SMA(data[,8], n=5)
  lines(fpr_ts, col="darkred", lty=2) 
  
  mcc_ts <- SMA(data[,9], n=5)
  lines(mcc_ts, col="darkblue", lty=2)
  
  print(dev.off())
}