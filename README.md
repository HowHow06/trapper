# Trapper: XSS Vulnerability Detection System

Trapper is an innovative Final Year Project (FYP) designed to enhance web security by identifying Cross-Site Scripting (XSS) vulnerabilities in web applications. This system integrates a browser extension with a back-end server to offer an efficient, passive black-box scanning technique capable of detecting three main types of XSS vulnerabilities. Aimed at security researchers, web developers, and cybersecurity enthusiasts, Trapper simplifies the process of securing web applications from one of the most common and perilous security threats today.

## Features

- **Passive Scanning**: Trapper passively scans web applications without disrupting their functionality, providing real-time insights.
- **Comprehensive Detection**: Capable of identifying reflected, stored, and DOM-based XSS vulnerabilities.
- **Browser Extension Integration**: Enhances user experience by integrating scanning capabilities directly into your browser.
- **Efficient Analysis**: Utilizes a novel black-box scanning technique for quick and efficient vulnerability detection.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose
- A modern web browser

### Build the extension

1. Run the docker compose.

```sh
docker compose build extension-app-build
```

2. The extension package zip will be available in `extension-vite/package` directory. Unzip it and load it from browser.

### Setup Guide

1. **Clone the Repository**

```bash
git clone https://github.com/HowHow06/trapper.git
cd trapper
```

2. **Environment Configuration**

Copy the `.env.sample` file to a new file named `.env` and update the environment variables according to your setup.

```bash
cp .env.sample .env
```

3. **Launch with Docker Compose**

Use Docker Compose to build and run the application components.

```bash
docker-compose up --build
```

Wait for it to complete. Then visit

- Console panel: `http://localhost:3000` (might take a few minutes to load for the first time)
- Backend API: `http://localhost:8000`
- XSSHunter Probe: `http://localhost:55000`
- RabbitMQ web: `http://localhost:15672`

4. **Install Browser Extension**

Navigate to the `extension-vite` directory and follow the instructions provided to install the Trapper browser extension into your web browser.

5. **Start Scanning**

With the back-end server running and the browser extension installed, navigate to your web application and start the passive scanning process to identify XSS vulnerabilities.

### To run the mariadb:

```bash
docker compose up -d db
```

```bash
docker compose down db
docker compose down --volumes
```

## Architecture

Trapper's architecture comprises two main components:

- **Browser Extension**: Facilitates the detection of XSS vulnerabilities directly from the user's browser, enhancing ease of use.
- **Back-End Server**: Processes data collected by the browser extension to identify potential XSS vulnerabilities efficiently.

## Troubleshooting & Useful Commands:

> https://markpatton.cloud/2020/08/12/error-when-running-docker-on-windows-after-install-fixed/

```powershell
cd "C:\Program Files\Docker\Docker" ; ./DockerCli.exe -SwitchDaemon
```

> Can add `-d` flag if you want

> Must use docker, because the env file is imported into docker and used by the app

```bash
docker compose build extension-app-dev
docker compose build extension-app-dev --no-cache
docker compose up extension-app-dev --build
docker compose up extension-app-dev
docker compose exec extension-app-dev yarn add formik


docker compose stop extension-app-dev
docker compose rm -v extension-app-dev
```

## Contributing

Your contributions are welcome! Whether you have a fix, improvement, or new feature suggestion, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
