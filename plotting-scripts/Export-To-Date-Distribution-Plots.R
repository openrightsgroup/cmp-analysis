# Preamble: set the path to the directory that the checkedout git repo is in - need to do this in order to load the data
gitRepoPath <- "/Users/mrowe/Documents/Git/cmp-analysis"

# Read in the export file
data <- read.table(paste(gitRepoPath,"/data/export.csv", sep=""), sep=",", fill=T, header=T)

#Element Names: 'URL','URL Submission Timestamp','Network Name','Filter Level','Status','Result Timestamp','HTTP Status','Probe Config'

# Plot 1: show has many probe requests have been made so far against each provider
print(pdf(paste(gitRepoPath,"/plotting-scripts/plots/probe-requests-per-isp-to-date.pdf", sep="")), height=5, width=5)
par(mfrow=c(1,1),mar=c(4,15,2,1))
freq <- as.numeric(table(data$Network.Name))
labels <- names(table(data$Network.Name))
probeRequests <- data.frame(Network.Name = labels, Request.Count = freq)
rankedProbeRequests <- probeRequests[with(probeRequests, order(-Request.Count)),]
barplot(rankedProbeRequests[,2], names.arg=rankedProbeRequests[,1], horiz=T, las=1, main=("Per-ISP Probe Requests To Date"))
print(dev.off())

# Plot 2: show the distribution of different statuses
print(pdf(paste(gitRepoPath, "/plotting-scripts/plots/per-probe-status-distribution-to-date.pdf", sep="")), height=5, width=5)
par(mfrow=c(1,1),mar=c(4,5,2,1))
freq <- as.numeric(table(data$Status))
labels <- names(table(data$Status))
probeStatuses <- data.frame(Status = labels, Request.Count = freq)
rankedProbeStatuses <- probeStatuses[with(probeStatuses, order(-Request.Count)),]
barplot(rankedProbeStatuses[,2], names.arg=rankedProbeStatuses[,1], horiz=T, las=1, main=("Probe Status Distribution To Date"))
print(dev.off())

# Plot 3: show the distribution of blocks per ISP
print(pdf(paste(gitRepoPath, "/plotting-scripts/plots/per-isp-blocked-pages-to-date.pdf", sep="")), height=5, width=5)
par(mfrow=c(1,1),mar=c(4,15,2,1))
# Get the records from the data object that describe blocked requests
blocked <- data[which(data$Status == 'blocked'),]
# Gauge the frequency of these per ISP
freq <- as.numeric(table(blocked$Network.Name))
labels <- names(table(blocked$Network.Name))
blockedPages <- data.frame(Network.Name = labels, Block.Count = freq)
rankedBlockedPages <- blockedPages[with(blockedPages, order(-Block.Count)),]
barplot(rankedBlockedPages[,2], names.arg=rankedBlockedPages[,1], horiz=T, las=1, main=("Per-ISP #Blocked Pages To Date"))
print(dev.off())

# Plot 4: show the distribution of blocks per domain
# Preamble: run python ComputeBlockedEntries code first
# Set the number of entries to show in the plot - as this can be huge
n = 40
# Print this
print(pdf(paste(gitRepoPath,"/plotting-scripts/plots/blocks-per-domain-to-date.pdf", sep="")), height=5, width=5)
par(mfrow=c(1,1),mar=c(2,10,2,1))
perDomainBlockCounts <- read.table(paste(gitRepoPath,"/data/domainToBlockCount.tsv", sep=""), sep="\t", fill=T, header=T)
rankedPerDomainBlockCounts <- perDomainBlockCounts[with(perDomainBlockCounts, order(-Block.Count)),]
barplot(rankedPerDomainBlockCounts[1:40,2], names.arg=rankedPerDomainBlockCounts[1:40,1], horiz=T, las=1, main=paste("Per-domain Blocks To Date - Top-", n, sep=""))
print(dev.off())