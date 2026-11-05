# Clean-clone verification

**Date:** 2026-11-06  
**Source:** public repository https://github.com/Sektorial12/bidroom at `HEAD` (single-commit history), and local `HEAD`

Commands:

```text
git clone https://github.com/Sektorial12/bidroom.git <temporary-directory>
cd <temporary-directory>
python -m unittest discover -s tools/tests -v
python tools/bidcheck.py verification/decision.example.json
```

Observed result:

```text
Ran 49 tests
OK

VALID: Northstar Citizen Services Portal | bid_with_partner | 68/100
```

The validator and example are reproducible from a clean clone of the public repository. The example matches the final three-room run scores: base **50/100**, partner **68/100**. The single-room prototype used base 46/100 and is kept as historical evidence. The three-room Switch workflow still requires the manual setup in `docs/setup.md`; it is not recreated by the clone.
