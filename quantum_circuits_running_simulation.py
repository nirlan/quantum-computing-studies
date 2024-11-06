# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 17:07:07 2024

@author: nirlan
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

# Prepare simulator
simulator = Aer.get_backend("aer_simulator")
# Create a 2 qubit Quantum Circuit. With 2 classical bits
# Classical bits are used to store results of measurements
circuit = QuantumCircuit(2, 2)

# Add a Hadamard gate on qubit 0
circuit.h(0)
# Add a CX (CNOT) gate on control qubit 0 and target qubit 1
circuit.cx(0, 1)
# Save current state vector to be retrieved later
circuit.save_statevector(label='v1')
# Measure the qubits and save to classical bits
circuit.measure([0,1], [0,1])

# Compile the circuit to simulator
compiled_circuit = transpile(circuit, simulator)
# Execute the circuit on the simulator, 1000 times
job = simulator.run(compiled_circuit, shots=1000)
# Get results
result = job.result()
# Get counts from results
counts = result.get_counts(compiled_circuit)
print("\nTotals for 00 and 11 are: ",counts)

# Plot the histogram of the results
plot_histogram(counts)

# Get state vector that was saved earlier
print(result.data(0)['v1'])

# Draw the circuit
circuit.draw(output="mpl")