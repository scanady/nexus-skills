# Microscopy & Imaging Formats

Light and electron microscopy, medical imaging, whole-slide imaging, and scientific image formats. Columns: **ext · format · read with · EDA focus**.

## Microscopy (vendor & standard)

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.tif`/`.tiff` | TIFF (multi-page) | `tifffile`, `scikit-image`, `AICSImageIO` | dims + bit depth, z-stack/pages, OME metadata, per-channel intensity, pixel calibration, dynamic range |
| `.ome.tif`/`.ome.tiff` | OME-TIFF | `tifffile`, `AICSImageIO`, `python-bioformats` | OME-XML validation, physical dims, channel wavelengths, plane positions (Z/C/T), instrument metadata |
| `.nd2` | Nikon NIS-Elements | `nd2reader`, `pims`, `AICSImageIO` | XYZCT structure, channels, timelapse frames, z-spacing, stage positions, laser/acquisition metadata |
| `.lif` | Leica | `readlif`, `AICSImageIO` | multi-experiment/series, per-experiment metadata, channels/timepoints, objective/detector |
| `.czi` | Zeiss | `czifile`, `pylibCZIrw`, `AICSImageIO` | scenes/positions, mosaic tiles, channel wavelengths, scaling, ROIs |
| `.oib`/`.oif` | Olympus FluoView | `AICSImageIO`, `python-bioformats` | directory validation, channels, scan params, PMT/filter settings |
| `.ims` | Imaris (HDF5) | `h5py`, `imaris_ims_file_reader` | resolution levels, timepoints, channels, hierarchy, chunking |
| `.lsm`/`.stk`/`.dv` | Zeiss LSM / MetaMorph / DeltaVision | `tifffile`, `AICSImageIO`, `python-bioformats` | TIFF-based metadata, scan/laser settings, stage positions, deconvolution status |

## Electron Microscopy

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.mrc` | MRC (cryo-EM/tomography) | `mrcfile`, `EMAN2` | volume dims, voxel size/units, origin/map stats, symmetry, density stats, header consistency |
| `.dm3`/`.dm4` | Gatan Digital Micrograph | `hyperspy`, `ncempy` | microscope params, EDS data, diffraction patterns, calibration, tag structure |
| `.eer` | electron-event representation | `mrcfile`, vendor tools | event counting, frame rate/dose, motion correction, gain reference |
| `.ser` | FEI/TFS TIA series | `hyperspy`, `ncempy` | series structure, calibration, acquisition metadata |

## Medical Imaging

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.dcm` | DICOM | `pydicom`, `SimpleITK`, `nibabel` | patient metadata (**check anonymization**), modality, series/study, slice spacing, Hounsfield units (CT), orientation |
| `.nii`/`.nii.gz` | NIfTI | `nibabel`, `nilearn`, `SimpleITK` | volume dims/voxel size, affine matrix, fMRI time series, intensity dist, orientation |
| `.mnc` | MINC | `pyminc`, `nibabel` | as NIfTI + NetCDF structure, dimension ordering |
| `.nrrd`/`.mha`/`.mhd` | NRRD / MetaImage (ITK) | `pynrrd`, `SimpleITK`, `itk` | header fields, encoding, spacing, orientation matrix, header–data pairing (MHD) |
| `.hdr`/`.img` | Analyze (legacy) | `nibabel` | header–image pairing, byte order; convert to NIfTI |

## Whole-Slide Imaging (pathology)

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.svs` | Aperio ScanScope | `openslide-python`, `tiffslide` | pyramid structure, MPP calibration, label/macro images, thumbnail |
| `.ndpi` | Hamamatsu NanoZoomer | `openslide-python` | multi-resolution pyramid, objective, scan area/magnification, focal planes |
| `.vsi`/`.scn` | Olympus VSI / Leica SCN | `openslide-python`, `AICSImageIO` | pyramid levels, tile structure/overlap, macro/label, tissue detection |

## Standard & Cloud-Native Image Formats

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.png`/`.bmp`/`.gif` | lossless raster | `Pillow`, `scikit-image`, `imageio` | bit depth, color mode, metadata, transparency, histogram; GIF frame count/timing |
| `.jpg`/`.jpeg` | JPEG (lossy) | `Pillow`, `scikit-image` | compression artifacts, quality factor, EXIF — **not for quantitative analysis** |
| `.svg`/`.eps`/`.pdf` | vector / document | `svgpathtools`, `cairosvg`, `PyMuPDF`, `pdf2image` | element structure, viewbox/dims, embedded fonts, image extraction, DPI |
| `.ome.zarr` | OME-ZARR (NGFF) | `ome-zarr-py`, `zarr` | multiscale levels, OME-NGFF compliance, coordinate transforms, labels, chunk access |
| `.hdf5`/`.klb` | large-imaging containers | `h5py`, `pyklb` | dataset hierarchy, multi-resolution pyramid, chunk/compression, memory-mapped access |
| `.raw`/`.bin` | unformatted pixels | `numpy.fromfile`, `struct` | dims (external info needed), byte order/dtype, header detection, value range, noise |
| `.roi`/`.zip` (ROI) | ImageJ ROI(s) | `read-roi`, `roifile` | ROI type/coordinates, area/perimeter, set count, overlaps, Z/T position |

**Notes:** `AICSImageIO` and Bio-Formats read most vendor microscopy formats behind one API. Report image dimensions in explicit XYZCT order and always cross-check stated pixel size against metadata. Lossy formats (JPEG) are for visualization, not measurement.
