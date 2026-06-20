# Find the CIRCT Version Closest to an LLVM Release

## Goal

Find the CIRCT version that uses an LLVM **release** version (e.g., 18.1.0, 19.1.0) rather than a development snapshot. This is the version to target for Fedora packaging.

## Steps

1. Determine the target LLVM release version (e.g., 18.1.0).
2. Search for all CIRCT commits that bump the LLVM submodule.
   - use the keyword `bump llvm` and other possible ones
   - use the LLVM release date as a hint to narrow down the commits
3. From the relevant CIRCT commits, extract the LLVM submodule commit hash.
4. Verify the LLVM commit has a tag matching a release version (e.g., `llvmorg-18.1.0`).
5. Report commit hash, version, date, tags, commit messages of :
   - all close CIRCT releases
   - LLVM used by these close CIRCT releases
   - all close CIRCT commits that bump LLVM
   - LLVM used by them

Report for both:
   - **Exact version**: search for the specific release (e.g., `18.1.0`)
   - **Major version range**: search for all LLVM versions within the same major release (e.g., `18.0.0` to `19.0.0` exclusive) to find any CIRCT commit tracking that major line

Never clone or shallow clone new copies of circt or llvm repos. they are huge.
update local clones if you have to.

## Data Sources

- **GitHub**: Prefered for the latest information.
  - `https://github.com/llvm/circt`
  - `https://github.com/llvm/llvm-project`
- **Local clones** (if available and up to date):
  - `/mnt/zpool-febdash/src/circt`
  - `/mnt/zpool-febdash/src/llvm-project`
