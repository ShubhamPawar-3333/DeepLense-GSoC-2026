# DeepLense — GSoC 2026 Evaluation Tests

**Contributor:** Shubham Pawar  
**Organization:** [ML4SCI](https://ml4sci.org/)  
**Project:** [Agentic AI for Gravitational Lensing Simulations](https://ml4sci.org/gsoc/2026/proposal_DEEPLENSE1.html)  
**Repository:** Test submissions for GSoC 2026 evaluation

---

## Test I — Multi-Class Classification

**Objective:** Classify simulated gravitational lensing images into three dark matter substructure types — `no_substructure`, `sphere` (CDM), and `vort` (axion).

**Approach:**
- ResNet18 with pretrained ImageNet weights, fine-tuned on the DeepLense dataset
- Learning rate: `1e-4`, epochs: `20`, optimizer: Adam with weight decay
- Multi-seed robustness evaluation across 3 random seeds

**Key Results:**

| Metric | Value |
|--------|-------|
| Macro ROC-AUC | **0.9854** |
| Accuracy | 92.36% |
| No-Sub Recall | 97.84% |
| Sphere Recall | 84.20% |
| Vort Recall | 95.04% |

**Notebook:** [`DeepLense_Test_I/Test_I_Classification.ipynb`](DeepLense_Test_I/Test_I_Classification.ipynb)

---

## Test II — Agentic AI for Simulation Workflows

**Objective:** Build an LLM-powered agent that autonomously orchestrates gravitational lensing simulation workflows using DeepLenseSim.

**Approach:**
- **Framework:** Pydantic AI with Groq-hosted Llama 3.3 70B
- **Pydantic schemas** for simulation parameters with physics validation (e.g., `z_source > z_lens`)
- **Human-in-the-loop** confirmation before executing simulations
- **Tool functions** for simulation execution, parameter validation, and error handling
- **Model support:** Model_I (NFW + Hernquist) and Model_II (NFW + double Sérsic)

**Key Features:**
- Natural language → structured simulation plan → validated images
- Physics constraints enforced at the schema level
- Error detection and automatic parameter correction
- Side-by-side Model_I vs Model_II comparison

**Notebook:** [`DeepLense_Test_II/Test_II_Agentic_AI.ipynb`](DeepLense_Test_II/Test_II_Agentic_AI.ipynb)  
**Project modules:** [`DeepLense_Test_II/project/`](DeepLense_Test_II/project/)

---

## Repository Structure

```
├── DeepLense_Test_I/
│   └── Test_I_Classification.ipynb      # Multi-class classification
│
├── DeepLense_Test_II/
│   ├── Test_II_Agentic_AI.ipynb         # Agentic AI notebook
│   ├── project/
│   │   ├── models.py                    # Pydantic schemas
│   │   ├── sim_wrapper.py               # DeepLenseSim wrapper
│   │   └── agent.py                     # Pydantic AI agent
│   ├── requirements.txt                 # Dependencies
│   ├── .env.example                     # API key template
│   └── .gitignore
│
└── GSoC_2026_Proposal.pdf               # Project proposal
```

---

## Setup

### Test I
Open `Test_I_Classification.ipynb` in Google Colab — all dependencies are installed inline. Dataset is auto-downloaded via `gdown`.

### Test II
```bash
cd DeepLense_Test_II
pip install -r requirements.txt
```
Set your Groq API key:
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```
Then run `Test_II_Agentic_AI.ipynb`.

---

## Contact

- **Email:** shuubham.pawar.368@gmail.com
- **GitHub:** [ShubhamPawar-3333](https://github.com/ShubhamPawar-3333)
- **LinkedIn:** [shubham-dilip-pawar](https://linkedin.com/in/shubham-dilip-pawar)
