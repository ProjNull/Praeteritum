# Contributing

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#how-to-contribute">How to Contribute</a>
      <ul>
        <li><a href="#reporting-issues">Reporting Issues</a></li>
        <li><a href="#suggesting-features">Suggesting Features</a></li>
        <li><a href="#contributing-code">Contributing Code</a></li>
      </ul>
    </li>
    <li>
      <a href="#development-setup">Development Setup</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li>
            <a href="#development-environment-setup">Development Environment Setup</a>
        </li>
      </ul>
    </li>
    <li>
        <a href="#style-guidelines">Style Guidelines</a>
    </li>
    <li><a href="#pull-request-process">Pull Request Process</a></li>
  </ol>
</details>

## How to Contribute

### Reporting Issues

If you encounter bugs or have ideas for improvements:

1. Search [existing issues](https://github.com/ProjNull/Praeteritum/issues) to
   avoid duplicates.

2. If no related issue exists, create one with the following:
   - **Title**: Clear and concise.
   - **Description**: Detailed explanation, including screenshots or logs if relevant.
   - **Reproduction Steps**: Precise steps to reproduce the issue.

### Suggesting Features

To propose a new feature, open a discussion or issue. Provide:

- Use case(s) or scenarios for the feature.
- Why it benefits the project.
- Any relevant examples or references.

### Contributing Code

If you have a solution, patch or implementation relating to a suggested feature
or reported issue, you can implement it and [open a pull request](https://github.com/ProjNull/Praeteritum/compare).

## Development Setup

This section will walk you through how to setup your local development
environment for work on this code base.

### Prerequisites

Before you can get started, make sure you have the following installed or prepared:

- [Docker](https://docker.com/) (or [Podman](https://podman.io/))
- docker-compose (or podman-compose)

Additionally, you need any programming languages that the micro services you are
going to be working with are written in.

### Development Environment Setup

1. Clone the repository using one of the methods below:

   ```sh
   git clone git@github.com:ProjNull/Praeteritum.git
   git clone https://github.com/ProjNull/Praeteritum.git
   gh repo clone ProjNull/Praeteritum
   ```

2. Open the project in your preferred IDE

3. Install dependencies and project modules

## Style Guidelines

To keep style across the codebase somewhat consistent, you can find guidelines
for individual sections below. Please attempt to follow them.
If you don't, but your code is understandable and readable, you can go without these.

<!-- Kinda ironic considering most of what I write is comparable to hieroglyphs -->

```txt
Use meaningful commit messages (e.g., fix: resolve issue with X or feat: add Y functionality).
Write tests for new features or fixes.
```

## Pull Request Process

1. Fork the repo and create your branch:

    ```sh
    git checkout -b feature/your-feature
    ```

2. Make your changes and ensure:
   Linting passes (if there is any).
   That all relevant tests pass (if there are any).

3. Push to your fork and open a pull request:
   Describe your changes in detail.
   Link relevant issues or discussions.

4. Respond to feedback and make updates as needed.
