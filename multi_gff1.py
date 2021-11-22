#!/usr/bin/env python
# coding: utf-8

# In[63]:
import subprocess,os

DirLs = os.listdir(os.getcwd())
genomes = []
gffs = []

for i in DirLs:
    if i.endswith('.fna'):
        genomes.append(i)
    elif i.endswith('.gff'):
        gffs.append(i)
        
if len(genomes) != len(gffs):
    print("error message")
    
for j in range(len(genomes)):
    gff = []
    ref = genomes[j][:-12]
    print(j)
    if genomes[j].startswith(ref) and genomes[j].endswith('fna'):
        genome = genomes[j]
    if gffs[j].startswith(ref) and gffs[j].endswith('gff'):
        gff = gffs[j]
    subprocess.run(['gffread', gff, '-g', genome, '--merge', '-x',ref+'_mRNA','-y' ,ref+'_Prots'])
    subprocess.run(['Echo', 'Iteration '+ str(j+1)+'/'+str(len(genomes)), 'Protein File created as', ref+'_Prots'])
    subprocess.run(['Echo', 'Iteration '+ str(j+1)+'/'+str(len(genomes)), 'mRNA File created as', ref+'_mRNA'])
