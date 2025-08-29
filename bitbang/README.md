# FABulous Bitbang Configuration

This repo contains files to configure an (e)FPGA created with
[FABulous](https://github.com/FPGA-Research/FABulous) using the custom bitbang
protocol.

## Prerequisites

First, you need a microcontroller which can run
[MicroPython](https://docs.microPython.org/en/latest/index.html). In the example
we use the [ESP32 WROOM](https://microPython.org/download/ESP32_GENERIC/).
Follow the instructions for you specific microcontroller. A list of all the
MicroPython ports can be found
[here](https://micropython.org/download/). To compile the Python
modules into MicroPython files, `mpy-cross` is used. The compiled files are
uploaded to the microcontroller using `mpremote`. Before installing these
requirements, we recommend creating a Python
[venv](https://docs.Python.org/3/library/venv.html). The requirements can then
be installed using the following command:

```bash
pip install -r requirements.txt
```

## Uploading the Bitstream

If you now have a board running MicroPython and installed all the required
tools, you are ready to upload a bitstream. For this, you only need to execute
the following command:

```bash
make upload
```

Make sure to update the pins for your specific board in `upload_bitstream.py`
and the path to your bitstream in `config.json`. 

> [!NOTE] 
> The code was only tested using the mentioned ESP32 WROOM module. While it
> should also work on other board once you adjust the pins, there could still be
> issues. If you run into any, please let us know!

