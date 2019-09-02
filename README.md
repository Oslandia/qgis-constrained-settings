# Constraining user settings

This repo shows how to constrain user settings using a QGIS Startup Script. Constrained user
settings are settings that users cannot freely set or override.

The startup script is `pyqgis_startup.py`. And the path to this script is to be specified with the
`PYQGIS_STARTUP` environment variable. For example:

```sh
$ PYQGIS_STARTUP=/home/user/pyqgis_startup.py qgis
```

QGIS will execute that script at startup time, and when switching profiles. The script is
responsible for rewriting the user settings based on the constraints defined in the "user settings
contraints" file.

The "user settings contraints" file is a YAML file that must be named
`qgis_constrained_settings.yml` and located in the same folder as that containing the global
settings file (`qgis_global_settings.ini`).

Note: the startup script won't be able to find the "user settings contraints" file and the file name
is not `qgis_contrained_settings.yml` or if the file is not located in the same directory as the
global settings file.

Here is an example of a `qgis_constrained_settings.yml` file:

```yaml
---
propertiesToRemove:
  proxy:
  - authcfg
  - proxyEnabled
  - proxyExcludeUrls
  - proxyHost
  - proxyPassword
  - proxyPort
  - proxyType
  - proxyUser
propertiesToMerge:
  svg:
  - searchPathsForSVG
```

The section `propertiesToRemove` includes the properties that will be removed from the user settings
by the startup script. The first level, `proxy` in the above example, defines the group that
includes the properties.

The section `propertiesToMerge` includes the properties whose values will be merged with the values
defined in the global settings by the startup script. For example if `searchPathsForSVG` is set to
`/usr/qgis/svg` in the user settings and to `/global/qgis/svg` in the global settings then the
startup script will change the `searchPathsForSVG` to `/global/qgis/svg, /usr/qgis/svg` in the user
settings. The startup script will also remove duplicates.

Notes:

* The path to the startup script (specified with the `PYQGIS_STARTUP` environment variable) must be
  absolute for QGIS to be able to execute this script when switching profiles.
* The `PYQGIS_STARTUP` environment variable must be defined in a QGIS startup script (see
  [qgis.sh](qgis.sh) in this repo for an example), at a system level in a global manner, or in the
  global settings file (with `customEnvVars` in the `qgis` section).
* In this repo the `PYQGIS_STARTUP` environment variable is defined in the [qgis.sh](qgis.sh) script
  rather than in the global settings to avoid hard-coding the path to the script in the global
  settings.