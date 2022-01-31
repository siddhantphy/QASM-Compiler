import numpy as np

class QASM_compiler():
    
    def __init__(self, file_p: str):
        self.QASM_read(filepath=file_p)

    def QASM_read(self, filepath: str):
        self.read_circuit = open(filepath, 'r')
        self.read_circuit.read()


circuit1 = QASM_compiler("/QASM samples/test1.qasm")