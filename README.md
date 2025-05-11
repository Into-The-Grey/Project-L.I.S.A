[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](./LICENSE)

# Project L.I.S.A — Learning and Intelligent Scheduling Assistant

**Project LISA** is a fully offline, modular AI assistant for task management, time scheduling, and cybersecurity coursework support. Built for privacy and local execution, it integrates open-source NLP models, structured datasets, and a flexible architecture that supports CLI and web interfaces.

---

## 🔧 Core Features

- Modular task manager (Work, Home, Study contexts)
- Local scheduling and recurring reminders
- Natural language input (e.g., “remind me to review at 6 PM”)
- Cybersecurity Q&A support using offline datasets
- Flashcard and quiz study modes
- Optional voice command support (Vosk / Whisper)
- Local-only operation — no cloud or external services

---

## 🚀 Quickstart

```bash
git clone https://github.com/your-username/project-lisa.git
cd project-lisa
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python core/main.py  # or ./lisa if CLI entrypoint is aliased
```

> 📦 Ensure you have Python 3.10+ and at least 8 GB RAM for LLM usage. Models are stored in `models/`.

---

## 📂 Project Structure

- `core/` – Core logic: scheduler, CLI, NLP interface
- `modules/` – Work, Home, Study modules (independent configs and logs)
- `data/` – Local Q&A datasets, calendars, task DB
- `models/` – Local LLMs and vector indexes
- `docs/` – Full manual and changelog

---

## 📘 Documentation

- [📚 Full Manual](./docs/README.md) – Features, usage, and configuration guide
- [🛠 Changelog](./docs/CHANGELOG.md)
- [📄 License](./LICENSE)

---

## 🧠 Models & Dependencies

LISA supports quantized local LLMs such as:

- [Mistral 7B (Apache 2.0)](https://mistral.ai/news/introducing-mistral-7b/)
- [TinyLlama (1.1B)](https://huggingface.co/TinyLlama)
- [GPT4All Ecosystem](https://gpt4all.io/)

NLP parsing uses Duckling + `dateparser`, and offline STT via [Vosk](https://alphacephei.com/vosk/) or [Whisper](https://github.com/openai/whisper).

---

## 🛡 Privacy-First Design

LISA runs entirely offline:

- No telemetry
- No cloud APIs
- All data stored locally
