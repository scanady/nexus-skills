# Proteomics & Metabolomics Formats

Mass-spec proteomics, metabolomics, lipidomics, and multi-omics — raw data, identifications, quantification, and feature tables. Columns: **ext · format · read with · EDA focus**.

## Raw & Standard MS

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.mzML` | MS markup language | `pymzml`, `pyteomics.mzml`, `pyopenms` | scan count/MS levels, TIC/BPC, m/z coverage/resolution, RT range, precursor patterns, QC (lock mass/standards) |
| `.mzXML` | legacy MS XML | `pyteomics.mzxml`, `pymzml` | as mzML + version/conversion validation |
| `.raw` (Thermo) | Orbitrap/Q Exactive raw | `pymsfilereader`, `ThermoRawFileParser` | MS1/MS2 rates, AGC target/fill times, resolution, isolation windows, SPS ions (TMT), contamination |
| `.d` (Agilent) | data directory | community parsers → mzML | method consistency, calibration, sequence run, RT stability |
| `.wiff` | SCIEX (QTRAP/TripleTOF) | vendor tools → mzML | MRM transition performance, dwell/cycle time, peak integration |
| `.cdf`/`.netCDF` | ANDI-MS (GC/LC-MS) | `netCDF4`, `pyopenms` | TIC/EIC, cross-sample peak detection, retention index, library-match prep |

## Peptide/Protein Identification

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.mzIdentML`/`.mzid` | PSI identification | `pyteomics.mzid`, `pyopenms` | PSM count/score dist, FDR filtering, modifications, missed cleavages, protein inference, decoys, rank-1 vs lower |
| `.pepXML`/`.pep.xml` | TPP peptide | `pyteomics.pepxml` | score distributions (XCorr/expect), charge states, modification frequencies, PeptideProphet probs, spectral counts |
| `.protXML` | TPP protein inference | `pyteomics.protxml` | protein groups, parsimony, ProteinProphet probs, coverage, unique vs shared peptides |
| `.msf`/`.pdResult` | Proteome Discoverer | `sqlite3`, export to TSV | schema exploration, peptide/protein tables, score thresholds, quantification, confidence |
| `.pride.xml` | PRIDE deposition | `pyteomics.pride` | experiment metadata, identification completeness, spectra cross-links, protocol |
| `.idXML` | OpenMS identifications | `pyopenms` | identification rate, score dist, match quality, FDR, annotation transfer |

## Quantification (targeted & feature-level)

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.sky`/`.sky.zip` | Skyline (SRM/MRM/PRM) | Skyline API, export CSV, `zipfile` | transition validation, peak quality, interference, RT consistency, calibration curve, replicate correlation, LOD/LOQ |
| `.featureXML` | OpenMS features | `pyopenms` | detection params, per-feature quality, isotope fitting, charge, FWHM/asymmetry |
| `.consensusXML` | OpenMS consensus | `pyopenms` | correspondence quality, RT alignment, missing-value patterns, normalization needs |
| `.mzTab`/`.mzTab-M` | PSI tabular summary | `pyteomics.mztab`, `pandas` | completeness, metadata sections, quantification method, confidence, DB references (HMDB/KEGG) |
| `.tsv`/`.csv` | MaxQuant/PD/Skyline tables | `pandas` | ID counts, quant value distributions, missing patterns, LFQ/isobaric ratios, CV, batch effects |

## Metabolomics & Spectral Libraries

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.mgf` | MS/MS peak lists | `matchms`, `pyteomics.mgf` | spectrum QC, precursor purity, fragment m/z accuracy, neutral losses |
| `.msp` | NIST spectral library | `matchms`, custom | library coverage, metadata (InChI/SMILES), spectral quality, collision-energy standardization |
| `.nmrML` | NMR metabolomics | `nmrml2isa`, custom | spectral quality, binning consistency, reference validation, pH/temperature, ID confidence |
| `.txt` | feature tables (MZmine/XCMS/MS-DIAL) | `pandas` | feature count/quality, missing-value imputation, normalization, batch correction, PCA/clustering QC, fold change |
| `.json` | GNPS / MetaboAnalyst | `json`, `pandas` | annotation coverage, molecular-networking stats, adduct/in-source linkage, ID confidence |

## Lipidomics & Structures

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.lcb` | LipidCreator batch | export CSV | transition coverage per class, RT prediction, collision energy, class fragmentation |
| `.csv` (LipidSearch) | lipid IDs | `pandas` | class distribution, ID grade/confidence, fatty-acid composition, chain/double-bond patterns, IS normalization |
| `.sdf`/`.mol` (metabolites) | structures | `RDKit` | structure validation, logP/MW/TPSA, formula consistency, tautomers, RT-prediction features |

## Omics Storage

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.h5`/`.hdf5` | omics container | `h5py`, `anndata` | organization, chunking/compression, metadata, sample/feature annotations |
| `.parquet` | columnar tables | `pandas`, `pyarrow` | compression, column stats, partitions, schema, fast filtering |
| `.Rdata`/`.rds` | R objects (xcms/MSnbase) | `pyreadr`, `rpy2` | object structure, data extraction, method params, conversion |
| `.pkl` | pickled models/data | `pickle`, `joblib` | object type/structure, model params, shapes; only unpickle trusted sources |

**Notes:** Convert vendor raw to mzML early for cross-tool analysis. `pyteomics` covers most identification/quant XML/tabular formats; `pyopenms` covers the OpenMS ecosystem; `matchms` covers spectral-library matching. Always report FDR and how missing values were handled.
