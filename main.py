import subprocess
import os
import argparse
from Bio import SeqIO
from BCBio import GFF

def setting():
    parser = argparse.ArgumentParser(prog='quantify and detect pathogens', usage='%(prog)s [options]')
    parser.add_argument("-w", "--workdir", nargs="?", default="/tmp/")
    # parser.add_argument('currentWD', help='folder where fastq file are located')#, widget='DirChooser')
    parser.add_argument("-p", "--pairlist", nargs="?", default=False, help="if you have prepared a list of GFF:Genome-Fasta pairs, -p <pairfile>")
    parser.add_argument("-o", "--orthofinder", nargs="?", default=False, help="Optional Arg. To run orthofinder on the output, enter -o <Prot_directory>")
    # parser.add_argument("-m", "--min",  default="0.01", help="minimum number of reads to plot a species as fraction of total mappd reads [0-1]")
    # parser.add_argument("-c", "--correct", action='store_true', help="correct or not reads via racon")
    # parser.add_argument("-a", "--assembled", action='store_true', help="assembled-reads")
    # parser.add_argument("-p", "--percentage", type = float, default="90", help="minimum identity to consider a valid alignment")
    # parser.add_argument("-mr", "--min_reads", type = float, default="100", help="minimum number of reads to sequence to consider a sample in the analysis")
    args = parser.parse_args()
    return args

def gffread():
    DirLs = os.listdir(args.workdir)
    genomes = []
    gffs = []
    for i in DirLs:
        if is_fasta(i):
            genomes.append(i)
        elif is_gff(i):
            gffs.append(i)

    if len(genomes) != len(gffs):
        print("error message")
    counter = 1
    for j in genomes:
        ref = j[:-12]
        if j.startswith(ref):
            genome = j
        for i in gffs:
            if i.startswith(ref):
                gff = i
        if any(gff) and any(genome):
            gff_read(gff,genome,ref, counter, gffs)
            counter += 1
    print('done')
# File Checks

def gff_read(gff, genome, ref, counter, gffs):
    subprocess.run(['gffread', gff, '-g', genome, '--merge', '-x',ref+'_mRNA.faa','-y' ,ref+'_Prots.faa'])
    subprocess.run(['echo', 'Iteration '+str(counter) +'/'+ str(len(gffs)), 'Protein File created as',ref +'_Prots.faa'])
    subprocess.run(['echo', 'Iteration '+str(counter) +'/'+ str(len(gffs)), 'mRNA File created as',ref +'_mRNA.faa'])
    subprocess.run(['mv', ref+'_Prots.faa', 'Prots'])
    subprocess.run(['mv', ref +'_mRNA.faa', 'CodingSeqs'])
    subprocess.run(['mv', genome +'.fai', 'Fai'])

def is_gff(filename):
    try:
        in_handle = open(filename, 'r')
    except:
        return False
    try:
        for rec in GFF.parse(in_handle):
            return True
        in_handle.close()
    except:
        return False

def is_fasta(filename):
    file = filename
    try:
        with open(file, "r") as handle:
            try:
                fasta = SeqIO.parse(handle, "fasta")
                return any(fasta)
            except:
                return False
    except:
        return False

def trimmer():
    prot_dir = os.listdir(args.workdir + '/Prots/')
    for p in prot_dir:
        if p.endswith('.faa'): #fucking mac keeps making .DS_Store
            fin = open('Prots/'+p, 'r').readlines()
            fout = open('Prots/'+p, 'w')
            for line in fin:
                if not line.startswith('>'):
                    fout.write(line.replace('.', 'X'))
                else:
                    fout.write(line)
            fout.close()

if __name__ == '__main__':
    args = setting()
    os.chdir(args.workdir)
    subprocess.run(['mkdir', 'Prots'])
    subprocess.run(['mkdir', 'CodingSeqs'])
    subprocess.run(['mkdir', 'Fai'])
    if not args.pairlist:
        gffread()
    trimmer()
    if args.orthofinder:
        try:
            subprocess.run(['orthofinder','-f', args.orthofinder])
        except:
            print("No installation of orthofinder found, check conda environment")







