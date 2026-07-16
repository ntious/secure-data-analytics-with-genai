# Day 2 supplementary resources

These five resources extend the Day 2 topics of privacy-conscious analytics, local Python workflows, notebook security, analytical validation, and secure LLM use. They complement the workshop’s Metadata-Driven Secure Prompting workflow but do not guarantee privacy, security, or compliance.

## 1. NIST — Privacy Framework

[Explore the NIST Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework).

This voluntary framework helps organizations identify and manage privacy risk throughout data processing. It is useful for understanding why privacy requires ongoing risk management rather than relying only on de-identification, access control, or a checklist.

## 2. pandas — Getting started

[Use the official pandas getting-started guides](https://pandas.pydata.org/docs/getting_started/).

The pandas documentation provides maintained tutorials on reading tabular data, selecting rows and columns, handling missing values, calculating summaries, combining tables, and creating plots. It is the primary technical reference for the local DataFrame operations used in the workshop.

## 3. Project Jupyter — Security

[Review Project Jupyter’s security guidance](https://jupyter.org/security).

This official page explains the Jupyter project’s security resources and clarifies that data handling depends on whether notebooks run locally, through an institution, or through an external service. Treat notebooks as executable documents: review their code and trust source before running them.

## 4. scikit-learn — Common pitfalls and recommended practices

[Study scikit-learn’s common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html).

This guide explains inconsistent preprocessing, test-set contamination, data leakage, pipelines, and other mistakes that can produce misleadingly optimistic results. It directly supports the MDSP requirement to validate generated analytical code and assumptions before accepting results.

## 5. OWASP — LLM Prompt Injection Prevention Cheat Sheet

[Read the OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).

OWASP describes direct and indirect prompt injection, data exfiltration, malicious external content, and defense-in-depth measures such as input validation, least privilege, output screening, and human approval. This resource is most relevant when analytics systems connect LLMs to files, retrieval systems, APIs, or executable tools.

## Use of external resources

Links were reviewed on July 16, 2026. External pages may change, move, or become unavailable. Their content remains subject to the publishers’ terms and licenses. Inclusion here does not imply endorsement of every statement, tool, or linked third-party resource.

