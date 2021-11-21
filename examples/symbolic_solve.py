import plotkit.plotkit as pk
from sympy import latex, Symbol

from symcircuit.bode import plot_system
from symcircuit.system import SymbolicSystem

#        ___     ___
#   .---|___|----UUU--o--------o----.
#   |     Z1      Z2  |        ^    |
#   |                 |        |   .|.
#  / \               ---       |   | |
# ( ~ )              --- Z3    Uo  | |Z4
#  \_/                |        |   '-'
#   |                 |        v    |
#   '-----------------o--------o----'

s = SymbolicSystem("""
# Nodes
io == i4
ii == i1
i1 == i2
i2 == i4 + i3
i3 + i4 == ii
# Circuits
ui + i1 Z1 + i2 Z2 + i3 Z3
-i3 Z3 + i4 Z4
# Elements
s == const
Z1 == R1
Z2 == s L2
Z3 == 1 / (s C3)
Z4 == Ro
R1 == const
Ro == const
L2 == const
C3 == const
# Inout
io == i4
uo == - i4 Z4
H == uo / ui
Ro -> oo
""")

# find transfer function
sol = s.focus("H")
transfer = sol["H"].collect(Symbol("s"))
print(transfer)

# plot parameterised transfer function
v = dict(
    R1=2,
    L2=100e-6,
    C3=220e-6,
)

fig = plot_system(transfer, 1, 50000, values=v, return_fig=True)
fig.suptitle("$" + latex(transfer) + "$")
pk.finalize(fig)
