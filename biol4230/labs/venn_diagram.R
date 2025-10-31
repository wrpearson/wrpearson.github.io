Venn2 <- function(set1, set2, names)
{
  stopifnot( length(names) == 2)
 
  # Form universe as union of all three sets
  universe <- sort( unique( c(set1, set2) ) )
 
  Counts <- matrix(0, nrow=length(universe), ncol=2)
  colnames(Counts) <- names
 
  for (i in 1:length(universe))
  {
    Counts[i,1] <- universe[i] %in% set1
    Counts[i,2] <- universe[i] %in% set2
  }
 
  vennDiagram( vennCounts(Counts) )
}
