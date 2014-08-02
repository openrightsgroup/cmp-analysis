cmp-analysis - Plotting Scripts
============

This directory contains the R scripts to plot the exported probe result data.

To run and plot distributions:

1. Download the latest version of the probe data export from ORG from [here](https://api.blocked.org.uk/data/export.csv.gz) into the /<local-git-repo>/cmp-analysis/data directory, and extract it (you should then get an export.csv file)

2. cd into <local-git-repo>/cmp-analysis/statistics-computation and then run 'python ComputeBlockedEntries.py' to compute statistics data for plotting

3. cd into <local-git-repo>/cmp-analysis/plotting-scripts and edit Export-Plots.R and set the preamble variable 'gitRepoPath' to point to the <local-git-repo>

4. Run Export-Plots.R to produce PDF files of to-date statistics of blocks

Get involved!
-------------

We welcome new contributors especially - we hope you find getting involved both easy and fun. All you need to get started is a github account.

Please see our [issues repository](https://github.com/openrightsgroup/cmp-issues) for details on how to join in.

License and credits
-------------------

Content is released under a [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) licence.
Data is released under a [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) licence.
Code is released under the General Public Licence version 3.

We reused the following software and creative components to make this:

- Nothing here yet...

Thanks!
