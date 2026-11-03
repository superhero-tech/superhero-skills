# Evidence and source consistency

- The document identifies actual pages, date, viewport sizes, states, and gaps.
- Every measured token/component claim points to a saved snapshot and element/property; visual observations point to a screenshot.
- Raw snapshots preserve font size, weight, line-height, tracking, alpha, gradients, and asymmetric borders/corners where relevant.
- Representative values in DESIGN.md match raw data; spot-check heading typography, primary control, surface, and one spacing/radius value when present.
- Component classifications and logo candidates have been visually reviewed; frequency alone does not determine semantic roles.
- A viewport screenshot and extraction describe the same viewport/theme/state. Full-page captures are identified as such.
- Unavailable mobile, interaction, or theme measurements are explicitly unverified. There are no invented minimum counts or missing states filled with conventions.
- Declared media queries and observed layout changes are distinguished; sampled widths are not described as discovered breakpoints.
- Temporary browser changes were restored, or an isolated fallback browser was closed.
- Run validate-evidence.py to check artifacts and token references. Correct data issues; do not treat a passing validator as proof of screenshot fidelity.
