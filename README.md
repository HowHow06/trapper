# To setup this app:

## Build the extension app

1. Run the docker compose.

```sh
docker compose build extension-app-build
```

2. The extension package zip will be available in `extension-vite/package` directory. Unzip it and load it from browser.

## Run the app with docker compose

1. Use the command below:

```sh
docker compose up
```

2. Wait for it to complete. Then visit

- Console panel: `http://localhost:3000` (might take a few minutes to load for the first time)
- Backend API: `http://localhost:8000`
- XSSHunter Probe: `http://localhost:55000`
- RabbitMQ web: `http://localhost:15672`

---

To run the mariadb:

```bash
docker compose up -d db
```

```bash
docker compose down db
docker compose down --volumes
```

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
