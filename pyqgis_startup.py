import sys
try:
    import qgis.core
except ModuleNotFoundError:
    # when QGIS is installed using the OSGeo4W installer pyqgis is installed
    # in a specific folder (C:/OSGeo4W64/apps/qgis/python by default). So we
    # need to add that folder to sys.path prior to importing qgis.
    sys.path.extend(["C:/OSGeo4W64/apps/qgis/python", "C:/OSGeo4W64/apps/qgis-ltr/python"])
    import qgis.core
import yaml
import pathlib
import collections
import configparser
import PyQt5.QtCore


def main():
    application = qgis.core.QgsApplication.instance()
    applicationSettings = qgis.core.QgsSettings(
        application.organizationName(), application.applicationName()
    )
    globalSettingsPath = pathlib.Path(applicationSettings.globalSettingsPath())
    globalSettingsDirPath = globalSettingsPath.parent
    qgisConstrainedSettingsPath = globalSettingsDirPath / "qgis_constrained_settings.yml"

    if not qgisConstrainedSettingsPath.is_file():
        print("No file named {}".format(qgisConstrainedSettingsPath))
        return

    print("Load constrained settings from {}".format(qgisConstrainedSettingsPath))
    with open(str(qgisConstrainedSettingsPath)) as f:
        constrainedSettings = yaml.safe_load(f)

    userSettings = PyQt5.QtCore.QSettings()
    print("Process {}".format(userSettings.fileName()))

    propertiesToRemove = constrainedSettings.get("propertiesToRemove", {})
    for group, properties in propertiesToRemove.items():
        userSettings.beginGroup(group)
        if isinstance(properties, str):
            if properties == "*":
                userSettings.remove("")
        else:
            for prop in properties:
                userSettings.remove(prop)
        userSettings.endGroup()

    globalSettings = configparser.ConfigParser()
    with open(str(globalSettingsPath)) as f:
        globalSettings.read_file(f)

    propertiesToMerge = constrainedSettings.get("propertiesToMerge", {})
    for group, properties in propertiesToMerge.items():
        if not globalSettings.has_section(group):
            continue
        userSettings.beginGroup(group)
        for prop in properties:
            if not globalSettings.has_option(group, prop):
                continue
            userPropertyValues = userSettings.value(prop)
            if not userPropertyValues:
                continue
            globalPropertyValues = globalSettings.get(group, prop)
            globalPropertyValues = globalPropertyValues.split(",")
            globalPropertyValues = list(map(str.strip, globalPropertyValues))
            userPropertyValues = globalPropertyValues + userPropertyValues
            # remove duplicates
            userPropertyValues = list(collections.OrderedDict.fromkeys(userPropertyValues))
            userSettings.setValue(prop, userPropertyValues)
        userSettings.endGroup()


if __name__ == "__main__":
    main()
