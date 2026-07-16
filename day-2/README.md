# Day 2: Secure Data Analytics with GenAI and LLMs

## Session description

Day 2 applies GenAI skills to privacy-conscious, metadata-based data analytics. Participants learn how AI can support data understanding, question generation, analytical planning, code generation, interpretation, and validation without unnecessarily exposing raw sensitive data.

## Learning outcomes

- Distinguish safe, risky, and unsafe uses of AI for data analytics.
- Use reviewed metadata rather than raw data to generate research questions and analysis plans.
- Prompt AI to support data cleaning, coding, statistical planning, and visualization safely.
- Request defensive, beginner-readable Python code with validation and error handling.
- Evaluate AI-generated analytical outputs for accuracy, privacy, leakage, and responsible interpretation.
- Create a secure analytics blueprint for AI-assisted data work.

## Expected preparation

Complete Day 1 or review its core concepts. Install Python, Jupyter, and the dependencies declared by the notebook you intend to use. Download materials locally. Do not substitute private data for the workshop dataset.

> **Metadata is safer than raw data, but metadata is not automatically safe.**

## Folder guide

- [`data/`](data/) — workshop data and research-question text.
- [`docs/`](docs/) — session notes, prompts, and data-resource guidance.
- [`figures/`](figures/) — generated analytical figures.
- [`group_activity/`](group_activity/) — group instructions and a partial-code notebook.
- [`notebooks/`](notebooks/) — starter and comparative GenAI-assisted notebooks.
- [`scripts/`](scripts/) — local dataset-inspection scripts.

## Recommended sequence

1. Review [`docs/Day 2 session 1.pdf`](docs/Day%202%20session%201.pdf).
2. Open [`notebooks/start_here_01.ipynb`](notebooks/start_here_01.ipynb).
3. Review [`docs/create_metadata_prompt.md`](docs/create_metadata_prompt.md).
4. Review [`docs/create_analysis.md`](docs/create_analysis.md).
5. Compare the available GenAI-assisted analysis notebooks.
6. Complete the group activity and validate privacy, code, assumptions, and results.

## Notebooks

- [`start_here_01.ipynb`](notebooks/start_here_01.ipynb)
- [`group_activity_patial_code.ipynb`](group_activity/group_activity_patial_code.ipynb) — existing filename retained to avoid overwriting workshop material.
- [`Codex analysis notebook`](notebooks/analyse_notebooks_by_genai/mdsp_california_housing_analysis%28codex%29.ipynb)
- [`Claude analysis notebook`](notebooks/analyse_notebooks_by_genai/mdsp_california_housing_analysis%28claude%29.ipynb)
- [`ChatGPT analysis notebook`](notebooks/analyse_notebooks_by_genai/mdsp_california_housing_analysis%28chatgpt%29.ipynb)
- [`Gemini analysis notebook`](notebooks/analyse_notebooks_by_genai/mdsp_california_housing_analysis%20%28gemini%29.ipynb)

## Group activity

Use the [group-activity instructions](group_activity/group_activity.pdf) and the [partial-code notebook](group_activity/group_activity_patial_code.ipynb). Treat all exercise schemas according to the sensitivity they represent.

## Completion checklist

- [ ] I kept raw data local.
- [ ] I extracted and reviewed metadata locally.
- [ ] I removed or generalized risky metadata before prompting.
- [ ] I inspected generated code before running it.
- [ ] I validated outputs, assumptions, leakage risk, and interpretation.
- [ ] I documented limitations and responsible-use constraints.

## Troubleshooting

See [Troubleshooting](#troubleshooting) below.

- Confirm that notebook paths are relative to the repository root or current notebook.
- Install only explicitly required packages in an isolated environment.
- Do not enable network access merely to make an unknown notebook cell succeed.
- If a dataset path fails, select the public workshop file in [`data/`](data/) rather than private data.
- Clear sensitive outputs before saving or sharing a notebook.

[Back to the workshop README](../README.md)

