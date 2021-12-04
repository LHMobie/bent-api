# Bent Token Supply API
Python/Hug api tp report on max, current, and (calculated) circulating supplies

### Important files:
- `api.py` - Main API endpoint logic
- `config.ini` - Configurations for API
- `bent_abi.json` - Bent token contract abi
- `Dockerfile` - Docker container build config
- `requirements.txt` - Pip3 module installation
- `build_api_container_local.sh` - Bash shell script to build api container

## Build Instructions
(**IMPORTANT** - Requires python v3.8 or higher)

### Local - Dev mode
- (recommended) Create local environment with virtualenv
- Clone this repository to local drive
- Install python packages - `pip3 install -r requirements.txt`
- Start api - `hug -f api.py`
- View api in browser - `http://127.0.0.1:8000`

### Using Docker
- Clone this repository to local drive
- Build container with local script - `./build_api_container_local.sh`
- Start container - `docker run --name bent-api --network=host -p 8000:8000/tcp -d bent-api:latest`
- View api in browser - `http://127.0.0.1:8000`

## Notes
- Depending on your deployment stack, you may need to update the build script to tag the container for storage in a git registry
- Using `--network-host` when running the container will discard public port mappings
- The httpprovider keys in the config.ini should be updated to use your own infura account key.