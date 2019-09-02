#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PYQGIS_STARTUP=${SCRIPT_DIR}/pyqgis_startup.py qgis --globalsettingsfile ${SCRIPT_DIR}/qgis_global_settings.ini --profile test
