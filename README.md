# Spiral lift boundary regression

Public synthetic fixture only. No customer models, printer connection, or private presets.

`spiral-boundary.3mf` is a 269.6 x 269.6 x 0.8 mm rectangle on the U1 printable polygon X=0.5..270.5, Y=1..271. Spiral lift is 0.4 mm with a 3 degree travel slope. All four nozzle offsets are zero in this end-to-end fixture; nonzero offsets are covered by the C++ tests.

The PNGs are real, unchanged 1200 x 800 window captures after Slice plate, using the U1 0.4 mm profile, Generic PLA and the factory Textured PEI selection. Before: official Snapmaker Orca 2.4.1. After: main 6245898ef plus the fix in ea1867cd67. The screenshots prove the warning state only; UI styling and estimate differences may come from the version change. Both versions' original GCodeWriter sources are identical before the fix.

The native CLI uses the embedded Cool Steel Plate configuration. On this fixture, official 2.4.1 emits 6 spiral circles, 5 crossing the configured boundary. The fixed build emits 1 spiral circle, entirely inside. The other 5 use a vertical Z lift. No physical print was run.

`audit_spirals.py FILE.gcode` independently checks the emitted full-circle G2/G3 P1 bounds against the fixture's bed polygon. It supports absolute XYZ and zero nozzle offsets only; this is a fixture-specific oracle, not a general printer safety validator. It exits nonzero on an out-of-bounds circle.

The source PR adds 10 C++ cases (217 assertions), including all four tools and edges, plate origins, nonzero nozzle offsets, partial offset vectors, inward circles, concave and clockwise beds, rounding clearance, large lifts, and tiny travel slopes.
