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
python3 main.py @ mysubdomain mysecondsubdomain
```

#### Docker Compose example

You can also use docker compose for easy deployment. Make sure the image was built using the command explained in step 2
.

If you named your image differently, make sure to change it in the compose file

```yaml
version: '3.7'

services:
  app:
    image: luatan/dyndnschecker
    container_name: dynDNSChecker
    environment:
      - API_KEY=<your_key>
      - DOMAIN=<your_domain>
    #command: python3 main.py @ mysubdomain # uncomment, if you need multiple subdomains checked

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