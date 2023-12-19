# file-name-obfuscator.

An app to recursively obfuscate the file names in a directory.

Currently Designed to run within a Docker container. Follow steps to execute:

In order to setup a source folder, you'll need to load that as a Docker Volume as follows:

```yaml
version: "3.8"

services:
  dev:
    build: .
    volumes:
      - ./:/workarea/
      - ~/Downloads/Folder_to_rename/:/workarea/src_dir/
```

```bash
$ docker-compose run dev

# within docker container, run the following commands:

# Obfuscate
$ python main.py encode ./src_dir ./manifest.json

# Un-obfuscate
$ python main.py decode ./src_dir ./manifest.json

# outside the docker container:
$ docker-compose down
```