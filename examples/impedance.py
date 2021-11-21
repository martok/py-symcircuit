from io import StringIO

import plotkit.plotkit as pk

from symcircuit.bode import plot_system
from symcircuit.spice import Circuit
from symcircuit.system import SymbolicSystem

circ = Circuit()
circ.parse_spice_netlist(StringIO(r"""
* examples\network1.asc
R1 N001 0 1k
R2 N002 0 3k
C1 N002 0 50µ
L1 N001 N002 120µ
V1 N001 0 AC 1
.ac dec 30 10 10000
.backanno
.end
"""))

# translate to equation system
s = SymbolicSystem(circ.to_system_description())

# Add "measurement" characteristics
s.extend(SymbolicSystem("""
Zsys == V1 / i_V1
"""))
print(s.info())

# find transfer function
impedance = s.focus("Zsys")["Zsys"]
print("System Impedance = ", impedance)

# plot parameterised transfer function
v = dict(
    R1=1e3,
    R2=3e3,
    C1=50e-6,
    L1=120e-6,
)
fig = plot_system(impedance, 10, 50000, values=v, amplitude_linear=True, return_fig=True)
pk.finalize(fig)