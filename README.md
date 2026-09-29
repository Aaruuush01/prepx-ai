# PrepX AI — Private On-Device Interview Coach

**Snapdragon® AI Lab Build & Present Challenge 2026 — Qualcomm**

PrepX AI is a privacy-first interview preparation desktop/web prototype designed for Snapdragon-powered HP PCs. It analyzes a candidate's resume and job description, generates a personalized interview plan, conducts mock interviews, and provides structured feedback. The production architecture is designed around Qualcomm AI Hub / QNN-compatible on-device models so sensitive career documents and voice data can remain on the device.

> **Important:** This repository contains a runnable CPU reference demo. It does **not** claim that NPU inference is active unless the Qualcomm runtime/model adapter is configured and actually measured on a compatible Snapdragon PC.

## Why this idea?

Most interview tools send resumes, job descriptions, answers, and sometimes voice recordings to cloud APIs. PrepX is designed around a different principle:

**Your career data stays on your laptop.**

On a Snapdragon PC, the planned production path uses:
- Qualcomm AI Hub optimized models
- Llama 3.2 1B/3B class local generation for coaching
- Whisper for local speech-to-text
- ONNX Runtime / QNN or Qualcomm Genie/QAIRT where supported
- CPU fallback for development and judging environments without Snapdragon hardware

Qualcomm documents Windows-on-Snapdragon development across CPU, GPU and Hexagon NPU, and its AI Hub provides deployable optimized models. See the official resources in `docs/RESOURCES.md`.

## Core workflow

1. Upload/paste resume.
2. Paste a job description.
3. PrepX extracts skills, projects and role requirements.
4. It builds a personalized interview plan.
5. Start a mock interview.
6. Answer by text today; optional local Whisper adapter can provide voice transcription.
7. PrepX analyzes answer structure, relevance, specificity and filler words.
8. Generate a final preparation report.

## Challenge alignment

| Evaluation criterion | PrepX implementation |
|---|---|
| Technical Implementation | Modular inference layer, local document processing, retrieval-style context, optional Qualcomm adapter |
| Application Use Case & Innovation | Career coaching without sending private resume/voice data to a server |
| Deployment & Accessibility | Streamlit prototype now; designed for native Windows on Snapdragon; CPU fallback |
| Presentation & Documentation | Architecture, deployment plan, demo flow, limitations and submission summary |

## Project structure

```text
prepx_ai/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── MODEL_PLAN.md
│   ├── SUBMISSION_SUMMARY.md
│   └── RESOURCES.md
├── sample_data/
│   ├── sample_resume.txt
│   └── sample_jd.txt
└── tests/
    └── test_core.py
```

## Run locally

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit.

## Optional PDF resume support

The app accepts `.txt` and `.pdf` resume files. PDF extraction uses PyMuPDF.

## Qualcomm / Snapdragon deployment

The code separates the application layer from the inference layer. For a Snapdragon deployment, replace the reference `LocalCoachEngine` with a model adapter backed by Qualcomm AI Hub exported assets and an appropriate runtime.

Do not present simulated latency or CPU inference as NPU benchmark data. Record actual measurements on the target Snapdragon HP PC.

## Demo script

**0:00–0:20 — Problem**
Career documents and voice answers are sensitive. Cloud interview tools require users to upload them.

**0:20–0:45 — Solution**
PrepX is a local interview coach that turns a resume + JD into a personalized mock interview.

**0:45–1:30 — Live demo**
Paste a resume and JD → generate skill gaps → start interview → submit answer → receive structured feedback.

**1:30–2:00 — Snapdragon**
Show the local inference architecture and explain that the production build maps model workloads to Qualcomm's NPU using supported AI Hub/QNN/Genie paths.

**2:00–2:30 — Differentiation**
Private-by-design, offline-capable, low-latency, no per-question cloud API cost, and designed for Windows on Snapdragon.

## Responsible claims

This repository intentionally distinguishes:
- **Implemented:** CPU reference demo.
- **Designed:** Qualcomm AI Hub/QNN production adapter.
- **Measured:** only numbers collected on an actual target device.

Never claim NPU acceleration unless it has been verified on the actual hardware.

## License

MIT for the application code. Model licenses remain those of their respective model owners.
