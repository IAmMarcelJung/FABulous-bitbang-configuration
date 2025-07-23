#!/usr/bin/env python3


from modules.board import Board


def run():
    board = Board(
        fpga_sclk=17,
        fpga_sdata=18,
    )

    board.transmit_bitstream("bitstream.bin")
    board.disable_bitbang()
