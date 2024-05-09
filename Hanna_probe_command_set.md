COMMANDS REQUIRING AN ANSWER
The instrument will answer for these commands with:
<STX> <answer> <checksum> <ETX>
where the checksum is the bytes sum of the answer string sent as 2 ASCII characters.
All the answer messages are with ASCII characters.
RAS Causes the instrument to send a complete set of readings in according with the current
range:
• pH, temperature and mV reading on pH range.
The answer string contains:
• Meter mode (2 chars):
• 00 ‑ pH range (0.001 resolution)
• 01 ‑ pH range (0.01 resolution)
• 02 ‑ pH range (0.1 resolution)
• 03 ‑ mV range
• Meter status (2 chars of status byte): represents a 8 bit hexadecimal
encoding.
• 0x10 ‑ temperature probe is connected
• 0x01 ‑ new GLP data available
• 0x02 ‑ new SETUP parameter
• 0x04 ‑ out of calibration range
• 0x08 ‑ the meter is in autoend point mode
40 PC INTERFACE
PAR Requests the setup parameters setting.
The answer string contains:
• Instrument ID (4 chars)
• Calibration Alarm time out for pH (2 chars)
• SETUP information (2 chars): 8 bit hexadecimal encoding.
• 0x01 ‑ beep ON (else OFF)
• 0x04 ‑ degrees Celsius (else degrees Fahrenheit)
• 0x08 ‑ Offset calibration (else Point calibration)
• Reading status (2 chars): R ‑ in range, O ‑ over range, U ‑ under range. First
character corresponds to the primary reading. Second character corresponds to
mV reading.
• Primary reading (corresponding to the selected range) ‑ 11 ASCII chars, includ‑
ing sign and decimal point and exponent.
• Secondary reading (only when primary reading is not mV) ‑ 7 ASCII chars,
including sign and decimal point.
• Temperature reading ‑ 7 ASCII chars, with sign and two decimal points, always
in °C.
