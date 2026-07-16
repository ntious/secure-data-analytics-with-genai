# Secure Data Analytics with GenAI and LLMs

## From AI Literacy to Responsible Analytics

[![MIT License](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![CC BY 4.0](https://img.shields.io/badge/educational%20content-CC%20BY%204.0-lightgrey.svg)](CONTENT-LICENSE.md)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![CodeQL](https://img.shields.io/badge/security-CodeQL-2f81f7.svg)](.github/workflows/codeql.yml)

This public educational repository supports a two-day Python and Jupyter Notebook workshop on secure data analytics with GenAI, metadata-driven secure prompting, privacy-conscious AI-assisted analytics, and the responsible use of large language models.

## Workshop details

- **Dates:** July 16–17, 2026
- **Time:** 5:00–8:00 PM GMT | 1:00–4:00 PM EDT
- **Venue:** Online
- **Facilitators:**
  - **Dr. I. K. Nti**, Assistant Professor, University of Cincinnati, USA; Co-Lead, Information Technology Analytics Center
  - **Dr. F. Kyeremeh**, Sunyani Technical University, Ghana


## Workshop purpose

The workshop builds practical AI literacy before applying GenAI to local data analysis. It emphasizes metadata-only prompting, defensive code generation, human validation, and responsible AI for research and education without unnecessarily disclosing row-level data.

## Learning objectives

By the end of the workshop, participants should be able to:

- explain foundational AI, GenAI, and LLM concepts;
- construct clearer, structured prompts for research, teaching, writing, coding, and analytics;
- identify privacy, bias, copyright, academic-integrity, security, and accuracy risks;
- prepare reviewed metadata for metadata-driven secure prompting;
- run and validate AI-assisted analytical code locally; and
- design a privacy-conscious workflow for responsible AI-assisted analytics.

## Two-day workshop overview

### Day 1: AI Literacy, Prompt Engineering, and Responsible Use

Day 1 introduces participants to AI, generative AI, and large language models at a practical level. Participants examine how these systems work, their useful applications, their limitations, structured prompting methods, and responsible use in research, teaching, writing, coding, and knowledge work.

Learning outcomes:

- Explain core AI, GenAI, and LLM concepts in accessible terms.
- Describe practical uses of GenAI in research, teaching, writing, and knowledge work.
- Apply structured prompting techniques to improve AI outputs.
- Use AI tools for literature-review support, academic writing, idea generation, and coding assistance.
- Recognize ethical, privacy, bias, copyright, academic-integrity, and accuracy concerns.

See the [Day 1 materials](day-1/).

### Day 2: Secure Data Analytics with GenAI and LLMs

Day 2 applies GenAI skills to privacy-conscious, metadata-based data analytics. Participants learn how AI can support data understanding, question generation, analytical planning, code generation, interpretation, and validation without unnecessarily exposing raw sensitive data.

Learning outcomes:

- Distinguish safe, risky, and unsafe uses of AI for data analytics.
- Use reviewed metadata rather than raw data to generate research questions and analysis plans.
- Prompt AI to support data cleaning, coding, statistical planning, and visualization safely.
- Request defensive, beginner-readable Python code with validation and error handling.
- Evaluate AI-generated analytical outputs for accuracy, privacy, leakage, and responsible interpretation.
- Create a secure analytics blueprint for AI-assisted data work.

See the [Day 2 materials](day-2/).

## Metadata-Driven Secure Prompting workflow

The Metadata-Driven Secure Prompting (MDSP) workflow is a practical risk-reduction pattern:

1. Keep raw data local.
2. Extract metadata locally.
3. Review and remove risky metadata.
4. Prompt GenAI using sanitized metadata only.
5. Run generated code locally.
6. Validate the code, results, assumptions, and privacy implications.

> **Metadata is safer than raw data, but metadata is not automatically safe.**

Column names, free-text descriptions, uncommon categories, schema combinations, and statistics can still reveal confidential or identifying information. Review metadata before sharing it with any external system.

## Repository structure

```text
.
├── day-1/
│   ├── data/
│   ├── docs/
│   ├── figures/
│   ├── group_activity/
│   ├── notebooks/
│   └── scripts/
├── day-2/
│   ├── data/
│   ├── docs/
│   ├── figures/
│   ├── group_activity/
│   ├── notebooks/
│   └── scripts/
└── .github/
```

## Getting started

1. Clone or download the repository.
2. Install Python 3 and JupyterLab or Jupyter Notebook.
3. Create and activate a local virtual environment.
4. Install only the packages required by the material you plan to use.
5. Begin with the [Day 1 guide](day-1/) or [Day 2 guide](day-2/).

## Required tools

- A current Python 3 release
- JupyterLab, Jupyter Notebook, or a compatible notebook environment
- A modern web browser
- A text editor or integrated development environment
- Optional access to a facilitator-approved GenAI tool, subject to institutional policy

## How to use the notebooks

Read each notebook before running it. Confirm all file paths, dependencies, and data sources; run cells in order; keep sensitive data local; and inspect generated code before execution. Notebook validation in this repository checks JSON and syntax but deliberately does not execute analyses, download data, or contact model services.

## Privacy and responsible-use notice

Do not upload confidential records, direct identifiers, participant submissions, credentials, private URLs, or sensitive raw datasets. The repository does not guarantee anonymity, privacy preservation, security, or regulatory compliance. Users are responsible for reviewing applicable organizational, institutional, legal, contractual, and ethical requirements.

## Synthetic-data notice

Public workshop datasets may be synthetic or openly licensed. Synthetic datasets should be treated according to the sensitivity represented by their schema. A synthetic table that models health, financial, education, employment, or other sensitive records can still normalize unsafe handling practices or expose a sensitive schema.

## Group activity overview

Activities ask participants to classify AI-assisted analytics scenarios, review metadata, design prompts, inspect generated code, and validate interpretations. Use only the materials provided in the day folders or facilitator-approved substitutes.

## Contributing

Contributions are welcome when they preserve participant privacy, document provenance, and improve educational value. Read the [Contribution guide](CONTRIBUTING.md) and follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security reporting

Do not report suspected vulnerabilities or exposed secrets in a public issue. Follow the private reporting instructions in the [Security policy](SECURITY.md).

## Citation

Citation metadata is provided in [CITATION.cff](CITATION.cff). Update `REPOSITORY_URL` before publishing a release.

## Licenses

Code including scripts, notebook code cells, reusable examples, configuration, and workflow files—is licensed under the [MIT License](LICENSE). Educational content—including Markdown, workshop notes, figures, activity instructions, diagrams, and notebook Markdown cells—is licensed under [CC BY 4.0](CONTENT-LICENSE.md). Third-party datasets and libraries retain their original terms.

## Acknowledgments

Thanks to the facilitators, workshop contributors, reviewers, and open-source communities whose tools support responsible analytics education.

## Disclaimer

These materials are educational examples, not legal, compliance, privacy, cybersecurity, or production-deployment advice. AI-generated code and analysis may be incomplete, biased, insecure, or incorrect and must be independently reviewed.
