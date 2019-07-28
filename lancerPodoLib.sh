#!/bin/sh
APP_ROOT=$(dirname $(readlink -fm $0))
python3.6 "$APP_ROOT"
