#Authors: Bernd Klaus and Alessandro Ori, modified by Jan Kosinski @ EMBL
#Added eta0 by Huy Bui
#Add args[3] to output individual R plot, which is disabled by default

#Running:
#Rscript <path>/pval_from_solutions.R

args = commandArgs(trailingOnly=TRUE)
# test if there is at least one argument: if not, return an error
if (length(args)==1) {
  args[2] = "correlation_about_mean"
}

if (length(args)==0) {
  args[1] = "solutions.csv"
  args[2] = "correlation_about_mean"
}


fn = args[1]
score = args[2]
if (length(args) == 3) {
	outfile = paste(args[3], '_pvalue.pdf', sep="")
	pdf(outfile)
}

print(score)

# install.packages('fdrtool')
# install.packages('psych')

library(fdrtool)
library(psych)

hit_data <- read.csv(fn, sep="")

# print(colnames(hit_data))
# head(hit_data)

if ("overlap" %in% colnames(hit_data)) {
    max_overlap = hit_data[1, "overlap"]
    overlap_thresh = 0.0
    hit_data_sub <- hit_data[hit_data[,'overlap'] > overlap_thresh*max_overlap,]
} else {
    hit_data_sub <- hit_data
}

# print(hit_data_sub)

min_score = -1.0
hit_data_sub <- hit_data_sub[hit_data_sub[,score] > min_score,]
## look at scores
hist(hit_data_sub[,score], breaks=100)

## do a z-transform
if (score == 'overlap') {
    scores_norm = 2*(hit_data_sub[,score] -min(hit_data_sub[,score]))/(max(hit_data_sub[,score])-min(hit_data_sub[,score]))-1 #rescale to -1 to 1
    hit_data_sub$score_z <- scores_norm
} else {
    hit_data_sub$score_z <- fisherz(hit_data_sub[,score])
}


hist(hit_data_sub$score_z, freq = FALSE, breaks=100)
## shifted or scaled!
## but "outliers" are clearly visibile!
# sort(hit_data_sub$score_z, decreasing = TRUE)[1:10]

# sum(hit_data_sub$score_z > 1.5)

## try a simple shift
hit_data_sub$score_z_c <- hit_data_sub$score_z-mean(hit_data_sub$score_z)
hist(hit_data_sub$score_z_c, breaks=30)

fdrtool_res_shift <- fdrtool(hit_data_sub$score_z_c , statistic =  "normal", cutoff.method="pct0", pct0=0.95)

hit_data_sub$pvalues <- fdrtool_res_shift$pval
hit_data_sub$eta0 <- fdrtool_res_shift$param[3]
hit_data_sub$pvalues_one_tailed <- ifelse(hit_data_sub$score_z_c > 0, hit_data_sub$pvalues/2, 1-hit_data_sub$pvalues/2)
hit_data_sub$BH_adjusted_pvalues <- p.adjust(fdrtool_res_shift$pval, method = "BH")
hit_data_sub$BH_adjusted_pvalues_one_tailed <- ifelse(hit_data_sub$score_z_c > 0, hit_data_sub$BH_adjusted_pvalues/2, 1-hit_data_sub$BH_adjusted_pvalues/2)
print("Best p-values:")
head(sort(hit_data_sub$pvalues), n=10)
print("Best adjusted p-values:")
head(sort(hit_data_sub$BH_adjusted_pvalues), n=10)

plot(sort(hit_data_sub$pvalues))
plot(sort(hit_data_sub$BH_adjusted_pvalues))

# sort(BH.adjusted.pvalues)[1:100]
outfn <- gsub (".csv", "_pvalues.csv", fn)
# write.csv(hit_data_sub, outfn)
write.csv(hit_data_sub[order(hit_data_sub[[score]], decreasing = TRUE),], outfn)
## outlier tests
boxplot(hit_data_sub$score_z_c)
boxplot.stats(hit_data_sub$score_z_c)

if (length(args) == 3) {
	dev.off()
}

## DEBUG Code


# sort(fdrtool_res_shift$pval)[1:10] 
# hist(fdrtool_res_shift$pval)
# sum(fdrtool_res_shift$pval < hc.thresh(fdrtool_res_shift$pval, alpha0=0.012))


