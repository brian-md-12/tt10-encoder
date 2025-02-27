/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_priority_encoder(
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    reg [7:0] uo_out_reg; // Intermediate register for uo_out
    always @(*) begin
        // Concatenate
         reg [15:0] In = {ui_in, uio_in};// Concatenated 16-bit input
        
        // Default output for all inputs 0
        uo_out_reg = 8'b11110000;

        // Priority encoding logic
        if (In[15]) uo_out_reg = 8'd15;
        else if (In[14]) uo_out_reg = 8'd14;
        else if (In[13]) uo_out_reg = 8'd13;
        else if (In[12]) uo_out_reg = 8'd12;
        else if (In[11]) uo_out_reg = 8'd11;
        else if (In[10]) uo_out_reg = 8'd10;
        else if (In[9]) uo_out_reg = 8'd9;
        else if (In[8]) uo_out_reg = 8'd8;
        else if (In[7]) uo_out_reg = 8'd7;
        else if (In[6]) uo_out_reg = 8'd6;
        else if (In[5]) uo_out_reg = 8'd5;
        else if (In[4]) uo_out_reg = 8'd4;
        else if (In[3]) uo_out_reg = 8'd3;
        else if (In[2]) uo_out_reg = 8'd2;
        else if (In[1]) uo_out_reg = 8'd1;
        else if (In[0]) uo_out_reg = 8'd0;
    end

  
  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = uo_out_reg; // Assign the intermediate register to the output wire
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
