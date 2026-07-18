#!/usr/bin/env python3
"""Scientific data EDA analyzer.

Detects a scientific data file's format from its extension, pulls the matching
entry from the domain reference catalog, runs format-appropriate profiling, and
writes a markdown EDA report.

Usage:
    python eda_analyzer.py <filepath> [output.md]

If no output path is given, the report is written next to the input file as
``<stem>_eda_report.md``.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

# extension (no dot) -> (domain, human-readable format name)
EXTENSION_REGISTRY: dict[str, tuple[str, str]] = {
    # chemistry / molecular
    "pdb": ("chemistry_molecular", "Protein Data Bank"),
    "cif": ("chemistry_molecular", "Crystallographic Information File"),
    "mol": ("chemistry_molecular", "MDL Molfile"),
    "mol2": ("chemistry_molecular", "Tripos Mol2"),
    "sdf": ("chemistry_molecular", "Structure Data File"),
    "xyz": ("chemistry_molecular", "XYZ Coordinates"),
    "smi": ("chemistry_molecular", "SMILES String"),
    "smiles": ("chemistry_molecular", "SMILES String"),
    "gro": ("chemistry_molecular", "GROMACS Coordinate File"),
    "fchk": ("chemistry_molecular", "Gaussian Formatted Checkpoint"),
    "cube": ("chemistry_molecular", "Gaussian Cube File"),
    "dcd": ("chemistry_molecular", "Binary Trajectory"),
    "xtc": ("chemistry_molecular", "Compressed Trajectory"),
    "trr": ("chemistry_molecular", "GROMACS Trajectory"),
    # bioinformatics / genomics
    "fasta": ("bioinformatics_genomics", "FASTA"),
    "fa": ("bioinformatics_genomics", "FASTA"),
    "fna": ("bioinformatics_genomics", "FASTA"),
    "fastq": ("bioinformatics_genomics", "FASTQ"),
    "fq": ("bioinformatics_genomics", "FASTQ"),
    "sam": ("bioinformatics_genomics", "Sequence Alignment/Map"),
    "bam": ("bioinformatics_genomics", "Binary Alignment/Map"),
    "bed": ("bioinformatics_genomics", "Browser Extensible Data"),
    "gff": ("bioinformatics_genomics", "General Feature Format"),
    "gff3": ("bioinformatics_genomics", "General Feature Format"),
    "gtf": ("bioinformatics_genomics", "Gene Transfer Format"),
    "vcf": ("bioinformatics_genomics", "Variant Call Format"),
    "bigwig": ("bioinformatics_genomics", "BigWig"),
    "bw": ("bioinformatics_genomics", "BigWig"),
    "mtx": ("bioinformatics_genomics", "Matrix Market (sparse)"),
    "h5ad": ("bioinformatics_genomics", "AnnData"),
    # microscopy / imaging
    "tif": ("microscopy_imaging", "TIFF"),
    "tiff": ("microscopy_imaging", "TIFF"),
    "nd2": ("microscopy_imaging", "Nikon NIS-Elements"),
    "lif": ("microscopy_imaging", "Leica Image Format"),
    "czi": ("microscopy_imaging", "Carl Zeiss Image"),
    "ims": ("microscopy_imaging", "Imaris"),
    "mrc": ("microscopy_imaging", "MRC (electron microscopy)"),
    "dm3": ("microscopy_imaging", "Gatan Digital Micrograph"),
    "dm4": ("microscopy_imaging", "Gatan Digital Micrograph"),
    "dcm": ("microscopy_imaging", "DICOM"),
    "nii": ("microscopy_imaging", "NIfTI"),
    "svs": ("microscopy_imaging", "Aperio ScanScope (whole slide)"),
    # spectroscopy / analytical
    "fid": ("spectroscopy_analytical", "NMR Free Induction Decay"),
    "jdx": ("spectroscopy_analytical", "JCAMP-DX"),
    "spc": ("spectroscopy_analytical", "Galactic SPC"),
    "wdf": ("spectroscopy_analytical", "Renishaw Raman"),
    "hkl": ("spectroscopy_analytical", "Reflection Data"),
    "mtz": ("spectroscopy_analytical", "MTZ (CCP4)"),
    "xy": ("spectroscopy_analytical", "Powder Diffraction XY"),
    # proteomics / metabolomics
    "mzml": ("proteomics_metabolomics", "mzML"),
    "mzxml": ("proteomics_metabolomics", "mzXML"),
    "mgf": ("proteomics_metabolomics", "Mascot Generic Format"),
    "pepxml": ("proteomics_metabolomics", "pepXML"),
    "protxml": ("proteomics_metabolomics", "protXML"),
    "mzid": ("proteomics_metabolomics", "mzIdentML"),
    "mztab": ("proteomics_metabolomics", "mzTab"),
    "msp": ("proteomics_metabolomics", "NIST MS spectral library"),
    "raw": ("proteomics_metabolomics", "Vendor raw MS"),
    # general scientific
    "npy": ("general_scientific", "NumPy Array"),
    "npz": ("general_scientific", "Compressed NumPy Archive"),
    "csv": ("general_scientific", "Comma-Separated Values"),
    "tsv": ("general_scientific", "Tab-Separated Values"),
    "xlsx": ("general_scientific", "Excel Spreadsheet"),
    "xls": ("general_scientific", "Excel Spreadsheet"),
    "json": ("general_scientific", "JSON"),
    "xml": ("general_scientific", "XML"),
    "hdf5": ("general_scientific", "HDF5"),
    "h5": ("general_scientific", "HDF5"),
    "zarr": ("general_scientific", "Zarr"),
    "parquet": ("general_scientific", "Apache Parquet"),
    "mat": ("general_scientific", "MATLAB Data"),
    "fits": ("general_scientific", "FITS (astronomy)"),
    "nc": ("general_scientific", "NetCDF"),
}

DOMAIN_REFERENCE: dict[str, str] = {
    "chemistry_molecular": "chemistry-molecular-formats.md",
    "bioinformatics_genomics": "bioinformatics-genomics-formats.md",
    "microscopy_imaging": "microscopy-imaging-formats.md",
    "spectroscopy_analytical": "spectroscopy-analytical-formats.md",
    "proteomics_metabolomics": "proteomics-metabolomics-formats.md",
    "general_scientific": "general-scientific-formats.md",
}

DOWNSTREAM_HINTS: dict[str, list[str]] = {
    "general_scientific": [
        "Distribution and outlier analysis",
        "Missing-value strategy",
        "Correlation / dimensionality reduction (PCA, UMAP)",
    ],
    "bioinformatics_genomics": [
        "Read QC and filtering",
        "GC-content and duplication analysis",
        "Alignment / variant-calling / differential-expression",
    ],
    "microscopy_imaging": [
        "Background correction and normalization",
        "Segmentation / object detection",
        "Intensity quantification and colocalization",
    ],
}


def human_bytes(size: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def detect_file_type(path: Path) -> tuple[str, str, str]:
    """Return (extension, domain, format_name); domain is 'unknown' if unmapped."""
    ext = path.suffix.lower().lstrip(".")
    domain, name = EXTENSION_REGISTRY.get(ext, ("unknown", "Unknown Format"))
    return ext, domain, name


def basic_info(path: Path) -> dict:
    stat = path.stat()
    return {
        "filename": path.name,
        "path": str(path.resolve()),
        "size_bytes": stat.st_size,
        "size_human": human_bytes(stat.st_size),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
    }


def load_reference_section(domain: str, ext: str) -> dict | None:
    """Extract the reference entry for ``ext`` from the domain catalog, if present."""
    ref_name = DOMAIN_REFERENCE.get(domain)
    if not ref_name:
        return None
    ref_path = Path(__file__).resolve().parent.parent / "references" / ref_name
    if not ref_path.exists():
        return None
    try:
        text = ref_path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - defensive
        print(f"Could not read reference {ref_path}: {exc}", file=sys.stderr)
        return None
    # entries may be table rows ("| .fastq |") or headings ("### .fastq"); grab a
    # line/section mentioning the extension so the report links the right context.
    heading = re.search(rf"###\s+\.?{re.escape(ext)}\b.*?(?=\n###|\Z)", text,
                        re.IGNORECASE | re.DOTALL)
    if heading:
        return {"reference_file": ref_name, "section": heading.group(0).strip()}
    row = re.search(rf"^.*\|\s*`?\.?{re.escape(ext)}`?\s*\|.*$", text,
                    re.IGNORECASE | re.MULTILINE)
    if row:
        return {"reference_file": ref_name, "section": row.group(0).strip()}
    return {"reference_file": ref_name, "section": None}


def analyze_general(path: Path, ext: str) -> dict:
    try:
        if ext == "npy":
            import numpy as np
            arr = np.load(path, mmap_mode="r")
            numeric = np.issubdtype(arr.dtype, np.number)
            return {
                "shape": list(arr.shape), "dtype": str(arr.dtype), "ndim": arr.ndim,
                "stats": {
                    "min": float(np.min(arr)) if numeric else None,
                    "max": float(np.max(arr)) if numeric else None,
                    "mean": float(np.mean(arr)) if numeric else None,
                    "std": float(np.std(arr)) if numeric else None,
                },
            }
        if ext == "npz":
            import numpy as np
            with np.load(path) as data:
                return {"arrays": list(data.files),
                        "shapes": {k: list(data[k].shape) for k in data.files}}
        if ext in {"csv", "tsv"}:
            import pandas as pd
            sep = "\t" if ext == "tsv" else ","
            df = pd.read_csv(path, sep=sep, nrows=10_000)
            numeric = df.select_dtypes("number")
            return {
                "shape": list(df.shape),
                "columns": list(df.columns),
                "dtypes": {c: str(t) for c, t in df.dtypes.items()},
                "missing": df.isnull().sum().to_dict(),
                "summary": numeric.describe().to_dict() if not numeric.empty else {},
                "note": "profiled first 10,000 rows",
            }
        if ext == "json":
            data = json.loads(path.read_text(encoding="utf-8"))
            return {"type": type(data).__name__,
                    "keys": list(data)[:50] if isinstance(data, dict) else None,
                    "length": len(data) if isinstance(data, (list, dict)) else None}
        if ext in {"h5", "hdf5"}:
            import h5py

            def walk(group, prefix=""):
                out = {}
                for key in group:
                    node = group[key]
                    p = f"{prefix}/{key}"
                    if isinstance(node, h5py.Dataset):
                        out[p] = {"type": "dataset", "shape": list(node.shape),
                                  "dtype": str(node.dtype)}
                    else:
                        out[p] = {"type": "group"}
                        out.update(walk(node, p))
                return out

            with h5py.File(path, "r") as f:
                return {"structure": walk(f), "attributes": dict(f.attrs)}
    except ImportError as exc:
        return {"error": f"required library not installed: {exc}"}
    except Exception as exc:  # noqa: BLE001 - report any read failure, don't crash
        return {"error": f"analysis error: {exc}"}
    return {}


def analyze_bioinformatics(path: Path, ext: str) -> dict:
    try:
        from Bio import SeqIO
    except ImportError as exc:
        return {"error": f"install biopython to analyze sequences: {exc}"}
    try:
        if ext in {"fasta", "fa", "fna"}:
            seqs = list(SeqIO.parse(str(path), "fasta"))
            lengths = [len(s) for s in seqs]
            return {
                "sequence_count": len(seqs),
                "total_length": sum(lengths),
                "mean_length": (sum(lengths) / len(lengths)) if lengths else 0,
                "min_length": min(lengths, default=0),
                "max_length": max(lengths, default=0),
                "first_ids": [s.id for s in seqs[:10]],
            }
        if ext in {"fastq", "fq"}:
            seqs, lengths, quals = [], [], []
            for i, rec in enumerate(SeqIO.parse(str(path), "fastq")):
                lengths.append(len(rec))
                phred = rec.letter_annotations["phred_quality"]
                quals.append(sum(phred) / len(phred) if phred else 0)
                if i >= 9_999:  # sample first 10k reads
                    break
                seqs.append(rec)
            return {
                "reads_sampled": len(lengths),
                "mean_length": (sum(lengths) / len(lengths)) if lengths else 0,
                "mean_quality": (sum(quals) / len(quals)) if quals else 0,
                "min_length": min(lengths, default=0),
                "max_length": max(lengths, default=0),
                "note": "profiled first 10,000 reads",
            }
    except Exception as exc:  # noqa: BLE001
        return {"error": f"analysis error: {exc}"}
    return {}


def analyze_imaging(path: Path, ext: str) -> dict:
    try:
        from PIL import Image
        import numpy as np
    except ImportError as exc:
        return {"error": f"install pillow to analyze images: {exc}"}
    try:
        if ext in {"tif", "tiff", "png", "jpg", "jpeg"}:
            img = Image.open(path)
            arr = np.asarray(img)
            result = {
                "size": list(img.size), "mode": img.mode, "format": img.format,
                "shape": list(arr.shape), "dtype": str(arr.dtype),
                "value_range": [int(arr.min()), int(arr.max())],
                "mean_intensity": float(arr.mean()),
            }
            if ext in {"tif", "tiff"}:
                pages = 0
                try:
                    while True:
                        img.seek(pages)
                        pages += 1
                except EOFError:
                    result["page_count"] = pages
            return result
    except Exception as exc:  # noqa: BLE001
        return {"error": f"analysis error: {exc}"}
    return {}


ANALYZERS = {
    "general_scientific": analyze_general,
    "bioinformatics_genomics": analyze_bioinformatics,
    "microscopy_imaging": analyze_imaging,
}


def analyze_file(path: Path) -> dict:
    ext, domain, name = detect_file_type(path)
    analyzer = ANALYZERS.get(domain)
    return {
        "basic_info": basic_info(path),
        "file_type": {"extension": ext, "domain": domain, "format": name},
        "reference": load_reference_section(domain, ext),
        "data_analysis": analyzer(path, ext) if analyzer else {},
    }


def render_report(analysis: dict) -> str:
    b, ft = analysis["basic_info"], analysis["file_type"]
    lines = [
        f"# Scientific Data EDA Report: {b['filename']}",
        f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "---\n",
        "## Basic Information\n",
        f"- **Filename:** `{b['filename']}`",
        f"- **Path:** `{b['path']}`",
        f"- **Size:** {b['size_human']} ({b['size_bytes']:,} bytes)",
        f"- **Modified:** {b['modified']}",
        f"- **Extension:** `.{ft['extension']}`\n",
        "## File Type\n",
        f"- **Domain:** {ft['domain'].replace('_', ' ').title()}",
        f"- **Format:** {ft['format']}\n",
    ]
    ref = analysis.get("reference")
    if ref and ref.get("section"):
        lines += ["## Format Reference\n", ref["section"],
                  f"\n*Reference: {ref['reference_file']}*\n"]
    data = analysis.get("data_analysis") or {}
    if data:
        lines.append("## Data Analysis\n")
        if "error" in data:
            lines.append(f"> **Note:** {data['error']}\n")
        else:
            lines += ["```json", json.dumps(data, indent=2, default=str), "```\n"]
    hints = DOWNSTREAM_HINTS.get(ft["domain"])
    if hints:
        lines.append("## Recommended Next Steps\n")
        lines += [f"- {h}" for h in hints]
        lines.append("")
    lines += ["---", "*Generated by the data-analysis-scientific-eda skill.*"]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python eda_analyzer.py <filepath> [output.md]")
        return 1
    src = Path(argv[1])
    if not src.exists():
        print(f"Error: file not found: {src}")
        return 1
    out = Path(argv[2]) if len(argv) > 2 else src.with_name(f"{src.stem}_eda_report.md")
    print(f"Analyzing: {src}")
    report = render_report(analyze_file(src))
    out.write_text(report, encoding="utf-8")
    print(f"Report saved to: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
