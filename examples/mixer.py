#!/usr/bin/python

# WARNING: This syntax is still in flux and very much subject to change. Don't
# rely on this being stable until we've at least built out an alpha!


# perhaps these three are automatic in the IDE?
from autopcb import * # connect(), Net, units
from autopcb.board import Board
from autopcb.schematic import Schematic

from autopcb.components.electronics import LM358, ICL7660
from autopcb.components.connectors import MiniatureStereoPhone, USBC2
from autopcb.components.sound import LinearDualChannelVariableResistor6044Something
from autopcb.components.basic import Resistor, Capacitor
from autopcb.nets import Net, Ground

NUM_INPUTS=4
NUM_OUTPUTS=4

# all units are millimeters
board = Board(width=85, height=120)

# Power
power_in = USBC2()
connect(power_in.pin(1), Net("5V"))
connect(power_in.pin(1), Ground)
# class Coords: def Coords(x_pos: float, y_pos: float, rotation: float)
# TODO: this gets placed over the inputs/outputs
board.place(power_in, Coords(0,0,0 * units.PI)) # def place(Coords) -> None: # We could get PI out of math, but we already usually have units imported? /shrug

# -5V generation
inverter = ICL7660()
inverter.style = "SMT" # Should this be an enum somewhere?
inverter.datasheet = "http://bourns.com/docs/Product-Datasheets/PTB.pdf" # This and the following two could be common to all components?
inverter.manufacturer = "Bourns"
inverter.cost = 4.95 # BOM?
cap1 = Capacitor(10 * units.MICROFARAD, max_voltage=25 * units.VOLT)
connect(inverter.pin(1), None) # This pin intentionally left empty; this can also be left implicit, though maybe that's a warning?
connect(inverter.pin(2), cap1.pin(1)) # connect pin 2 to cap1's pin 1
connect(inverter.pin(3), Ground)
connect(inverter.pin(4), cap1.pin(2))
cap2 = Capacitor(10 * units.MICROFARAD)
connect(inverter.pin(5), cap2.pin(1))
connect(inverter.pin(5), Net("-5V")) # Net is sort of a singleton-ish thing?
connect(cap2.pin(2), Ground)
connect(inverter.pin(6), Ground)
connect(inverter.pin(7), None)
connect(inverter.pin(8), Net("5V")) # Nets get "re-declared for use"? Not sure exactly how this would work
board.place_wherever(inverter, cap1, cap2) # def place_wherever(...component: autopcb.Component) -> Coords: # This sounds hard

for channel_id in range(NUM_INPUTS):
    input = MiniatureStereoPhone()

    input_x_free = board.width - (NUM_INPUTS + NUM_OUTPUTS)*input.width
    input_padding = input_x_free / (NUM_INPUTS + NUM_OUTPUTS + 1)
    input_coords = Coords()
    input_coords.x = padding + (input.width + padding) * channel_id
    input_coords.y = board.height - input.height + 2 * units.MILLIMETER # sticks 2mm off the top of the board
    board.place(input, input_coords)

    connect(input.pin(1), Ground)
    left_r = Resistor(10 * units.KILOHM, 0.125 * units.WATT)
    right_r = Resistor(10 * units.KILOHM, 0.125 * units.WATT)
    connect(input.pin(2), left_r.pin(1))
    connect(input.pin(3), right_r.pin(1))

    op_amp = LM358()
    slider = LinearDualChannelVariableResistor6044Something()

    left_output_r = Resistor(10 * units.KILOHM, 0.125 * units.WATT)
    connect(op_amp.pin(1), left_output_r.pin(1))
    connect(left_output_r.pin(2), Net("Intermediate_Left_Channel"))
    connect(op_amp.pin(1), slider.pin(1))
    connect(op_amp.pin(2), left_r.pin(2))
    connect(op_amp.pin(2), slider.pin(slider.WIPER_1)) # We can have constants here, I suppose? Static, I guess.
    connect(op_amp.pin(3), Ground)

    right_output_r = Resistor(10 * units.KILOHM, 0.125 * units.WATT)
    connect(op_amp.pin(5), right_output_r.pin(1))
    connect(right_output_r.pin(2), Net("Intermediate_Right_Channel"))
    connect(op_amp.pin(5), slider.pin(slider.CCW_2))
    connect(op_amp.pin(6), right_r.pin(2))
    connect(op_amp.pin(6), slider.pin(slider.WIPER_2)) # We can have constants here, I suppose? Static, I guess.
    connect(op_amp.pin(7), Ground)

    connect(op_amp.pin(4), Net("-5V"))
    connect(op_amp.pin(8), Net("5V"))

    op_amp_x_free = board.width - (NUM_INPUTS + 1) * slider.width
    op_amp_padding = board_x_free / NUM_INPUTS+2
    op_amp_x_pos = padding + (slider.width + padding) * channel_id
    op_amp_y_pos = padding # origin at bottom left, unlike EasyEDA
    board.place(op_amp, Coords(board_x_pos, board_y_pos, 0 * units.PI)) # Is there a way we can see if the input was multiplied by PI?

# Output Amp

op_amp = LM358()
slider = LinearDualChannelVariableResistor6044Something()

connect(op_amp.pin(1), Net("Left_Out"))
connect(op_amp.pin(1), slider.pin(1))
connect(op_amp.pin(2), Net("Intermediate_Left_Channel"))
connect(op_amp.pin(2), slider.pin(slider.WIPER_1)) # We can have constants here, I suppose? Static, I guess.
connect(op_amp.pin(3), Ground)

connect(op_amp.pin(5), Net("Right_Out"))
connect(op_amp.pin(5), slider.pin(slider.CCW_2))
connect(op_amp.pin(6), Net("Intermediate_Right_Channel"))
connect(op_amp.pin(6), slider.pin(slider.WIPER_2)) # We can have constants here, I suppose? Static, I guess.
connect(op_amp.pin(7), Ground)

connect(op_amp.pin(4), Net("-5V"))
connect(op_amp.pin(8), Net("5V"))

op_amp_x_free = board.width - (NUM_INPUTS + 1) * slider.width
op_amp_padding = board_x_free / NUM_INPUTS+2
op_amp_x_pos = padding + (slider.width + padding) * channel_id
op_amp_y_pos = padding # origin at bottom left, unlike EasyEDA
board.place(op_amp, Coords(board_x_pos, board_y_pos, 0 * units.PI)) # Is there a way we can see if the input was multiplied by PI?

# Outputs
for output_id in range(NUM_OUTPUTS):
    output = MiniatureStereoPhone()
    connect(output.pin(1), Ground)
    connect(output.pin(2), Net("Left_Out"))
    connect(output.pin(3), Net("Right_Out"))

    output_x_free = board.width - (NUM_INPUTS + NUM_OUTPUTS)*output.width
    output_padding = input_x_free / (NUM_INPUTS + NUM_OUTPUTS + 1)
    output_coords = Coords()
    output_coords.x = padding + (output.width + padding) * output_id + NUM_INPUTS
    output_coords.y = board.height - output.height + 2 * units.MILLIMETER # sticks 2mm off the top of the board
    board.place(output, output_coords)

board.render()
