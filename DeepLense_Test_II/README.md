# DeepLense Test II — Agentic AI for Gravitational Lensing

Small project for the GSoC Agentic AI track: you chat (via Pydantic AI + Groq), and **DeepLenseSim** generates strong-lensing images with different DM substructure recipes (`no_sub`, `cdm`, `axion`).

## What this is

I wrapped DeepLenseSim behind Pydantic models so parameters stay typed and checked before any heavy ray-tracing runs. The agent has tools for “show me a plan” vs “actually run it”, which made it easier to bolt on a human-in-the-loop flow even inside a notebook.

### Substructure flavours

| Code | Rough idea | What you might notice |
|------|------------|------------------------|
| `no_sub` | Smooth halo | Clean ring-ish arcs |
| `cdm` | Subhalos | Extra wiggles / perturbations |
| `axion` | Vortex-y | More asymmetric distortions |

## Flow (one sentence version)

User text → Pydantic AI (Groq) → tools → `SimulationRequest` → `LensingSimulator` → DeepLenseSim → `.npy` on disk + JSON-ish metadata back through the agent.

### Files

| Path | Role |
|------|------|
| `project/models.py` | Schemas + physics checks |
| `project/sim_wrapper.py` | Model I (`simple_sim`) vs Model II (Euclid-style + `simple_sim_2`) |
| `project/agent.py` | Agent + tools |
| `Test_II_Agentic_AI.ipynb` | The whole story: setup, code cells that write the `.py` files, tests, plots |

The notebook’s **`%%writefile`** cells define `models.py`, `sim_wrapper.py`, and `agent.py`; the same files live under **`project/`** and are exported from the notebook so they stay identical (see `project/README.md`).

## Running it (Colab is easiest)

1. Upload / open `Test_II_Agentic_AI.ipynb`.
2. Put your Groq key in §2 (swap back to a placeholder before you share the notebook anywhere public).
3. Run top to bottom. If you want images in `outputs/`, don’t skip **§6.2b** after **§6.2** — the notebook explains why (tl;dr: no chat memory between cells).

There’s more hand-written context in the notebook itself (especially §1 design notes and §7).

### Example `run_sync` ideas

```python
result = agent.run_sync("Generate 3 CDM lensing images")
# …and for something that should fail:
result = agent.run_sync("Generate images with z_halo=2.0 and z_gal=0.5")
```

## Dependencies

Pydantic AI, Groq, lenstronomy 1.9.2, pyhalo, colossus, DeepLenseSim (cloned in the first notebook cell). The setup cell patches a few Python 3.12 / Colab quirks — see comments there.

## Submitting this for GSoC

The canonical instructions live in **`GSoC26_DeepLense_Tests.md`** at the repo root. Quick sanity list:

- [ ] Notebook included / linked, key scrubbed.
- [ ] Your repo URL (own branch — don’t PR upstream DeepLenseSim).
- [ ] Form + portal proposal + CV per the official doc.
- [ ] **Test I** (classification + ROC/AUC) is separate but still required for the full application.

A slightly more detailed checklist: [`SUBMISSION.md`](SUBMISSION.md). If you like templates, there’s also [`../Submission_Packet_Template.md`](../Submission_Packet_Template.md).
