from QASM_oop import QASM_compiler

"""
==========================================================================================================
                                            Testing the QASM Files
==========================================================================================================
    
""" 
# circuit1 = QASM_compiler("QASM samples/test1.qasm")
# circuit1 = QASM_compiler("QASM samples/test2.qasm")
# circuit1 = QASM_compiler("QASM samples/test3.qasm")
# circuit1 = QASM_compiler("QASM samples/test4.qasm")
circuit1 = QASM_compiler("QASM samples/rep_code.qasm")

print("✵ The parsed quantum operations are: ",circuit1.read_circuit)
print("✵ Number of qubits: ",circuit1.nq)
print("✵ Total time steps for the hardware: ",circuit1.time)
circuit1.quantum_operations()
circuit1.circuit_simulate()
print("✵ Final state at the end of the circuit is: ", circuit1.state[list(circuit1.state.keys())[-1]])
print("✵ The measurement probability distribution is: ", circuit1.measurements)
print("✵✵✵✵✵✵✵✵✵✵✵✵✵✵✵✵✵✵✵")
print("✵ Chronological time evolution of the quantum circuit: \n", circuit1.state)
print("✵✵✵✵✵✵✵✵✵✵✵✵✵✵✵✵✵✵✵")

circuit1.visualize()

"""
==========================================================================================================
                                            Statistics
==========================================================================================================
    
""" 

# for itr in list(range(10)):
#     circuit1.circuit_simulate()