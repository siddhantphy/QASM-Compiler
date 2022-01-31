import numpy as np
# from typing import list

class QASM_compiler():

    self.nq: int
    self.operations: dict

    def __init__(self, file_p: str):
        self.QASM_read(filepath=file_p)

    @property
    def read_circuit(self):
        return self.read_circuit

    @read_circuit.setter
    def QASM_read(self, filepath: str):
        self.read_circuit = open(filepath, 'r')
        self.read_circuit.read()

    def initialize_register(self):
        pass

    def gates(self):
        pass

    def simulate_circuit(self):
        pass

    def measure(self):
        pass

    def visualize(self):
        pass




circuit1 = QASM_compiler("/QASM samples/test1.qasm")