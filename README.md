![](https://img.shields.io/badge/python-v3.13.1-brightgreen)
![](https://img.shields.io/badge/fastapi-latest-blue)
![](https://img.shields.io/badge/mongo-latest-blue)
![](https://img.shields.io/badge/docker%20compose-v3-2FBAE0)


# edX IDSA Provider Use Case API
This is an API able to store IDSA-compliant contract information, to ensure proper supply of data to a Sovity consumer.

## Pre-Requisites 
* **System requirements**: 
  * 2 vCPUs
  * 4 GB RAM
  * 60 GB Storage
  * Ubuntu 20.04+ LTS Virtual Machine

* **System software requirements**: 
  * Git 
  * Docker
  * Docker-compose

### Run API
Before running this API, you must create an .env file, based on the .env.template file, available in edx_ux_api/src. Further detailing can be found in said file.

After doing so, the API is ready to run. To do so, go to edx_ux_api/src folder, then type in the command line:
```
docker-compose up --build
```
To stop the project, simply type:
```
docker-compose down
```
The edX IDSA Provider Use Case API should now be available. To access the API, simply type http://localhost:6200/ on your preferred browser.

## Maintainers
**Bruno Santos** - Design & Development - bruno-g-santos@alticelabs.com

## License
This module is distributed under [Apache 2.0 License](LICENSE) terms.