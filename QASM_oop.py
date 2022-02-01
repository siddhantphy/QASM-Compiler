import numpy as np
import functools as ft
# from typing import list

class QASM_compiler():

    def __init__(self, file_p: str):
        self.qasmfile = file_p
        self.time: int
        self.nq: int
        self.operations: dict
        self.gates: dict

        # self.current_state: np.array

        self.qasm_read(self.qasmfile)
        self.parse_operations()
        self.initialize_register()

    """
    ==========================================================================================================
                                            Initialization of QASM
    ==========================================================================================================
    
    """    

    def qasm_read(self, filepath: str):
        with open(filepath, 'r') as file:
            self.read_circuit = file.readlines()
        file.close()
        return
    
    def parse_operations(self):
        ''' Cleans up the strings line by line and parses to the computable form.'''
        for op in range(len(self.read_circuit)):
            self.read_circuit[op] = self.read_circuit[op].replace("\t", " ")
            self.read_circuit[op] = self.read_circuit[op].strip("\n") # Remove leading and trailing new line characters
            self.read_circuit[op] = self.read_circuit[op].split("#")[0] # Remove comments by splitting and selecting the first part
            self.read_circuit[op] = self.read_circuit[op].strip() # Remove all leading whitespaces

        self.read_circuit.remove("") # Remove all empty strings from the last version

        for op in range(len(self.read_circuit)):
            self.read_circuit[op] = self.read_circuit[op].split(" ") #Split with all white spaces between the string and take first and last element only
            self.read_circuit[op] = [self.read_circuit[op][0], self.read_circuit[op][-1]]

        for op in range(len(self.read_circuit)):
            if self.read_circuit[op] == ['', '']:
                self.read_circuit[op] = 'XXX'

        while 'XXX' in self.read_circuit:
            self.read_circuit.remove('XXX')

        self.time = len(self.read_circuit) # Number of time stamps for the quantum circuit

        for op in range(len(self.read_circuit)):
            self.read_circuit[op][-1] = self.read_circuit[op][-1].replace('q', '') # Remove the unecessary 'q' from the qubit labeling

    """
    ==========================================================================================================
                                            Quantum Gates
    ==========================================================================================================
    
    """

    def CNOT(self, control, target):
        id = np.identity(2)
        ele0 = np.array([[1, 0], [0, 0]])
        ele1 = np.array([[0, 0], [0, 1]])
        x = np.array([[0, 1], [1, 0]])
        
        first = list(range(self.nq))
        second = list(range(self.nq))

        for i in list(range(self.nq)):
            if i == control:
                first[i] = ele0
                second[i] = ele1
            elif i == target:
                first[i] = id
                second[i] = x
            else:
                first[i] = id
                second[i] = id
        
        first_n = ft.reduce(lambda x, y: np.kron(x, y), first)
        second_n = ft.reduce(lambda x, y: np.kron(x, y), second)

        cnot = first_n + second_n

        return cnot

        


    def H(self, qubit):
        id = np.identity(2)
        h =(1/np.sqrt(2)) * np.array([[1, 0], [0, -1]])
        hn = list(range(self.nq))
        
        for i in list(range(self.nq)):
            if i == qubit:
                hn[i] = h
            else:
                hn[i] = id
       
        h_n = ft.reduce(lambda x, y: np.kron(x, y), hn)

        return h_n

    def X(self, qubit):
        id = np.identity(2)
        x = np.array([[0, 1], [1, 0]])
        xn = list(range(self.nq))
        
        for i in list(range(self.nq)):
            if i == qubit:
                xn[i] = x
            else:
                xn[i] = id
       
        x_n = ft.reduce(lambda x, y: np.kron(x, y), xn)

        return x_n


    def Y(self, qubit):
        id = np.identity(2)
        y = np.array([[0, 0 - 1j], [0 + 1j, 0]])
        yn = list(range(self.nq))
        
        for i in list(range(self.nq)):
            if i == qubit:
                yn[i] = y
            else:
                yn[i] = id
       
        y_n = ft.reduce(lambda x, y: np.kron(x, y), yn)
        
        return y_n

    def Z(self, qubit):
        id = np.identity(2)
        z = np.array([[1, 0], [0, -1]])
        zn = list(range(self.nq))
        
        for i in list(range(self.nq)):
            if i == qubit:
                zn[i] = z
            else:
                zn[i] = id
       
        z_n = ft.reduce(lambda x, y: np.kron(x, y), zn)

        return z_n

    def S(self, qubit):
        id = np.identity(2)
        s = np.array([[1, 0], [0, 0 + 1j]])
        sn = list(range(self.nq))
        
        for i in list(range(self.nq)):
            if i == qubit:
                sn[i] = s
            else:
                sn[i] = id
       
        s_n = ft.reduce(lambda x, y: np.kron(x, y), sn)

        return s_n

    """
    ==========================================================================================================
                                            Circuit Simulation functions
    ==========================================================================================================
    
    """ 
     
    def initialize_register(self):
        qubits = 0
        for op in range(len(self.read_circuit)):
            if self.read_circuit[op][0] == 'qubit':
                qubits += 1
        self.nq = qubits

        self.read_circuit = self.read_circuit[qubits:]
        self.time = self.time - qubits
        return

    def gates(self):
        pass

    def simulate_circuit(self):
        

    def measure(self):
        pass

    def visualize(self):
        pass




circuit1 = QASM_compiler("QASM samples/test3.qasm")
print(circuit1.read_circuit)
print(circuit1.time)

# print(circuit1.CNOT(1,0))