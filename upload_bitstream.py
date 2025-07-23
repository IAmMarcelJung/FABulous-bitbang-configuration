#!/usr/bin/env python3

from modules.board import Board
from modules.helpers import load_config, file_exists


def run():
    config_file = "config.json"
    if not file_exists(config_file):
        print(f"Configuration file '{config_file}' not found. Please create it.")
        return

    config = load_config(config_file)

    board = Board(
        fpga_sclk=17,
        fpga_sdata=18,
    )

    bitstream_file = config.get("bitstream_file")

    if not bitstream_file:
        print("Missing 'bitstream_file' in config.")
        return

    board.transmit_bitstream(bitstream_file)
    board.disable_bitbang()
