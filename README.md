# file-name-obfuscator.

An app to recursively obfuscate the file names in a directory. Should have docker installed.

# Run Quick:
```bash
# Encode:
docker-compose run --build --rm -v "/tmp/:/workarea/src_dir" app python main.py encode src_dir manifest.json

# Decode:
docker-compose run --build --rm -v "/tmp/:/workarea/src_dir" app python main.py decode src_dir manifest.json-YYYYmmDDHHMMSS

```

# Run manually:
```bash
$ docker-compose run --build --rm -v "/tmp/:/workarea/src_dir" app

# within docker container, run the following commands:

# Obfuscate
$ python main.py encode ./src_dir ./manifest.json

# Un-obfuscate
$ python main.py decode ./src_dir ./manifest.json

# outside the docker container:
$ docker-compose down
```

# Run VSCode within Docker Container:

Uncomment the commented Volume in docker-compose.yaml. Change `/tmp/` to point to the correct source directory.

```yaml
version: "3.8"

services:
  app:
    build: .
    volumes:
      - ./:/workarea/
      # - /tmp/:/workarea/src_dir/
```
Then run VScode: "Reopen in container".