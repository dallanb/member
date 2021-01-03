#!/bin/bash

ssh -i /home/dallanbhatti/.ssh/github super_dallan@mega <<EOF
  docker exec member_db pg_dump -c -U "$1" member > member.sql
EOF
rsync -chavzP --stats --remove-source-files super_dallan@mega:/home/super_dallan/member.sql "$HUNCHO_DIR"/services/member/member.sql

docker exec -i member_db psql -U "$1" member <"$HUNCHO_DIR"/services/member/member.sql
