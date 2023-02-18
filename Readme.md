# DynDNSChecker

Small python program to periodically check if the public ip address has changed since the last check.
If it has changed it updates the dns records on Cloudflare.

## Usage

### Docker

1. Clone the repository
2. navigate into the directory and run ``docker build . -t luatan/dyndnschecker``
3. run the container with

```bash
docker run -d -e API_KEY=<your_key> -e DOMAIN=<your_domain> luatan/dyndnschecker
```
if you need not only the root record to be updated, you can override the start command like so:
```bash
docker run -d \
-e API_KEY=<your_key> \
-e DOMAIN=<your_domain> \
luatan/dyndnschecker \
@ mysubdomain mysecondsubdomain
```

#### Docker Compose example
The compose file builds the image directly.
You can either use the environment variables directly in the yaml file or you can mount
an .env file. In this example it uses the .env file which has to be created in the same
directory as the docker-compose.yaml file.

```yaml
version: '3.7'

services:
  app:
    image: luatan/dyndnschecker
    build: .
    container_name: dynDNSChecker
#    environment: # uncomment if you want to use specific env values
#      - API_KEY=${API_KEY}
#      - DOMAIN=${DOMAIN}
#      - INTERVAL=${INTERVAL}
    volumes: # or use a .env file on your filesystem as source of environment variables
      - .env:/.env
#    command: @ mysubdomain # uncomment, if you need multiple subdomains checked

```

### Without Docker

2. Clone the repository
3. Install dependencies with the following command: ``pip install -r requirements.txt``
4. export the required Environment variables (see below)
5. run ``python3 /src/main.py``

If no arguments are given, the script uses the root record. Which is
essentially the same as @ you only have to use @ in combination with other subdomains. If you want to update
multiple subdomains you can run the script like this ``python3 /src/main.py @ mysubdomain``

## Environment Variables

| Description                                                                             | key       | default value | required |
|-----------------------------------------------------------------------------------------|-----------|---------------|----------|
| API key of your provider (currently only Cloudflare supported)                          | API_KEY   | None          | yes      |
| The domain which should be checked                                                      | DOMAIN    | None          | yes      |
| Interval in seconds in which the ip address should be tested                            | INTERVAL  | 180           | no       |
| Sets the log level allowd values are <br/> - DEBUG<br/>- INFO<br/>- WARNING<br/>- ERROR | LOG_LEVEL | INFO          | no       |