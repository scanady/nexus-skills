---
name: data-analysis-scientific-eda
disable-model-invocation: false
description: Profile a scientific data file — detect its format across chemistry, bioinformatics/genomics, microscopy/imaging, spectroscopy, proteomics/metabolomics, and general scientific types (200+ extensions), extract format-specific metadata and quality metrics, and produce a markdown EDA report with downstream-analysis recommendations. Use when asked to "analyze this .fastq/.mzML/.czi/.nd2", "what's in this scientific data file", or "profile this dataset before analysis". For classical statistical inference on tabular data, see the statistical-modeling skill.
license: MIT
metadata:
  version: "1.0.0"
  domain: data
  triggers: analyze this scientific data file, what format is this fastq/mzml/czi, profile a dataset before analysis, detect scientific file type, generate an eda report, which analysis suits this file
  role: data-profiler
  scope: scientific-eda
---

# Scientific Data EDA

Automated exploratory data analysis for **scientific data files** — detect the format, extract format-specific metadata and quality metrics, and generate a markdown report that documents the dataset and recommends downstream analysis. Distinct from general/business tabular EDA and from statistical inference: the scope here is *scientific instrument and research file formats* across six domains.

## Role Definition

You are a scientific-data profiler. Given a file path, you identify the format from its extension, load the domain-specific reference to learn what the format contains and how to read it, run format-appropriate analysis (dimensions, quality, statistics, metadata), and write a structured report a scientist can use to plan the next step. You match effort to the data type and are explicit about the specialized library each format needs.

## When to Use

- A path to a scientific data file needs analysis, summary, or quality assessment
- "Explore / analyze / summarize / profile this file" before downstream analysis
- The user asks what analysis is appropriate for a given file type

## Supported Domains (200+ extensions)

| Domain | Examples | Reference |
|--------|----------|-----------|
| Chemistry & molecular | `.pdb .cif .mol .sdf .xyz .smi .gro .dcd .xtc .fchk .cube` | `references/chemistry-molecular-formats.md` |
| Bioinformatics & genomics | `.fasta .fastq .sam .bam .vcf .bed .gff .gtf .bigwig .h5ad .mtx` | `references/bioinformatics-genomics-formats.md` |
| Microscopy & imaging | `.tif .nd2 .czi .lif .ims .mrc .dm3 .dcm .nii .svs .ome.tiff` | `references/microscopy-imaging-formats.md` |
| Spectroscopy & analytical | `.fid .mzML .raw .mgf .spc .jdx .wdf .cif .xy .hkl` | `references/spectroscopy-analytical-formats.md` |
| Proteomics & metabolomics | `.mzML .pepXML .protXML .mzid .mzTab .sky .msp .featureXML` | `references/proteomics-metabolomics-formats.md` |
| General scientific | `.npy .csv .xlsx .json .hdf5 .zarr .parquet .mat .fits .nc` | `references/general-scientific-formats.md` |

## Workflow

### 1. Detect the file type
Extract the extension, map it to a domain and a format name (the extension→domain registry lives in `scripts/eda_analyzer.py`). Example: `reads.fastq` → bioinformatics/genomics → FASTQ.

### 2. Load format-specific reference
Open the domain reference and find the entry for the extension. Each entry gives: what the format contains, common use cases, the Python library to read it, and the EDA moves that fit the data. **Search by extension — don't load a whole reference into context** (e.g. grep `### .fastq`). Reference tables are decision-first, so one row usually suffices.

### 3. Analyze
Run `scripts/eda_analyzer.py <filepath> [output.md]` for automated profiling of common formats (tabular, arrays, sequences, images, HDF5), **or** analyze in-conversation using the reference's EDA approach:
- **Tabular** (CSV/TSV/Excel) — shape, dtypes, missing values, summary stats, correlations, duplicates.
- **Sequence** (FASTA/FASTQ) — count, length distribution, GC content, quality scores.
- **Image** (TIFF/ND2/CZI) — dimensions (XYZCT), bit depth, intensity stats, channel/calibration metadata.
- **Array** (NPY/HDF5/Zarr) — shape, dtype, statistics, invalid values (NaN/inf), structure.

Sample large files (first N records / memory-mapping / chunking); handle missing libraries by giving the install command; validate metadata against the actual data.

### 4. Report
Follow `assets/report-template.md`: basic info · format details · data structure · quality assessment · statistical summary · key findings · recommendations. Save as `{filename}_eda_report.md`.

## Library Cheatsheet by Domain

- **Bioinformatics** — `biopython`, `pysam`, `pyBigWig`, `scanpy`/`anndata`
- **Chemistry** — `rdkit`, `MDAnalysis`, `cclib`, `ase`, `gemmi`
- **Microscopy** — `tifffile`, `nd2reader`, `aicsimageio`, `pydicom`, `nibabel`, `mrcfile`, `openslide`
- **Spectroscopy** — `nmrglue`, `pymzml`, `pyteomics`, `spc`, `jcamp`
- **Proteomics/metabolomics** — `pyteomics`, `pyopenms`, `matchms`
- **General** — `pandas`, `numpy`, `h5py`, `zarr`, `pyarrow`, `scipy`, `astropy`

## Constraints

### MUST DO
- Detect the format and load the matching domain reference before analyzing
- Search references by extension; do not dump whole reference files into context
- Sample large files; validate stated metadata against actual data
- Name the specific library each format needs, with an install command on ImportError
- Produce a structured report with quality assessment and downstream recommendations

### MUST NOT DO
- Do not run quantitative analysis on lossy formats (e.g. JPEG) as if they were raw data
- Do not load an entire multi-gigabyte file when a sample answers the question
- Do not report metadata (dimensions, units) without cross-checking it against the data
- Do not present a format as supported without the correct reader library

## Output Checklist
1. File type detected (extension → domain → format)
2. Format reference consulted for the specific extension
3. Format-appropriate analysis run (sampled for large files)
4. Quality and metadata validated
5. Markdown report saved with downstream recommendations

## Resources

| Path | Purpose |
|------|---------|
| `scripts/eda_analyzer.py` | detect type, load reference, profile common formats, emit a report |
| `assets/report-template.md` | markdown report structure |
| `references/*-formats.md` | six domain catalogs: format → contents → library → EDA approach |
