# Contributing

Thank you for helping improve this educational repository.

## Proposing a change

Open an issue for substantial changes, or create a focused branch and pull request for a well-scoped correction. Describe the educational need, affected workshop day, validation performed, and any data or licensing considerations.

## Branch and pull-request workflow

1. Create a short-lived branch from `main`.
2. Make focused changes without mixing unrelated cleanup.
3. Run the relevant validation checks.
4. Update documentation and links.
5. Submit a pull request using the repository template.

## Code and notebook standards

- Write beginner-readable Python with clear names, small functions, validation, and useful error messages.
- Avoid hidden network calls, unsafe deserialization, embedded credentials, and unnecessary dependencies.
- Keep notebooks reproducible and ordered from setup through interpretation.
- Clear outputs that contain row-level data, local paths, tokens, identifiers, or other unintended disclosures.
- Do not auto-execute notebooks that require private data, long training, network access, or unknown dependencies.

## Privacy requirements

Never upload confidential or sensitive raw datasets, participant submissions, registration exports, private facilitator notes, credentials, meeting links, or institutional secrets. Review metadata as carefully as raw data: column names, free text, uncommon categories, and combinations can be identifying.

## Testing and validation

Before submitting:

- validate notebook JSON and compile code cells without executing data analysis;
- run Python syntax checks;
- verify relative Markdown links;
- confirm that examples do not expose sensitive values;
- document required dependencies and data provenance; and
- inspect the diff for secrets and unintended notebook output.

## Documentation standards

Use one clear purpose per page, descriptive headings, meaningful link text, image alternative text, consistent terminology, and accessible language. Distinguish planned resources from available resources and do not create broken placeholder links.

## Licensing contributions

By contributing, you agree that code contributions are provided under the MIT License and educational-content contributions under CC BY 4.0, unless a compatible third-party license is clearly identified. Do not contribute material you do not have the right to share.

## Respectful participation

All contributors must follow the [Code of Conduct](CODE_OF_CONDUCT.md).

