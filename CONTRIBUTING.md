# Contributing to the ZeroBounce Postman collection

Thank you for your interest in contributing. This document explains how to get set up and submit changes.

## Code of Conduct

By participating in this project, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

See the [README](README.md) for importing the collection and setting its variables. CI checks that the collection is valid JSON in the Postman v2.1 format, that no request sends a hard-coded key, and that the key variables are empty.

```bash
python3 .github/scripts/check_collection.py
```

## How to Contribute

### Reporting Bugs

Open an [issue](https://github.com/zerobounce/postman-v2/issues) and include:

* What you did, step by step
* Expected vs actual behavior
* Relevant code or error messages

Never paste an API key, a real email address, or a raw API response that contains one into an issue.

### Submitting Changes

1. **Fork** the repository and create a branch from the default branch.
2. **Make your changes.** Use the `base_url`, `api_key` and `warmup_api_key` variables rather than literal values, and leave the key variables empty before committing.
3. **Commit** with a clear message (e.g. `Add X`, `Fix Y`).
4. **Push** your branch and open a **Pull Request**. Explain what changed and why, and link any related issues.

Maintainers will review and may request changes. Once approved, your PR can be merged.

## Releases (maintainers)

There is no package to publish. Users import the collection from `master`.

## Questions

* [ZeroBounce API docs](https://www.zerobounce.net/docs/)
* [Project homepage](https://zerobounce.net)
* Contact: **integrations@zerobounce.net**

Thanks for contributing.
