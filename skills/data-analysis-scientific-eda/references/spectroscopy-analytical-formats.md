# Spectroscopy & Analytical Formats

NMR, mass spectrometry, IR/Raman, UV-Vis, X-ray/diffraction, electron spectroscopy, chromatography, and thermal/elemental/electrochemistry. Columns: **ext · format · read with · EDA focus**.

## NMR

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.fid` | free induction decay (time domain) | `nmrglue` (bruker/varian), `nmrstarlib` | signal decay, sampling rate/acquisition time, points, SNR, baseline drift, apodization choice |
| `.ft`/`.ft1`/`.ft2` | frequency-domain spectrum | `nmrglue` | peak picking/integration, chemical-shift range, baseline/phase correction, resolution, artifacts |
| `.1r`/`.2rr` | Bruker processed | `nmrglue` | processing params, window function, zero-filling, linear prediction |
| `.dx`/`.jdx`/`.jcamp` | JCAMP-DX | `jcamp`, `nmrglue` | format compliance, metadata, peak table, integration, compound ID |

## Mass Spectrometry

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.mzML` | MS markup language | `pymzml`, `pyteomics.mzml`, `pyopenms` | scan count/MS levels, RT range + TIC, m/z range/resolution, precursor selection, QC metrics |
| `.mzXML`/`.mzData` | legacy MS XML | `pyteomics`, `pymzml` | as mzML + version/conversion validation |
| `.raw` | vendor raw (Thermo/etc.) | `pymsfilereader`, `ThermoRawFileParser` | method params, instrument performance, calibration, scan functions, MS/MS quality |
| `.d` | Agilent data directory | community parsers, ChemStation | directory validation, method params, calibration curves, sequence metadata |
| `.wiff` | AB SCIEX | vendor SDK, convert to mzML | experiment type, scan properties, quantitation |
| `.mgf` | Mascot Generic Format | `pyteomics.mgf`, `pyopenms` | spectrum count, charge states, precursor m/z, fragment count, mass accuracy |
| `.ms1`/`.ms2` | simple MS text | `pyteomics.ms1`/`ms2` | scan count by level, RT series, charge states, m/z coverage |

## IR / Raman

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.spc` | Galactic SPC | `spc`, `specio` | wavenumber/wavelength range, point density, multi-spectrum, baseline, peaks, abs/trans mode |
| `.spa` | Thermo Nicolet FTIR | custom parsers, convert | interferogram vs spectrum, background validation, atmospheric compensation, resolution |
| `.0` | Bruker OPUS | `brukeropusreader`, `specio` | block types (AB/ScSm), sample/reference spectra, instrument params, optics |
| `.wdf` | Renishaw Raman | `renishawWiRE` | spectral vs mapping, laser wavelength, exposure/accumulation, spatial coords, baseline/cosmic-ray |
| `.dpt`/`.txt` | XY data table | `pandas` | X-axis type (wavelength/wavenumber/Raman shift), Y units, point spacing, header |

## UV-Vis

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.asd`/`.asc` | ASD FieldSpec | `spectral.io.asd` | UV–NIR range, reference/dark correction, integration time, reflectance vs radiance |
| `.sp` | Perkin Elmer | custom parsers | scan params, baseline, multi-wavelength, sample/reference |
| `.csv` | UV-Vis export | `pandas` | λmax, Beer's-law compliance, baseline offset, path-length/concentration |

## X-ray & Diffraction

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.cif` | crystallographic info | `gemmi`, `PyCifRW`, `pymatgen` | crystal system/space group, unit cell, atomic positions/occupancy, thermal params, R-factors |
| `.hkl` | reflection data | custom, CCP4 | resolution range, completeness by shell, I/σ, systematic absences, twinning, Wilson plot |
| `.mtz` | MTZ (CCP4) | `gemmi`, `cctbx` | column types, resolution limits, Rwork/Rfree, phase probability, map coefficients |
| `.xy`/`.xye` | powder diffraction | `pandas`, `pymatgen` | 2-theta range, peak positions/intensities, background, peak width (size/strain), phase ID |
| `.raw` (XRD) | vendor XRD | vendor parsers | scan params (step/time), alignment, beam setup, detector config |
| `.gsa`/`.gsas` | GSAS | GSAS-II | histogram data, instrument params, phases, profile functions |

## Electron Spectroscopy & Other

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.vms` | VG Scienta (XPS/UPS/ARPES) | custom, `specio` | binding-energy calibration, pass energy/resolution, line ID, background subtraction, Fermi edge |
| `.spe` | WinSpec CCD | `spe2py`, `spe_loader` | CCD frames, wavelength calibration, dark subtraction, cosmic rays, readout noise |
| `.pxt` | PTI fluorescence | custom parsers | excitation/emission spectra, quantum yield, time-resolved, correction factors |
| `.chrom`/`.ch`/`.arw`/`.lcd` | chromatography (HPLC/GC) | vendor parsers, `pandas` | RT range, peak detection/integration, baseline drift, resolution, S/N, tailing |
| `.dta` | DSC/TGA thermal | custom, `pandas` | transition temperatures, enthalpy, mass-loss steps, heating-rate effects, baseline |
| `.run` | ICP-MS/OES | vendor tools | element quantitation, internal standard, spike recovery, isotope ratios, LOD/LOQ |
| `.exp` | electrochemistry | `galvani`, vendor parsers | redox peaks, peak potential/current, scan-rate effects, kinetics, capacitance |

**Notes:** Many analytical formats are best converted to an open standard first (vendor MS → mzML; FTIR → JCAMP/SPC). NMR needs correct vendor dialect in `nmrglue`. Report the axis type/units explicitly (wavenumber vs wavelength vs Raman shift vs 2-theta vs binding energy).
