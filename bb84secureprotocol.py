# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 14:21:24 2024

@author: nirlan
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

simulator = Aer.get_backend("aer_simulator")

# Compute a random bit to send
randomBitCircuit = QuantumCircuit(1,1)
randomBitCircuit.x(0)
randomBitCircuit.barrier()
randomBitCircuit.h(0)
randomBitCircuit.barrier()
randomBitCircuit.measure(0,0)

# Get a random classical bit
randomBitCompiledCircuit = transpile(randomBitCircuit, simulator)
job = simulator.run(randomBitCompiledCircuit, shots = 1)
result = job.result()
counts = result.get_counts(randomBitCompiledCircuit)
if("1" in counts.keys()):
    bitToSend = 1
else:
    bitToSend = 0

print("Bit to send = " + str(bitToSend))

# Compute a random encoding basis to use for sending (polarization angle)
randomSendBasisCircuit = QuantumCircuit(1,1)
randomSendBasisCircuit.x(0)
randomSendBasisCircuit.barrier()
randomSendBasisCircuit.h(0)
randomSendBasisCircuit.barrier()
randomSendBasisCircuit.measure(0,0)

randomSendBasisCompiledCircuit = transpile(randomSendBasisCircuit, simulator)
job = simulator.run(randomSendBasisCompiledCircuit, shots = 1)
result = job.result()
counts = result.get_counts(randomSendBasisCompiledCircuit)
if("1" in counts.keys()):
    # 45 degrees polarization
    sendBasis = 1
else:
    # horizontal/vertical polarization
    sendBasis = 0

print("Send basis = " + str(sendBasis))

# Compute a random basis to use for receiving (receiver guessing basis)
randomRecvCircuit = QuantumCircuit(1,1)
randomRecvCircuit.x(0)
randomRecvCircuit.barrier()
randomRecvCircuit.h(0)
randomRecvCircuit.barrier()
randomRecvCircuit.measure(0,0)

randomRecvBasisCompiledCircuit = transpile(randomRecvCircuit, simulator)
job = simulator.run(randomRecvBasisCompiledCircuit, shots = 1)
result = job.result()
counts = result.get_counts(randomRecvBasisCompiledCircuit)
if("1" in counts.keys()):
    # 45 degrees guessing
    recvBasis = 1
else:
    # horizontal/vertical guessing
    recvBasis = 0

print("Receive basis = " + str(recvBasis))    

# Quantum Send
# This circuit of one qubit acts as the photon that is transferred
commCircuit = QuantumCircuit(1,1)
if(bitToSend == 1):   # if bit to send equals one
    commCircuit.x(0)  # set qubit to one, otherwise remain zero
                     
    
if(sendBasis == 1):   # if sending basis equal to 45 degrees
    commCircuit.h(0)  # change basis

# Quantum Receive
if(recvBasis == 1):  # if receiver basis (guessed) is 45 degrees
    commCircuit.h(0) # HH = I. So this will reverse the Hadamard gate.
commCircuit.measure(0,0)

# This is an equivalent circuit to a polarized photon being sent from Alice to Bob
commCompiledCircuit = transpile(commCircuit, simulator)
job = simulator.run(commCompiledCircuit, shots = 1)
result = job.result()
counts = result.get_counts(commCompiledCircuit)

if("1" in counts.keys()):
    recvBit = 1
else:
    recvBit = 0
    
# If the basis are te same, the received bit should be the same
if(sendBasis == recvBasis):
    print("Sent bit = " + str(bitToSend) + " Received bit = " + str(recvBit))
else:
    print("Bit was lost because basis dind't match")
    

