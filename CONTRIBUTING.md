# Contributing

## Development setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Tests

```powershell
python -m unittest discover -s tests -v
python -m unittest discover -s tools/tests -v
```

The first suite covers the generic policy engine, scaffolding, and a second policy. The second suite is the Northstar demo conformance suite.

## Style

- Runtime code is standard-library only.
- Use type hints.
- Keep policy behavior out of prompt text; prompts explain the policy, the engine applies it.
- Do not add scenario-specific branches to the engine.
- Add a test for every policy rule change.
- Commit messages describe the change, not a phase or step number.

## Pull requests

- Explain the policy or schema impact.
- Include a test that fails before the change and passes after it.
- Do not commit generated records, local settings, credentials, or raw room exports with personal identifiers.
