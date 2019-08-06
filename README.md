# **py_sensirion_sps30_logger**

## Introduction

**py_sensirion_sps30_logger** is a Python package containing a data logging application for the [Sensirion SPS30 particulate matter sensor](https://www.sensirion.com/en/environmental-sensors/particulate-matter-sensors-pm25). **py_sensirion_sps30_logger** works well on Raspberry Pi systems. 

The low-level functions used to interface with the sensor were developed by Szymon Jakubiak and are available in the [**Python-Sensirion-SPS30**](https://github.com/dobra-dobra/Python-Sensirion-SPS30) repository. 

## Installation

Use pip to install this package from GitHub: 

```
# First, install a dependency
pip install git+https://github.com/skgrange/pys_logging_helpers

# Then install the py_sensirion_sps30_logger package, this may need sudo to 
# install a system programme at `usr/local/bin`
pip install git+https://github.com/skgrange/py_sensirion_sps30_logger
```

## Usage

  1. Ensure your user can read and write to serial ports by being in the `dialout` user group:

  ```
  # Add user to dialout group, change user_name to your user
  adduser user_name dialout
  # Usually need to log out and back in for this change to be applied
  ```

  2. Connect the sensor with the USB/serial converter and determine where the device is located: 
  
  ```
  # Find tty devices
  dmesg | grep tty
  ```
  
  The sensor will usually be located at `/dev/ttyUSB0`. 

  3. Install the **pys_logging_helpers** and **py_sensirion_sps30_logger** packages with **pip**. 

  4. Run the logging application from the terminal (this system programme is installed by **pip**): 
  
  ```
  # Start data logging
  # It is usually be a good idea to set the output directory with the -o argument
  log_sensirion_sps30_sensor -o ~/Desktop/data
  ```
  
  If the sensor is not located at `/dev/ttyUSB0`, use the `-d` argument to change the location. Likewise, use the `-tz` argument to alter the time zone the dates will be formatted to in the logged files: 
  
  ```
  # Start some logging with some options
  log_sensirion_sps30_sensor -o ~/Desktop/data -d /dev/ttyUSB1 -tz Europe/Zurich
  ```
