#!/usr/bin/env bash

docker run --rm --network container:postgres_aws \
    --volume $(pwd)/src/metadata/schemacrawler_entrypoint.sh:/bin/schemacrawler_entrypoint.sh \
    --volume $(pwd)/metadata/generated/:/share \
    -w="/schemacrawler" \
    sualeh/schemacrawler \
    /bin/sh -c "/bin/schemacrawler_entrypoint.sh"
