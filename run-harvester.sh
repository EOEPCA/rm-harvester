#!/bin/sh

echo "Running harvester" >&2

harvester daemon \
    --config-file /config.yaml \
    --host ${REDIS_HOST} \
    --port ${REDIS_PORT} \
    --listen-queue ${REDIS_HARVESTER_QUEUE_KEY} \
