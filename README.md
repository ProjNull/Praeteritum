<!--
Credit for this README where credit's due:
- https://github.com/othneildrew/Best-README-Template/blob/main/README.md
- https://github.com/Louis3797/awesome-readme-template

These two templates have been extremely helpful when creating my own README template
and I've drawn inspiration from them heavily.

Please keep this acknowledgement in further modifications of the README file, though
it's not like I can tell you what to do. I'm just a comment in a text file.

Copyright 2025 (c) HyScript7
-->

<div align="center">
  <!-- Logo or Icon -->
  <a href="https://github.com/ProjNull/Praeteritum">
    <img src="images/logo.svg" alt="logo" width="150" height="auto" />
  </a>
  <h1>Praeteritum</h1>
  <!-- Badges -->
  <p>
  </p>
  <!-- Short Description -->
  <p>
  A free & open-source retrospective application.
  </p>
</div>

<details>
  <summary>📋 Table of Contents</summary>
  <ol>
    <li><a href="#about">🚀 About</a></li>
    <li>
      <a href="#getting-started">🏁 Getting Started</a>
      <ul>
        <li><a href="#prerequisites">✅ Prerequisites</a></li>
        <li><a href="#installing-dependencies">📦 Installing dependencies</a></li>
        <li><a href="#building">🏗️ Building</a></li>
        <li><a href="#testing">🧪 Testing</a></li>
        <li><a href="#running-for-development">🔧 Running for Development</a></li>
        <li><a href="#running-for-production">🚀 Running for Production</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">🗺️ Roadmap</a></li>
    <li>
      <a href="#contributing">🤝 Contributing</a>
      <ul>
        <a href="#how-to-contribute">How to Contribute</a>
      </ul>
    </li>
    <li><a href="#support">✉️ Support</a></li>
    <li><a href="#license">📄 License</a></li>
    <li><a href="#acknowledgments">💖 Acknowledgments</a></li>
  </ol>
</details>

<a id="about"></a>

## 🚀 About

**Praeteritum** is an open-source retrospect application, that was originally
created on a hackathon and later worked on during our week of practical education.

We now aim to rewrite it for performant, production-ready use with a micro service
architecture.

<a id="built-with"></a>

## 🛠️ Built with

<!-- https://ileriayo.github.io/markdown-badges/ -->

- [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
! [![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
! [![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
- [![Keycloak](https://img.shields.io/badge/Keycloak-%23418bc9.svg?style=for-the-badge&logo=keycloak&logoColor=white)](https://www.keycloak.org/)
- [![Angular](https://img.shields.io/badge/angular-%23DD0031.svg?style=for-the-badge&logo=angular&logoColor=white)](https://angular.dev/)
- [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

<a id="getting-started"></a>

## 🏁 Getting started

This section will walk you through setting up the project locally. You can also
consult the [Contributing Guide](./CONTRIBUTING.md) for more information.

<a id="prerequisites"></a>

### ✅ Prerequisites

Before you can setup the project, you need to have the following installed
and/or prepared:

- [Docker](https://docker.com/) (or [Podman](https://podman.io/))
- docker-compose (or podman-compose)

<a id="installing-dependencies"></a>

### 📦 Installing dependencies

After you clone the project using git or github cli
([concrete commands here](CONTRIBUTING.md#development-environment-setup)), you
need to install the project dependencies using the appropriate package manager.

For the backend, since there are many services, some written in other languages,
you should refer to a README inside of the micro service you are going to be
working with.

For the frontend, you need to run `pnpm install` in the frontend directory.

<a id="building"></a>

### 🏗️ Building

To build the project, you can follow the steps below:

1. Make sure you are in the root of the repository directory
2. Run the command below

   ```sh
   docker-compose build
   ```

<a id="testing"></a>

### 🧪 Testing

This section will be updated as tests are implemented.

<a id="running-for-development"></a>

### 🔧 Running for Development

Since there are many services in this project, it's recommend you
run the ones you are not actively developing using `docker-compose`.

The `docker-compose.yml` file outlines which services should be using what ports.

<a id="running-for-production"></a>

### 🚀 Running for Production

This section will be updated with the first release.

<a id="roadmap"></a>

## 🗺️ Roadmap

- [ ] 1.0.0 Release
  - [ ] User Authentication (OAuth)
  - [ ] User Profiles
    - [ ] Custom Avatars
    - [ ] Settings & Preferences
  - [ ] Organizations
    - [ ] Organization Roles
    - [ ] Invites
  - [ ] Retrospectives
    - [ ] Feedbacks

<a id="contributing"></a>

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to
learn, inspire, and create. Any contributions you make are **greatly appreciated**!

### How to contribute

1. Fork the project.
2. Create your feature branch:

   ```bash
   git checkout -b feature/amazing-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add some amazing feature"
   ```

4. Push to the branch:

   ```bash
   git push origin feature/amazing-feature
   ```

5. Open a pull request.

For more detailed guidelines, check out [CONTRIBUTING.md](CONTRIBUTING.md).

<a id="support"></a>

## ✉️ Support

If you encounter any issues or have questions, feel free to:

- Open an issue in the [Issues tab](https://github.com/ProjNull/Praeteritum/issues).
- Reach out via email at **[contact@projnull.eu](mailto:contact@projnull.eu)**.
- Contact the repository maintainers on discord: [discord.gg/A3cfN4heE7](https://discord.gg/A3cfN4heE7)

We’re here to help!

<a id="license"></a>

## 📄 License

This project is licensed under the
**[BSD 3-Clause "New" or "Revised" License](LICENSE)** - feel free to use,
modify, and distribute this project in accordance with the license terms.

<a id="acknowledgments"></a>

## 💖 Acknowledgments

I would like to express my deepest gratitude to the following individuals and organizations:

- [G+SOŠ](https://gasos-ro.cz/cs/) - For organizing the hackathon where the
  initial version of the project was created.
- [Certicon a.s.](https://www.certicon.cz/) - For allowing us to continue
  working on this project during our school's practical education week.
