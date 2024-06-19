# Arnos Home Assistant Add-on Repository

This is my repository containing all Home Assistant Add-ons I developed over time. Currently, there are two add-ons available:

## DWD Global Radiation API Server

This add-on is a prerequisite for my DWD Global Radiation Home Assistant Integration. It provides the necessary API services for the integration to work correctly. You can find more details in the [README](https://github.com/aschmere/dwd_global_rad_hass/blob/main/README.md).

The add-on uses a Python library to retrieve global radiation measurement and forecast data from the "Deutscher Wetterdienst" (DWD). For more information about the library, visit the [DWD Global Radiation repository](https://github.com/aschmere/dwd_global_radiation).

Originally, the plan was to interact with the Python library directly within the Home Assistant integration. However, as of June 2024, the Home Assistant Integration framework cannot install Python packages with complex requirements, like the `netCDF4` package, into its core Docker container. The `netCDF4` package is essential for processing the DWD data (see [netCDF4 documentation](https://unidata.github.io/netcdf4-python/)). By using an add-on, a separate Docker image can be created to fulfill all Python requirements.

## DWD Global Radiation API Server (Development)

This add-on is for personal experiments and testing/debugging. It is not recommended for productive use and will likely not work with the integration.

## Disclaimer

**DISCLAIMER:** This project is a private open-source project and is not affiliated with the German public meteorology service institute "Deutscher Wetterdienst" (DWD). However, it uses its publicly available data interfaces.


[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Faschmere%2Fhass_addon_test)



<!--

Notes to developers after forking or using the github template feature:
- While developing comment out the 'image' key from 'example/config.yaml' to make the supervisor build the addon
  - Remember to put this back when pushing up your changes.
- When you merge to the 'main' branch of your repository a new build will be triggered.
  - Make sure you adjust the 'version' key in 'example/config.yaml' when you do that.
  - Make sure you update 'example/CHANGELOG.md' when you do that.
  - The first time this runs you might need to adjust the image configuration on github container registry to make it public
  - You may also need to adjust the github Actions configuration (Settings > Actions > General > Workflow > Read & Write)
- Adjust the 'image' key in 'example/config.yaml' so it points to your username instead of 'home-assistant'.
  - This is where the build images will be published to.
- Rename the example directory.
  - The 'slug' key in 'example/config.yaml' should match the directory name.
- Adjust all keys/url's that points to 'home-assistant' to now point to your user/fork.
- Share your repository on the forums https://community.home-assistant.io/c/projects/9
- Do awesome stuff!
 -->

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
