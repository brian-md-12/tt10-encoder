# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_priority_encoder(dut):
    """Test the priority encoder functionality for all possible input cases."""

    dut._log.info("Starting exhaustive priority encoder test")

    # Iterate through all 16-bit input combinations (0 to 65535)
    for i in range(65536):
        # Split the 16-bit input into ui_in (upper 8 bits) and uio_in (lower 8 bits)
        ui_in = (i >> 8) & 0xFF  # Upper 8 bits
        uio_in = i & 0xFF        # Lower 8 bits

        # Set inputs ui_in and uio_in
        dut.ui_in.value = ui_in
        dut.uio_in.value = uio_in

        # Wait for 10 time units to ensure values settle
        await Timer(10, units="ns")

        # Calculate the expected output
        expected_output = 0b11110000  # Default output (all zeros)
        for bit in range(15, -1, -1):
            if (i >> bit) & 1:
                expected_output = bit
                break

        # Check if the output matches the expected value
        if dut.uo_out.value.is_resolvable:
            assert dut.uo_out.value.integer == expected_output, (
                f"Priority encoder failed: input = {i:016b}, "
                f"uo_out = {dut.uo_out.value.integer:08b}, "
                f"expected = {expected_output:08b}"
            )
        else:
            dut._log.error(f"Unresolvable output: uo_out = {dut.uo_out.value.binstr}")

    dut._log.info("All 65,536 test cases passed!")
