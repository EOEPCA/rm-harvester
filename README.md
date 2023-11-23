<!--
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** template-svce, twitter_handle, email
-->

<!-- PROJECT SHIELDS -->
<!--
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
![Build][build-shield]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/EOEPCA/rm-harvester">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">EOEPCA Data Access - Harvester</h3>

  <p align="center">
    This repository includes the EOEPCA Data Access Harvester component
    <br />
    <a href="https://github.com/EOEPCA/rm-harvester"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/EOEPCA/rm-harvester">View Demo</a>
    ·
    <a href="https://github.com/EOEPCA/rm-harvester/issues">Report Bug</a>
    ·
    <a href="https://github.com/EOEPCA/rm-harvester/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [Description](#description)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Deployment](#deployment)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->

## Description

The EOEPCA Data Access Harvester component is built upon the upstream View Server Harvester component.

View Server is a Docker based software and all of its components are distributed and executed in context of Docker images, containers and Helm charts. Basic knowledge of Docker and either Docker Swarm or Helm and Kubernetes is a prerequisite.

The provided external services are services for searching, viewing, and downloading of Earth Observation (EO) data. Service endpoints optimized for performance as well as for flexibility are provided alongside each other.

The View Server default Chart vs consists of the following service components (with their respective Docker image in parenthesis):

* Web Client (client)
* Cache (cache)
* Renderer (core)
* Registrar (core)
* Seeder (seeder)
* Preprocessor (preprocessor)
* Ingestor (ingestor)
* Harvester (harvester)
* Scheduler (scheduler)
* Database (postgis)
* Queue Manager (redis)

The EOEPCA Data Access Harvester component extends the View Server Harvester.
View Server is Open Source, released under an MIT license.


### Built With

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [GDAL](https://gdal.org/)
- [PostGIS](https://postgis.net/)
- [EOXServer](https://github.com/EOxServer/eoxserver)
- [EOX View Server](https://gitlab.eox.at/vs/vs)

<!-- GETTING STARTED -->

## Getting Started

To get a View Server copy up and running follow these simple steps.

https://vs.pages.eox.at/vs/operator/k8s.html#operating-k8s

### Deployment

Data Access Harvester deployment is described [here](https://deployment-guide.docs.eoepca.org/current/eoepca/data-access/#harvester) in the [EOEPCA Deployment Guide](https://deployment-guide.docs.eoepca.org/current/eoepca/data-access/).


## Documentation

The component documentation can be found at https://vs.pages.eox.at/vs/operator/k8s.html#harvester-configuration-harvester.

<!-- USAGE EXAMPLES -->


<!-- ROADMAP -->

## Roadmap

See the [open issues](https://github.com/EOEPCA/rm-harvester/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the Apache-2.0 License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

Project Link: [https://github.com/EOEPCA/rm-harvester](https://github.com/EOEPCA/rm-harvester)

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

- README.md is based on [this template](https://github.com/othneildrew/Best-README-Template) by [Othneil Drew](https://github.com/othneildrew).

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/EOEPCA/rm-harvester.svg?style=flat-square
[contributors-url]: https://github.com/EOEPCA/rm-harvester/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/EOEPCA/rm-harvester.svg?style=flat-square
[forks-url]: https://github.com/EOEPCA/rm-harvester/network/members
[stars-shield]: https://img.shields.io/github/stars/EOEPCA/rm-harvester.svg?style=flat-square
[stars-url]: https://github.com/EOEPCA/rm-harvester/stargazers
[issues-shield]: https://img.shields.io/github/issues/EOEPCA/rm-harvester.svg?style=flat-square
[issues-url]: https://github.com/EOEPCA/rm-harvester/issues
[license-shield]: https://img.shields.io/github/license/EOEPCA/rm-harvester.svg?style=flat-square
[license-url]: https://github.com/EOEPCA/rm-harvester/blob/master/LICENSE
[build-shield]: https://www.travis-ci.com/EOEPCA/rm-harvester.svg?branch=master
