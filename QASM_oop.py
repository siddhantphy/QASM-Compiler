from time import time
import numpy as np
import functools as ft
import random

class QASM_compiler():

    def __init__(self, file_p: str):
        self.qasmfile = file_p
        self.time: int
        self.nq: int
        self.state = {}
        self.gates = {}
        self.measurements = {}

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

    def idle(self):
        id = np.identity(2)
        idle_nop = list(range(self.nq))

        for i in list(range(self.nq)):
                idle_nop[i] = id
            
        nop = ft.reduce(lambda x, y: np.kron(x, y), idle_nop)
        return nop

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

    def CX(self, control, target):
        pass

    def CZ(self, control, target):
        pass


    def H(self, qubit):
        id = np.identity(2)
        h =(1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
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
    @property
    def current_state(self):
        return self.current_state

    @current_state.setter
    def current_state(self):
        self.current_state = self.state[self.state.keys()[-1]]
        return self.current_state
     
    def initialize_register(self):
        qubits = 0
        for op in range(len(self.read_circuit)):
            if self.read_circuit[op][0] == 'qubit':
                qubits += 1
        self.nq = qubits

        self.read_circuit = self.read_circuit[qubits:]
        self.time = self.time - qubits
        return


    def quantum_operations(self):
        for op in range(len(self.read_circuit)):
            if self.read_circuit[op][0] == 'nop':
                self.gates[f't{op}'] = self.idle()

            if self.read_circuit[op][0] == 'cnot':
                control = int(list(self.read_circuit[op][1])[0])
                target = int(list(self.read_circuit[op][1])[-1])
                self.gates[f't{op}'] = self.CNOT(control, target)

            if self.read_circuit[op][0] == 'h':
                self.gates[f't{op}'] = self.H(int(list(self.read_circuit[op][1])[-1]))

            if self.read_circuit[op][0] == 'x':
                self.gates[f't{op}'] = self.X(int(list(self.read_circuit[op][1])[-1]))

            if self.read_circuit[op][0] == 'y':
                self.gates[f't{op}'] = self.Y(int(list(self.read_circuit[op][1])[-1]))

            if self.read_circuit[op][0] == 'z':
                self.gates[f't{op}'] = self.Z(int(list(self.read_circuit[op][1])[-1]))

            if self.read_circuit[op][0] == 's':
                self.gates[f't{op}'] = self.S(int(list(self.read_circuit[op][1])[-1]))

            if self.read_circuit[op][0] == 'measure':
                self.gates[f't{op}'] = int(list(self.read_circuit[op][1])[-1])

            if self.read_circuit[op][0] == 'c-x':
                self.gates[f't{op}'] = int(list(self.read_circuit[op][1])[-1])
            

    def circuit_simulate(self):
        self.state['t-1'] = np.zeros(2**self.nq)
        self.state['t-1'][0] = 1

        for op in range(len(self.read_circuit)):
            if self.read_circuit[op][0] == 'nop':
                self.state[f't{op}'] = np.matmul(self.idle(), self.state[f't{op-1}'])
            elif self.read_circuit[op][0] == 'cnot':
                control = int(list(self.read_circuit[op][1])[0])
                target = int(list(self.read_circuit[op][1])[-1])
                self.state[f't{op}'] = np.matmul(self.CNOT(control, target), self.state[f't{op-1}'])
            elif self.read_circuit[op][0] == 'h':
                self.state[f't{op}'] = np.matmul(self.H(int(list(self.read_circuit[op][1])[-1])), self.state[f't{op-1}'])
            elif self.read_circuit[op][0] == 's':
                self.state[f't{op}'] = np.matmul(self.S(int(list(self.read_circuit[op][1])[-1])), self.state[f't{op-1}'])
            elif self.read_circuit[op][0] == 'x':
                self.state[f't{op}'] = np.matmul(self.X(int(list(self.read_circuit[op][1])[-1])), self.state[f't{op-1}'])
            elif self.read_circuit[op][0] == 'y':
                self.state[f't{op}'] = np.matmul(self.Y(int(list(self.read_circuit[op][1])[-1])), self.state[f't{op-1}'])
            elif self.read_circuit[op][0] == 'z':
                self.state[f't{op}'] = np.matmul(self.Z(int(list(self.read_circuit[op][1])[-1])), self.state[f't{op-1}'])
            elif self.read_circuit[op][0] == 'measure':
                _temp_msr = self.measure(int(list(self.read_circuit[op][1])[-1]), op)
            elif self.read_circuit[op][0] == 'c-x':
                control = int(list(self.read_circuit[op][1])[0])
                target = int(list(self.read_circuit[op][1])[-1])
                msre = self.measure(control, op)
                if msre == 1:
                    self.state[f't{op}'] = np.matmul(self.X(int(list(self.read_circuit[op][1])[-1])), self.state[f't{op-1}'])
                else:
                    self.state[f't{op}'] = self.state[f't{op-1}']
            elif self.read_circuit[op][0] == 'c-z':
                control = int(list(self.read_circuit[op][1])[0])
                target = int(list(self.read_circuit[op][1])[-1])
                msre = self.measure(control, op)
                if msre == 1:
                    self.state[f't{op}'] = np.matmul(self.Z(int(list(self.read_circuit[op][1])[-1])), self.state[f't{op-1}'])
                else:
                    self.state[f't{op}'] = self.state[f't{op-1}']


    def measure(self, qubit, time):
        ele0 = np.array([[1, 0], [0, 0]])
        ele1 = np.array([[0, 0], [0, 1]])
        id = np.identity(2)

        ele0n = list(range(self.nq))
        ele1n = list(range(self.nq))
        
        for i in list(range(self.nq)):
            if i == qubit:
                ele0n[i] = ele0
                ele1n[i] = ele1
            else:
                ele0n[i] = id
                ele1n[i] = id
       
        ele0_n = ft.reduce(lambda x, y: np.kron(x, y), ele0n)
        ele1_n = ft.reduce(lambda x, y: np.kron(x, y), ele1n)

        self.state[list(self.state.keys())[-1]]


        prob_0 = np.sqrt(np.dot(self.state[list(self.state.keys())[-1]], np.matmul(ele0_n, self.state[list(self.state.keys())[-1]])))
        prob_1 = np.sqrt(np.dot(self.state[list(self.state.keys())[-1]], np.matmul(ele1_n, self.state[list(self.state.keys())[-1]])))
        weights = [prob_0, prob_1]

        pick = int((random.choices([0, 1]), weights)[0][0])

        if pick == 0:
            post_measure = np.matmul(ele0_n,self.state[list(self.state.keys())[-1]])
        elif pick == 1:
            post_measure = np.matmul(ele1_n,self.state[list(self.state.keys())[-1]])
        
        post_measure = post_measure / np.linalg.norm(post_measure)

        self.measurements[f'q{qubit}'] = weights[pick]
        self.state[f't{time}'] = post_measure

        return pick



    def visualize(self):
        pass
