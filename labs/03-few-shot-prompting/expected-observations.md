# Lab 03 — Expected Observations

Judge by characteristics; responses vary.

## Zero-shot — typical weakness

- May label the clicked-link case as **software** (pop-ups) rather than **security** (phishing).

## Few-shot — expected characteristics

- Classifies `few-shot-boundary-01` as **security**, citing the phishing/malware signal.
- Applies the demonstrated pattern to a request that is not identical to any example.
- Does not copy an example's wording verbatim.

## Teaching point

Examples must be accurate and internally consistent. An example that contradicts a written rule
will teach the model the wrong behavior — the improved prompt keeps examples aligned with the
category definitions.
