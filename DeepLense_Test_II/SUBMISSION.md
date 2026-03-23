# Before you hit “submit”

This is just a personal checklist I use so I don’t forget something dumb. The real rules are still **`GSoC26_DeepLense_Tests.md`** in the parent folder.

## What I’m linking in the form

| What | Where |
|------|--------|
| Test II notebook | `DeepLense_Test_II/Test_II_Agentic_AI.ipynb` |
| Optional copy of the modules | `DeepLense_Test_II/project/*.py` (same logic as the `%%writefile` cells) |

## Quick checks

1. **API key** — Search the notebook for `gsk_` or your real prefix. Should only see `YOUR_GROQ_API_KEY` (or similar) in anything you upload.
2. **Run order** — First cell installs + patches DeepLenseSim; then models → wrapper → agent; then tests. For plots that need `outputs/`, run **§6.2b** after **§6.2**.
3. **Outputs** — I usually submit with cleared outputs so the file isn’t huge; if you want pretty figures embedded, re-run all and save — your call.
4. **Test I** — Still need the classification notebook + metrics elsewhere; this folder is only Test II.

## Where it actually goes

Form link + email details are spelled out in the main test markdown. When in doubt: **ml4-sci@cern.ch** with the project title, not random DMs to mentors.
