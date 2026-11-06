# Environment

Component versions recorded from the build machine on 2026-11-04. Model and effort confirmed from the clean-room agent sessions on 2026-11-05 and the three-room run on 2026-11-06.

| Component | Version |
|---|---|
| Switch Console | 0.40.1 |
| Switch core | 0.31.0 |
| Mattermost | 11.9.0 |
| Claude Code | 2.1.318 |
| Python | 3.11.9 |
| Git | 2.49.0.windows.1 |
| OS | Windows 11 Pro, 10.0.26200, 64-bit |

## Agent settings

- Provider: Claude Code.
- Working directory: an empty local directory outside this repository.
- Auto mode: off.
- Bypass permissions: off.
- Tools: shell, network, file-search, and external actions disabled; room context only.
- Who can talk: owner plus the owner's agents (`Me and my agents`).
- Room membership: `bid-analyst` is in `bid-intake` and `bid-record`; `bid-critic` is in `bid-review` only; `room-auditor` joins `bid-record` only after the decision.
- The human is the only member of all three rooms and relays missing-fact questions between the analyst and critic.

These are manual Console settings. Verify them in the agent's **General** and **Advanced** pages before the final run. Do not commit agent settings files or credentials.

## Model and effort

| Setting | Value |
|---|---|
| Model | `deepseek-v4.1-flash` |
| Reasoning effort | `high` |

Both values applied to the analyst, critic, and fresh-agent auditor in the clean-room run. They are configured in Switch Console; verify them in each agent's **Advanced configuration** before recording.

## Reproducibility note

The validator, sample data, and record format are reproducible from a clean clone. The Switch room depends on the manual setup in `examples/northstar/docs/setup.md` and the live versions above.
