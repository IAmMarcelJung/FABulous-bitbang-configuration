#!/usr/bin/env python3

from machine import Pin
from modules.helpers import file_exists

BITS_IN_BYTE = 8
BITS_IN_WORD = 32
BYTES_IN_WORD = 4


class Board:
    def __init__(
        self,
        fpga_sclk="IO_10",
        fpga_sdata="IO_11",
    ):
        self.fpga_sclk = Pin(fpga_sclk, mode=Pin.OUT, value=0)
        self.fpga_sdata = Pin(fpga_sdata, mode=Pin.OUT, value=0)

    def bitbang(self, data: bytes, ctrl_word: int) -> None:
        """Transmit data using a custom bitbang protocol.

        :param data: The data to be transmitted.
        :ctrl_word: The control word to be used for the transmission.
        """
        for byte_pos, byte in enumerate(data):
            for bit_pos in range(BITS_IN_BYTE):
                self.fpga_sdata.value((byte >> ((BITS_IN_BYTE - 1) - bit_pos)) & 0x1)
                self.fpga_sclk.value(1)
                self.fpga_sdata.value(
                    (
                        ctrl_word
                        >> (
                            (BITS_IN_WORD - 1)
                            - (BITS_IN_BYTE * (byte_pos % BYTES_IN_WORD) + bit_pos)
                        )
                    )
                    & 0x1
                )
                self.fpga_sclk.value(0)
            if (byte_pos % 100) == 0:
                print("{}".format(byte_pos))
        self.fpga_sclk.value(0)
        self.fpga_sdata.value(0)

    def disable_bitbang(self):
        """Disable bitbang by sending the control word FAB0."""
        ctrl_word = 0x0000FAB0
        data = bytes(0)
        self.bitbang(data, ctrl_word)

    def transmit_bitstream(self, bitstream_file: str) -> None:
        """Transmit the bitstream to the FPGA.

        :param bitstream_file: The file containing the bitstream to be transmitted.
        :type bitstream_file:
        """
        # Set the control word to enable bitbang
        ctrl_word = 0x0000FAB1

        data = bytes()

        if file_exists(bitstream_file):
            with open(bitstream_file, mode="rb") as f:
                data += f.read()
            self.bitbang(data, ctrl_word)
        else:
            print(
                f"File {bitstream_file} not found. Please add it or change the path to the file."
            )
