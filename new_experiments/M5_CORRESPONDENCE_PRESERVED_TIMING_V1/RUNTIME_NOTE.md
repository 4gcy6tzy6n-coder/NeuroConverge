# Runtime note: NumPy/Apple Accelerate warnings

The successful frozen run used Python 3.9.6 and NumPy 2.0.2 linked to Apple's Accelerate BLAS/LAPACK on arm64 macOS. NumPy emitted `divide by zero`, `overflow`, and `invalid value` warnings for several matrix multiplications.

The warnings did not correspond to non-finite operands or results in the audited case:

- reproduced seed-51000 inputs were all finite, ranging from `−0.81904` to `1.83180`;
- the warned RBF matrix product was entirely finite, ranging from `0.000111` to `5.69628`;
- recomputing that product with `numpy.einsum` gave maximum absolute difference `0.0`;
- all 300 recorded seed × regime × arm nMAE values were finite and inside the normalized `[0, 1]` range;
- the post-run verifier recomputed all 150 paired correspondence effects and all reported arm means exactly.

The raw warnings are therefore retained as an environment-specific audit note rather than suppressed or used to alter the frozen implementation after outcome inspection.
