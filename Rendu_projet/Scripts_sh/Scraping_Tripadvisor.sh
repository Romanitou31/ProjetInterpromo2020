#!/bin/sh
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=24CPUNodes
#SBATCH --mail-type=END
#SBATCH --mail-user=romain.sedran@univ-tlse3.fr
#SBATCH --job-name=Scraping_Tripadvisor
#SBATCH --output=../OUTPUT_PROGRAMME/Scraping_Tripadvisor.out
#SBATCH --error=../ERREUR_PROGRAMME/Scraping_Tripadvisor.err
srun singularity exec /logiciels/containerCollections/CUDA9/vanilla_9.2.sif ../Collecte_de_donnees/bin/python Scraping_Tripadvisor.py
