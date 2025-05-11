# Project LISA

## Comprehensive Feature Architecture and Operational Manual

## Table of Contents

- [Project LISA](#project-lisa)
  - [Comprehensive Feature Architecture and Operational Manual](#comprehensive-feature-architecture-and-operational-manual)
  - [Table of Contents](#table-of-contents)
    - [Introduction](#introduction)
  - [Core Features](#core-features)
    - [Task and Reminder Management](#task-and-reminder-management)
    - [Scheduling and Time Management](#scheduling-and-time-management)
    - [Modular Structure](#modular-structure)
    - [Study Module – Cybersecurity Coursework Support](#study-module--cybersecurity-coursework-support)
    - [Natural Language Processing (Local NLP)](#natural-language-processing-local-nlp)
    - [Offline AI Model Integration](#offline-ai-model-integration)
  - [Advanced and Optional Features](#advanced-and-optional-features)
    - [Local Web Interface](#local-web-interface)
    - [Voice Interaction (Speech Input/Output)](#voice-interaction-speech-inputoutput)
    - [Data Management and Security](#data-management-and-security)
    - [Integration and Extensibility](#integration-and-extensibility)
  - [Best Practices and Recommendations](#best-practices-and-recommendations)
    - [Recommended Workflow Example](#recommended-workflow-example)
    - [Common Use Cases](#common-use-cases)
    - [Tips for Effectiveness](#tips-for-effectiveness)
  - [Troubleshooting and FAQs](#troubleshooting-and-faqs)
  - [Appendices](#appendices)
    - [Glossary](#glossary)
    - [Reference Materials](#reference-materials)

### Introduction

This manual provides an in-depth exposition of Project LISA’s full feature set, architectural framework, and operational behavior. It is intended to function as both a technical reference and a user guide, supporting seamless deployment, practical use, and extensibility of the system’s capabilities.

Project LISA (Learning and Intelligent Scheduling Assistant) is a fully offline, privacy-conscious AI assistant designed to manage task lists, scheduling needs, and academic workflows—particularly within the domain of cybersecurity education. It is built on a modular, extensible architecture and is suitable for integration into diverse personal or institutional environments.

The sections that follow cover LISA’s core functionality, advanced features, configuration options, best practices for optimal use, and troubleshooting strategies. This document is intended for system integrators, developers, power users, and technical stakeholders.

---

## Core Features

### Task and Reminder Management

LISA enables users to create, view, edit, and delete tasks and reminders. These can be categorized across three primary modules—Work, Home, and Study—for contextual organization. Each task supports prioritization, metadata annotation, and scheduling.

Tasks are stored persistently in a local backend, using either human-readable JSON files or an optional SQLite database for more advanced querying and scalability. All task data is saved under the `data/` directory to ensure transparency and ease of management. This ensures that information is retained between sessions and can be easily backed up or migrated.

A built-in notification engine monitors tasks and sends alerts when due. Alerts may be delivered through the CLI or via desktop notifications depending on configuration. This ensures LISA can serve as a passive scheduler or proactive assistant, depending on user needs.

**Capabilities include:**

- Task creation, editing, deletion, and review
- Module-based task categorization (Work, Home, Study)
- Priority assignment and deadline management
- Persistent local storage via JSON or SQLite
- CLI and notification integration for alerts

### Scheduling and Time Management

LISA uses a built-in scheduler to track task deadlines, support recurring tasks, and provide time-based alerts. The scheduler integrates with system-level notifications and operates independently once configured.

**Features include:**

- Daily, weekly, and custom recurrence patterns
- Deadline tracking and missed-task alerts
- Optional integration with desktop notification frameworks

### Modular Structure

LISA is built on a modular architecture. Each module (Work, Home, Study) operates semi-independently and includes its own configuration, log files, and business logic. This design allows users to tailor behaviors per domain and supports the addition of future modules.

**Capabilities include:**

- Modular separation of concerns
- Per-module configuration and logging
- Easy extension or customization through isolated components

### Study Module – Cybersecurity Coursework Support

This module provides academic assistance using local datasets relevant to cybersecurity. A Q\&A system retrieves answers from structured datasets, enabling users to query concepts in natural language. Interactive flashcard and quiz modes provide an additional study layer.

Recommended datasets include:

- Security StackExchange QA archive
- OWASP Top 10 documentation
- MITRE ATT\&CK framework
- CISA Known Exploited Vulnerabilities catalog

All datasets are stored locally under the `data/` directory and can be extended or replaced by the user. Questions can be randomly selected or filtered by topic.

**Features include:**

- Natural language Q\&A using offline datasets
- Flashcard and quiz mode with indexed metadata
- Custom dataset integration and topic filtering

### Natural Language Processing (Local NLP)

LISA supports natural language input for task creation and query handling. Tasks like “Remind me to call Alice at 2 PM tomorrow” are parsed using NLP pipelines that extract task intent, date/time, and module categorization.

**Core functions include:**

- Free-form task input and interpretation
- Hybrid parser with Duckling/dateparser and LLM assistance
- Multi-intent command parsing with user confirmation

### Offline AI Model Integration

LISA uses locally hosted open-source large language models (LLMs) for natural language understanding and question answering. Supported models include Mistral 7B and TinyLlama, chosen for their strong performance and low resource requirements.

**System attributes include:**

- Full offline operation (no internet dependency)
- Configurable model memory footprint (quantized loading)
- Integration with FAISS for semantic search and retrieval-augmented generation (RAG)

---

## Advanced and Optional Features

### Local Web Interface

LISA includes a browser-accessible dashboard hosted locally on `localhost`. It provides an overview of tasks, module filters, and quick input forms.

**Key elements:**

- Task dashboard with due dates, categories, and filters
- Input forms for task creation and study queries
- Fully offline, responsive layout for desktop/mobile use

### Voice Interaction (Speech Input/Output)

Voice control is enabled using offline STT engines (Vosk or Whisper). The user can dictate tasks or ask questions via push-to-talk. Responses can be read aloud using a TTS engine.

**Capabilities include:**

- Vosk: lightweight, real-time, supports 20+ languages
- Whisper: higher accuracy with greater resource demands
- Configurable engine selection and voice feedback
- Guidance for tuning microphone and environment settings

### Data Management and Security

All data used by LISA is stored locally. The system supports optional encryption and automated backup for reliability.

**Features include:**

- JSON or SQLite-based task storage
- Optional AES encryption (Fernet or SQLCipher)
- Configurable backup scheduling and recovery procedures

### Integration and Extensibility

LISA supports modular integration with external tools and scripting environments. Import/export formats are standardized to enable interoperability.

**Integration options include:**

- ICS calendar file import/export for external calendar syncing
- CSV import/export for task lists
- CLI compatibility with cron, shell scripts, and automation systems

---

## Best Practices and Recommendations

### Recommended Workflow Example

- Start your day by reviewing tasks with `lisa list --today`
- Add new tasks using natural language or CLI flags
- Assign each task to a relevant module (e.g., Work, Study)
- Use recurring tasks for habitual actions like daily backups or weekly study blocks
- At the end of the week, audit completed tasks to review productivity

### Common Use Cases

- Academic planning: manage lectures, exams, and flashcard sessions
- Project tracking: divide tasks by context with priority levels
- Personal task flow: manage household routines or appointments

### Tips for Effectiveness

- Use the web dashboard for a quick visual overview of upcoming work
- Enable encryption if handling sensitive or personal information
- Regularly update or personalize the cybersecurity dataset
- Tailor each module’s settings to reflect your work or study routine

---

## Troubleshooting and FAQs

**Tasks not listed?** Use the `--module` or `--all` flag.

**Missed reminders?** Ensure the scheduler is running and the system clock is accurate.

**Parsing issues?** Use `--verbose` to debug the NLP pipeline.

**Module switching?** Add `--module <name>` to CLI commands.

**General issues?** Review logs in the respective module's log directory.

---

## Appendices

### Glossary

- NLP – Natural Language Processing
- LLM – Large Language Model
- STT – Speech to Text
- TTS – Text to Speech
- RAG – Retrieval-Augmented Generation
- ICS – iCalendar File Format

### Reference Materials

- Project GitHub Repository
- Mistral and TinyLlama Documentation
- Security StackExchange Archive on Kaggle
- Vosk STT and Whisper STT documentation

**Licensing**
All components are open-source and licensed under Apache 2.0 or MIT licenses.

**Changelog**
Please consult the `/docs/CHANGELOG.md` file for version history and release notes.

---

*This manual reflects the canonical design and functionality of Project LISA. It is maintained in sync with the source code and evolves as features are added or revised.*
