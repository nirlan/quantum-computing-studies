# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 17:27:57 2024

@author: nirlan
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

simulator = Aer.get_backend("aer_simulator")

circuit = QuantumCircuit(2, 2)

# Add a Hadamard gate on qubit 0
circuit.h(0)

# Add a CX (CNOT) gate on control qubit 0 and acting on qubit 1
circuit.cx(0, 1)

# Save the matrix of the circuit until this point
# Capture the transformation matrix until that point in the reversible
# transformations produced by gates
circuit.save_unitary()

# Compile the circuit
compiled_circuit = transpile(circuit, simulator)

# Run it on the simulator
job = simulator.run(compiled_circuit)

# Collect the results
result = job.result()

# Print the unitary matriz that have been saved earlier
# This matrix is the representation of circuit
print(result.get_unitary(circuit,3)) # 3 is the number of digits of precision

# Draw the circuit
circuit.draw(output="mpl")