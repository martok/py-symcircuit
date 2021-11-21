from io import StringIO

import plotkit.plotkit as pk
from sympy import latex

from symcircuit.bode import plot_system
from symcircuit.spice import *
from symcircuit.system import SymbolicSystem

circ = Circuit()
circ.parse_spice_netlist(StringIO(r"""
* netlist from LTSpice
V1 N001 0 SINE() AC 1
Rin Vli 0 10000k
C1 N003 0 220µ
R1 Vlo N002 2
L1 N002 N003 100µ
Rout Vlo N001 1
L2 N003 Vli 50µ
C2 Vli 0 110µ
.ac dec 20 10 50000
.backanno
.end
"""))

# Visualise the equivalent graph
fig, ax = pk.new_regular(1, 1)
Circuit.draw_graph(circ.to_graph(), ax)
pk.finalize(fig)

# translate to equation system
scr = circ.to_system_description()
s = SymbolicSystem(scr)

# Add "measurement" characteristics
s.extend(SymbolicSystem("""
Rin -> oo
ui == V1
uo == Rin i_Rin
H == uo / ui
"""))
print(s.info())

# find transfer function
sol = s.focus("H")
transfer = sol["H"].collect(Symbol("s"))
print(transfer)

# plot parameterised transfer function
v = dict(
    Rout=1,
    R1=2,
    L1=100e-6,
    C1=220e-6,
    L2=50e-6,
    C2=110e-6,
)
fig = plot_system(transfer, 1, 50000, values=v, return_fig=True)
fig.suptitle("$" + latex(transfer) + "$")
pk.finalize(fig)
