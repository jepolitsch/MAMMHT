# MAMMHT

It is reccomended you use the Anaconda distribution of OrthoFinder, but local instalation will also work


```
conda install -c bioconda gffread 
conda install -c bioconda bcbio-gff
conda install -c bioconda orthofinder

```
Tool to find horizontal gene transfer events through bottom up hierarchical clustering of OrthoFinders ontology groups based on outliers in consensus tree

### Options:
-w <workingDirectory> specify working directory
  
#### Optional:
-o <ProtFolder> if empty, MAMMHT will not run orthofinder on your results, by default MAMMHT creats Prots folder with formatted inputs for OrthoFinder
-p <PairFile> if you have prepared a file with the pairwise couples of Genome Fasta and GFF file, specify here, or else MAMMHT will find the pairs in your cwd
  
 
  
  
