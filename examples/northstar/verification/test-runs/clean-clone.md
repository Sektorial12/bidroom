# Clean-clone verification

**Date:** 2026-11-06  
**Source:** public repository https://github.com/Sektorial12/bidroom at `HEAD`, and local `HEAD`

Commands:

```text
git clone https://github.com/Sektorial12/bidroom.git <temporary-directory>
cd <temporary-directory>
python -m unittest discover -s tests -v
python -m unittest discover -s tools/tests -v
python tools/bidroom.py check --project examples/northstar
python tools/bidroom.py validate --policy examples/northstar/policy.json examples/northstar/verification/decision.example.json
python tools/bidcheck.py examples/northstar/verification/decision.example.json
```

Observed result:

```text
Ran 11 tests
OK
Ran 49 tests
OK
PROJECT OK: Northstar Citizen Services Portal | northstar-bid-policy 1.0.0 | 6 gates | 4 criteria
VALID: Northstar Citizen Services Portal | bid_with_partner | 68/100
VALID: Northstar Citizen Services Portal | bid_with_partner | 68/100
```

The generic engine, the demo conformance suite, the project manifest, and the example are reproducible from a clean clone of the public repository. The example matches the final three-room run scores: base **50/100**, partner **68/100**. The single-room prototype used base 46/100 and is kept as historical evidence. The three-room Switch workflow still requires the manual setup in `examples/northstar/docs/setup.md`; it is not recreated by the clone.
