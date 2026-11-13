import json
import math
import re
import sys
from pathlib import Path

position = {'X': None, 'Y': None, 'Z': None}
arcs = []
for line_number, line in enumerate(Path(sys.argv[1]).read_text().splitlines(), 1):
    code = line.split(';', 1)[0].strip()
    if not code:
        continue
    op = code.split()[0]
    values = {key: float(value) for key, value in re.findall(r'([XYZIJPR])(-?(?:\d+(?:\.\d*)?|\.\d+))', code)}
    if op == 'G91':
        raise RuntimeError('Relative XYZ requires a separate oracle')
    if op in ('G2', 'G3') and values.get('P') == 1 and 'I' in values and 'J' in values:
        assert position['X'] is not None and position['Y'] is not None
        x = position['X'] + values['I']
        y = position['Y'] + values['J']
        radius = math.hypot(values['I'], values['J'])
        bounds = [x-radius, y-radius, x+radius, y+radius]
        inside = bounds[0] >= 0.5 and bounds[1] >= 1 and bounds[2] <= 270.5 and bounds[3] <= 271
        arcs.append({'line': line_number, 'bounds': bounds, 'inside': inside})
    if op in ('G0', 'G1', 'G2', 'G3', 'G92'):
        position.update({key: value for key, value in values.items() if key in position})
bad = [arc for arc in arcs if not arc['inside']]
print(json.dumps({'file': str(Path(sys.argv[1])), 'spiral_count': len(arcs), 'outside_count': len(bad), 'examples': bad[:3]}, indent=2))
assert not bad, 'Spiral lift leaves the configured printable polygon'
