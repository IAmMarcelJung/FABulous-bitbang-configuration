# UART

You can use `upload.py` to upload a bitstream over UART to a FABulous FPGA.
It was created using `argparse`, so for a full breakdown of the commands
simply use

```console
./upload.py -h
```

This is the general usage of the command:

```console
upload_bitstream.py [-h] [-b BAUDRATE] [-p PORT] [-v] bitstream_file
```

### Example Use Case

> [!IMPORTANT]
> Make sure to adjust the files to your local files.

Uploading a bitstream:

```console
./board.py -p /dev/ttyUSB0 bitstream.bin
```

This uses the default baudrate of 57600 Baud.
