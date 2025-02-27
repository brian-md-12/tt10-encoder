/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_priority_encoder(
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs (wire)
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Generate priority output using a function and continuous assignment
    assign uo_out = priority_encode({ui_in, uio_in});

    function automatic [7:0] priority_encode(input [15:0] In);
        begin
            priority_encode = 8'b11110000; // Default output when all inputs are 0
            if (In[15]) priority_encode = 8'd15;
            else if (In[14]) priority_encode = 8'd14;
            else if (In[13]) priority_encode = 8'd13;
            else if (In[12]) priority_encode = 8'd12;
            else if (In[11]) priority_encode = 8'd11;
            else if (In[10]) priority_encode = 8'd10;
            else if (In[9])  priority_encode = 8'd9;
            else if (In[8])  priority_encode = 8'd8;
            else if (In[7])  priority_encode = 8'd7;
            else if (In[6])  priority_encode = 8'd6;
            else if (In[5])  priority_encode = 8'd5;
            else if (In[4])  priority_encode = 8'd4;
            else if (In[3])  priority_encode = 8'd3;
            else if (In[2])  priority_encode = 8'd2;
            else if (In[1])  priority_encode = 8'd1;
            else if (In[0])  priority_encode = 8'd0;
        end
    endfunction

    // Assign unused outputs to 0
    assign uio_out = 0;
    assign uio_oe  = 0;

    // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
