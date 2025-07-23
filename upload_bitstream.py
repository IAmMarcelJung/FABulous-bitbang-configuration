#!/usr/bin/env python3

from modules.board import Board
from modules.helpers import load_config, file_exists, validate_config


KEY_BITSTREAM_FILE = "bitstream_file"
KEY_FPGA_SCLK = "fpga_sclk"
KEY_FPGA_SDATA = "fpga_sdata"

CONFIG_SCHEMA = {
    KEY_BITSTREAM_FILE: str,
    KEY_FPGA_SCLK: int,
    KEY_FPGA_SDATA: int,
}

CONFIG_FILE = "config.json"


def run():
    if not file_exists(CONFIG_FILE):
        print(f"Configuration file '{CONFIG_FILE}' not found. Please create it.")
        return
    try:
        config = load_config(CONFIG_FILE)
        validate_config(config, CONFIG_SCHEMA)

        bitstream_file = config.get(KEY_BITSTREAM_FILE)
        fpga_sclk = config.get(KEY_FPGA_SCLK)
        fpga_sdata = config.get(KEY_FPGA_SDATA)

    except (KeyError, ValueError) as e:
        print(f"Configuration error: {e}")
        return

    board = Board(
        fpga_sclk=fpga_sclk,
        fpga_sdata=fpga_sdata,
    )

    board.transmit_bitstream(bitstream_file)
    board.disable_bitbang()
