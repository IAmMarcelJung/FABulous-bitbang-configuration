#!/usr/bin/env python3

import serial
import argparse
import os
import stat
import sys
from pathlib import Path
from loguru import logger

DEFAULT_BAUDRATE = 57600
DEFAULT_PORT = "/dev/ttyUSB0"


def setup_logger(verbosity: int) -> None:
    """
    Setup the logger.

    :param verbosity: The verbosity to use for logging.
    :type verbosity: int
    """
    # Remove the default logger to avoid duplicate logs
    logger.remove()
    logger.level("INFO", color="<green>")

    # Define logger format
    if verbosity >= 1:
        log_format = (
            "[<level>{level:}</level>]: "
            "<cyan>[{time:DD-MM-YYYY HH:mm:ss]}</cyan> | "
            "<green>[{name}</green>:<green>{function}</green>:<green>{line}]</green> - "
            "<level>{message}</level>"
        )
    else:
        log_format = "[<level>{level:}</level>]: <level>{message}</level>"

    # Add logger to write logs to stdout
    logger.add(sys.stdout, format=log_format, level="DEBUG", colorize=True)


def device_port_exists(port_path) -> bool:
    """
    Check if a given device port exists on Linux.

    :param port_path: The device port path (e.g., '/dev/ttyUSB0', 'ttyUSB0', '/dev/ttyACM0')
    :type port_path: str
    :return: True if the device port exists and is a character device, False otherwise
    :rtype: bool
    """

    logger.info("Checking device...")
    # Normalize the path - add /dev/ prefix if not present
    if not port_path.startswith("/dev/"):
        port_path = "/dev/" + port_path

    try:
        if not os.path.exists(port_path):
            return False

        # Get file status
        file_stat = os.stat(port_path)

        # Check if it's a character device
        return stat.S_ISCHR(file_stat.st_mode)

    except (OSError, IOError):
        # Handle permission errors or other OS-level issues
        return False


def read_bitstream_data(bitstream_file: str) -> bytearray:
    """Read the bitstream data from the specified file.

    :param bitstream_file: The bitstream file to be read.
    :type bitstream_file: str
    :return: The bitstream data read from the file.
    :rtype: bytearray
    """
    file = Path(bitstream_file)
    if not file.is_file():
        logger.error(
            f"File {bitstream_file} does not exist."
            + " Check for spelling and if a bitstream file was created."
        )
        raise FileNotFoundError

    with open(bitstream_file, "rb") as f:
        data = bytearray(f.read())

    return data


def upload_bitstream(bitstream_file: str, baudrate: int, port: str) -> None:
    """Upload the bitstream to the eFPGA.

    :param bitstream_file: The bitstream file to be uploaded.
    :type bitstream_file: str
    :param baudrate: The baudrate to be used for the upload.
    :type bitstream_file: str
    :param ftdi_name: The name of the FTDI chip to be used.
    :type bitstream_file: str
    """

    logger.info(f"Using device at {port}")

    data = read_bitstream_data(bitstream_file)

    logger.info("Uploading bitstream...")

    with serial.Serial(port, baudrate) as ser:
        ser.write(data)

    logger.info("Bitstream transmitted!")


def __parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments.

    :return: The arguments parsed from the command line.
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(prog="upload_bitstream.py")
    parser.add_argument(
        "bitstream_file", help="Specifies the bitstream file to be uploaded."
    )
    parser.add_argument(
        "-b",
        "--baudrate",
        help=f"Specifies the baudrate. Defaults to {DEFAULT_BAUDRATE} which is the eFPGAs"
        + " baud rate at 10 MHz in MPW-2.",
        type=int,
        default=DEFAULT_BAUDRATE,
    )
    parser.add_argument(
        "-p",
        "--port",
        help=f"Specifies the port. Defaults to {DEFAULT_PORT}",
        type=str,
        default=DEFAULT_PORT,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="count",
        help="Show detailed log information including function and line number",
    )
    args = parser.parse_args()
    return args


def device_port_exists(port_path) -> bool:
    """
    Check if a given device port exists on Linux.

    Args:
        port_path (str): The device port path (e.g., '/dev/ttyUSB0', 'ttyUSB0', '/dev/ttyACM0')

    Returns:
        bool: True if the device port exists and is a character device, False otherwise
    """

    try:
        # Check if the path exists
        if not os.path.exists(port_path):
            logger.error(
                f"Device port {port_path} does not exist. Please check the conneciton and make sure you selected the correct port."
            )
            return False

        # Get file status
        file_stat = os.stat(port_path)

        # Check if it's a character device (typical for serial ports)
        is_char_device = stat.S_ISCHR(file_stat.st_mode)
        if not is_char_device:
            logger.warning(f"Path {port_path} exists but is not a character device")

        return is_char_device
    except (OSError, IOError) as e:
        # Log the error and exit gracefully
        logger.error(f"Failed to access device port {port_path}: {e}")
        return False


def main() -> None:
    """The main function containing the application logic"""
    args = __parse_arguments()
    setup_logger(args.verbose)
    port = args.port
    if not device_port_exists(port):
        exit()
    upload_bitstream(args.bitstream_file, args.baudrate, port)


if __name__ == "__main__":
    main()
