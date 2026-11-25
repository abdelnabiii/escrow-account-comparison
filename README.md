# Escrow account bank comparison

Decision tool comparing 15 Egyptian banks for the project escrow / controlled collection account
required by a revenue-share development contract (commercial plot, L'avenir, Mostakbal City).

- `index.html` is the whole tool: self-contained, runs offline, data embedded as a JSON object at the top. English and Arabic (RTL).
- `src/` holds the inputs and the build script: `python3 src/build.py` regenerates `index.html` from
  `src/template.html`, `src/static.json` (contract, structures, criteria), `src/manual.json` (flags and rating adjustments)
  and `src/research/*.json` (researched data points with status, source URL and access date).

Research date: 2026-11-25. Every data point is Verified, Bank to confirm or Unknown; nothing is estimated.
Edits made in the page (bank offers) are stored in the browser only; use Export JSON to keep them.
