#!/bin/sh
#SBATCH --account=redditsa
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=12:00:00 
#SBATCH --mem=5G
#SBATCH --output=/project/redditsa/reddit-scraping/slurmOutput
#SBATCH --error=/project/redditsa/reddit-scraping/slurmError

module load miniconda3/4.12.0
conda activate ../redditSAModule/

python redditScrape.py
python sentimentAnalyzer.py