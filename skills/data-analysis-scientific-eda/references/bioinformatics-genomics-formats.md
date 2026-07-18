# Bioinformatics & Genomics Formats

Sequence data, alignments, annotations, variants, and expression/omics. Columns: **ext · format · read with · EDA focus**.

## Sequence Data

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.fasta`/`.fa`/`.fna` | FASTA | `Biopython SeqIO`, `pyfaidx` | sequence count, length distribution, GC content, N content, duplicates, assembly N50/L50 |
| `.fastq`/`.fq` | FASTQ (reads + quality) | `Biopython SeqIO`, `pysam`, `HTSeq` | read count, length dist, per-base/per-read quality, GC bias, duplication, adapters, Phred33/64 |
| `.sff` | 454 flowgram | `Biopython SeqIO('sff')` | read count/length, flowgram quality, key/adapter detection |
| `.ab1`/`.scf` | Sanger trace | `Biopython('abi')`, `tracy` | base-call quality, trace SNR, mixed-base/heterozygosity, quality region |
| `.embl`/`.genbank`/`.gb` | annotated sequence | `Biopython SeqIO` | feature types, CDS/translation validation, annotation completeness, source organism |

## Alignments

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.sam` | Sequence Alignment/Map | `pysam`, `HTSeq` | mapping rate/quality, coverage, insert size, flags, CIGAR, mismatch/indel rate |
| `.bam` | binary SAM | `pysam`, `bamnostic` | as SAM + compression, `.bai` index, per-chrom stats, strand bias, read groups |
| `.cram` | reference-compressed | `pysam` (+ reference) | compression vs BAM, reference dependency, lossy assessment |
| `.maf`/`.axt`/`.chain`/`.psl` | multiple/pairwise alignment, chains | `Biopython AlignIO`, `bx-python`, `pyliftover` | block stats, species coverage, identity %, gaps, synteny, mapping quality |
| `.phylip`/`.nexus`/`.nwk`/`.newick` | phylogenetic | `Biopython Phylo`, `ete3`, `dendropy` | tree tips/nodes, branch length dist, balance, bootstrap support, topology |

## Genomic Features & Signal

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.bed` | genomic intervals | `pybedtools`, `pyranges`, `pandas` | feature count/size, chrom distribution, strand, score dist, overlaps, coverage |
| `.bedGraph` | per-base signal | `pybedtools`, `pyBigWig` | signal stats, genome coverage %, peaks/valleys, zero-coverage regions |
| `.bigWig`/`.bw` | indexed signal | `pyBigWig`, `pybbi` | genome-wide summaries, zoom levels, regional extraction, S/N (ChIP/ATAC) |
| `.bigBed`/`.bb` | indexed BED | `pybbi`, `pybigtools` | feature density, interval queries, size stats |
| `.wig` | wiggle | `pyBigWig`, custom | signal stats, fixedStep vs variableStep, span |
| `.narrowPeak`/`.broadPeak` | ENCODE peaks | `pybedtools`, custom | peak count/width, signal dist, p/q-values, summits, feature overlap |
| `.gff`/`.gff3` | annotations | `gffutils`, `pyranges`, `BCBio.GFF` | feature-type distribution, gene-model validity, strand balance, CDS phase, per-gene exon/intron |
| `.gtf` | gene transfer | `pyranges`, `gffutils`, `HTSeq` | isoforms, transcript length, exon-number dist, biotypes, overlapping genes |

## Variants

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.vcf` | Variant Call Format | `pysam.VariantFile`, `cyvcf2` | count by type (SNP/indel/SV), quality dist, allele-freq spectrum, Ts/Tv, heterozygosity, missing GT, HWE |
| `.bcf` | binary VCF | `pysam`, `cyvcf2` | as VCF + compression, indexing, read performance |
| `.gvcf` | genomic VCF | `pysam` | reference blocks, coverage uniformity, variant density, per-position GQ |

## Expression & Single-Cell

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.counts` | gene count matrix | `pandas`, `scanpy` | library size, detection rate, zero-inflation, replicate correlation, PCA |
| `.tpm`/`.fpkm` | normalized expression | `pandas`, `anndata` | expression dist, highly-expressed genes, batch effects, CV, dynamic range |
| `.mtx` | Matrix Market (sparse) | `scipy.io.mmread`, `scanpy` | sparsity, cell/gene filtering thresholds, mito fraction, UMI dist, doublets |
| `.h5ad` | AnnData | `scanpy`, `anndata` | cell/gene counts, layer availability, embeddings (PCA/UMAP), QC metrics, batch, annotation coverage |
| `.loom` | Loom | `loompy`, `scanpy` | spliced/unspliced layers, row/col attributes, clusters, velocity metrics |
| `.rds`/`.Rdata` | R objects (Seurat) | `pyreadr`, `rpy2` | object type, structure, metadata, conversion to AnnData |
| `.cool`/`.mcool`/`.hic` | Hi-C contacts | `cooler`, `hicstraw` | resolution, contact stats, distance decay, compartments/TADs, normalization |
| `.2bit` | compact genome | `py2bit`, `twobitreader` | compression, random-access, masked regions, N content |
| `.sizes` | chromosome sizes | `pandas` | genome size, chrom count, karyotype validation |
| `.agp`/`.scaffolds`/`.contigs` | assembly | FASTA tools, QUAST | N50/N90, gap type/size, contiguity, BUSCO completeness |
