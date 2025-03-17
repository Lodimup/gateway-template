#! /bin/bash

PRE='export $(grep -v '\''^#'\'' '
POST='/.env | xargs)'
CMD=$PRE$1$POST
echo $CMD >> ~/.bashrc

apt update && apt install -y postgresql-client redis-tools
uv sync
