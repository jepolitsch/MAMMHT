import subprocess,os
import argparse
from Bio import SeqIO
from BCBio import GFF

def setting():
    parser = argparse.ArgumentParser(prog='quantify and detect pathogens', usage='%(prog)s [options]')
    parser.add_argument("-w", "--workdir", nargs="?", default="/tmp/")
    # parser.add_argument('currentWD', help='folder where fastq file are located')#, widget='DirChooser')
    # parser.add_argument("-e", "--email", nargs="?", default="", help="email for blast search")
    # parser.add_argument("-s", "--search", nargs="?", default="", help="ncbi search to retrieve GIs")
    # parser.add_argument("-m", "--min",  default="0.01", help="minimum number of reads to plot a species as fraction of total mappd reads [0-1]")
    # parser.add_argument("-c", "--correct", action='store_true', help="correct or not reads via racon")
    # parser.add_argument("-a", "--assembled", action='store_true', help="assembled-reads")
    # parser.add_argument("-p", "--percentage", type = float, default="90", help="minimum identity to consider a valid alignment")
    # parser.add_argument("-mr", "--min_reads", type = float, default="100", help="minimum number of reads to sequence to consider a sample in the analysis")
    args = parser.parse_args()
    return args

def gffread():
    args = setting()
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

    for j in range(len(genomes)):
        gff = []
        ref = genomes[j][:-12]
        print(j)
        if genomes[j].startswith(ref) and genomes[j].endswith('fna'):
            genome = genomes[j]
        if gffs[j].startswith(ref) and gffs[j].endswith('gff'):
            gff = gffs[j]
        subprocess.run(['gffread', gff, '-g', genome, '--merge', '-x',ref+'_mRNA','-y' ,ref+'_Prots'])
        subprocess.run(['echo', 'Iteration '+ str(j+1)+'/'+str(len(genomes)), 'Protein File created as', ref+'_Prots'])
        subprocess.run(['echo', 'Iteration '+ str(j+1)+'/'+str(len(genomes)), 'mRNA File created as', ref+'_mRNA'])


# File Checks
def is_fasta(filename):
    try:
        with open(filename, "r") as handle:
            fasta = SeqIO.parse(handle, "fasta")
            return any(fasta)  # False when `fasta` is empty, i.e. wasn't a FASTA file

    except:
        print('check your genome file, they are not in fasta')

def is_gff(filename):
    try:
        in_handle = open(i)
        if GFF.parse(in_handle):
            return True
    except:
        print('not a gff files')


if __name__ == '__main__':
    gffread()

