# Chemistry & Molecular Formats

Structure files, computational-chemistry outputs, MD trajectories/topologies, and chemical databases. Columns: **ext · format · read with · EDA focus**.

## Structures

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.pdb` | Protein Data Bank | `Biopython Bio.PDB`, `MDAnalysis`, `ProDy` | structure validation (bonds/angles/clashes), secondary structure, B-factors, missing residues, Ramachandran |
| `.cif`/`.mmcif` | Crystallographic Info File | `gemmi`, `PyCifRW`, `Biopython MMCIFParser` | completeness, resolution/quality, unit cell, symmetry, ADPs, R-factors |
| `.mol` | MDL Molfile | `RDKit`, `Open Babel` | MW/logP/TPSA, functional groups, rings, stereochemistry, valence/charge |
| `.mol2` | Tripos Mol2 | `RDKit`, `Open Babel`, `MDAnalysis` | atom-type distribution, partial charges, bond types, substructures, conformers |
| `.sdf` | Structure Data File (multi) | `RDKit SDMolSupplier`, `PandasTools` | dataset size/diversity, property distributions, Tanimoto similarity, scaffolds |
| `.xyz` | Cartesian coordinates | `ASE`, `Open Babel`, `cclib` | geometry (bonds/angles/dihedrals), center of mass, moment of inertia, symmetry |
| `.smi`/`.smiles` | SMILES line notation | `RDKit MolFromSmiles`, `Open Babel` | syntax validation, descriptors, fingerprints, substructure search, tautomers/stereoisomers |
| `.pdbqt` | AutoDock PDBQT | `Meeko`, `Open Babel` | charge distribution, rotatable bonds, atom types, H placement, torsions |
| `.mae` | Schrödinger Maestro | `schrodinger.structure` | property extraction, conformers, docking scores, ligand efficiency |
| `.inchi` | InChI identifier | `RDKit MolFromInchi`, `Open Babel` | validation, layer analysis, stereochemistry, InChIKey, round-trip |
| `.cml`/`.cdx`/`.rxn`/`.rdf` | chemical markup / drawings / reactions | `RDKit`, `Open Babel`, `lxml` | structure extraction, reaction balancing, atom mapping, yield/condition stats |

## Computational Chemistry Output

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.log`/`.out` | Gaussian / QM output | `cclib`, `ASE` | convergence, energy profile, vibrational frequencies, orbital energies, Mulliken/NBO, thermochemistry |
| `.fchk` | Gaussian checkpoint | `cclib` | wavefunction quality, basis set, gradient/Hessian, natural orbitals |
| `.wfn`/`.wfx` | wavefunction | `Multiwfn`, `Horton` | orbital populations, electron density, QTAIM critical points, bonding |
| `.cube` | Gaussian cube (volumetric) | `cclib`, `ase.io` | grid dims/spacing, value distribution, isosurface values, volume integration |

## MD Trajectories & Topologies

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.dcd` | CHARMM/NAMD trajectory | `MDAnalysis`, `MDTraj` | RMSD/RMSF, frame count, coordinate drift, PBC handling, time step |
| `.xtc` | GROMACS compressed traj | `MDAnalysis`, `MDTraj` | compression/precision, RMSD over time, stability, sampling frequency |
| `.trr` | GROMACS full traj | `MDAnalysis`, `MDTraj` | full dynamics + velocities/forces, energy conservation, T/P validation |
| `.nc`/`.netcdf` | Amber NetCDF traj | `MDAnalysis`, `PyTraj`, `netCDF4` | metadata, trajectory stats, replica exchange, time series |
| `.gro` | GROMACS coordinates | `MDAnalysis`, `MDTraj` | system composition, box dims, position/velocity distribution, density, solvation |
| `.top`/`.psf`/`.prmtop` | topology | `ParmEd`, `MDAnalysis`, `PyTraj` | force-field parameter validity, composition, bond/angle/dihedral dist, charge neutrality |
| `.inpcrd`/`.rst7` | Amber coordinates/restart | `ParmEd`, `PyTraj` | coordinate validity, box vectors, velocity dist (restart), minimization status |

**Notes:** Trajectory files require a matching topology to interpret. Many QM/vendor outputs are best handled by `cclib` (universal parser). See `spectroscopy-analytical-formats.md` for NMR/MS/crystallography analytical data.
