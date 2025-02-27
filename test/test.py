# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_priority_encoder(dut):
    """Test the priority encoder functionality with edge cases."""

    dut._log.info("Starting priority encoder test")

    # Define test cases: (ui_in, uio_in, expected uo_out)
    test_cases = [
        # Edge case 1: All zeros
        (0b00000000, 0b00000000, 0b11110000),  # ui_in = 00000000, uio_in = 00000000 → concatenated_input = 00000000_00000000 → special case
        # Edge case 2: Single 1 at MSB
        (0b10000000, 0b00000000, 0b00001111),  # ui_in = 10000000, uio_in = 00000000 → concatenated_input = 10000000_00000000 → first 1 at bit 15
        # Edge case 3: Single 1 at LSB
        (0b00000000, 0b00000001, 0b00000000),  # ui_in = 00000000, uio_in = 00000001 → concatenated_input = 00000000_00000001 → first 1 at bit 0
        # Edge case 4: Single 1 at bit 7
        (0b00000000, 0b10000000, 0b00000111),  # ui_in = 00000000, uio_in = 10000000 → concatenated_input = 00000000_10000000 → first 1 at bit 7
        # Edge case 5: All ones
        (0b11111111, 0b11111111, 0b00001111),  # ui_in = 11111111, uio_in = 11111111 → concatenated_input = 11111111_11111111 → first 1 at bit 15
        # Edge case 6: Alternating 1s and 0s
        (0b10101010, 0b10101010, 0b00001111),  # ui_in = 10101010, uio_in = 10101010 → concatenated_input = 10101010_10101010 → first 1 at bit 15
        # Edge case 7: Single 1 in the middle
        (0b00000000, 0b00010000, 0b00000100),  # ui_in = 00000000, uio_in = 00010000 → concatenated_input = 00000000_00010000 → first 1 at bit 4
        # Edge case 8: Multiple 1s with the first 1 at bit 12
        (0b00010000, 0b00010000, 0b00001100),  # ui_in = 00010000, uio_in = 00010000 → concatenated_input = 00010000_00010000 → first 1 at bit 12
        # Edge case 9: Input with x (unknown) values
        (BinaryValue("xxxxxxxx", 8), BinaryValue("xxxxxxxx", 8), None),  # ui_in = xxxxxxxx, uio_in = xxxxxxxx → concatenated_input = xxxxxxxx_xxxxxxxx → unresolved output
    ]

    for ui_in, uio_in, expected in test_cases:
        # Set inputs ui_in and uio_in
        dut.ui_in.value = ui_in
        dut.uio_in.value = uio_in

        # Wait for 10 time units to ensure values settle
        await Timer(10, units="ns")

        # Check expected output
        if dut.uo_out.value.is_resolvable:
            assert dut.uo_out.value.integer == expected, (
                f"Priority encoder failed: ui_in = {ui_in:08b}, uio_in = {uio_in:08b}, "
                f"uo_out = {dut.uo_out.value.integer:08b}, expected = {expected:08b}"
            )
        else:
            dut._log.error(f"Unresolvable output: uo_out = {dut.uo_out.value.binstr}")

    dut._log.info("Priority encoder test completed successfully")
