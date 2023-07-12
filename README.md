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
