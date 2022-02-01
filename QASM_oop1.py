import numpy as np
import functools as ft
# from typing import list

class QASM_compiler():

    def __init__(self, file_p: str):
        self.qasmfile = file_p
        self.time: int
        self.nq: int
        self.operations: dict
        self.gates = {}

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

        # self.read_circuit.remove("") # Remove all empty strings from the last version

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


    def quantum_operations(self):
        for op in range(len(self.read_circuit)):
            if self.read_circuit[op][0] == 'nop':
                self.gates[f't{op}'] = self.nop()

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



    def simulate_circuit(self):
        start = np.zeros(2**self.nq)
        start[0] = 1


    def measure(self):
        pass


    def visualize(self):
        print(self.read_circuit,self.nq)
        with open('/home/matthew1303/Dropbox/PhD - TUDelft - MSteinberg/CodingClass(2022)/new_file.txt','w') as wr:
            wr.write("\\begin{quantikz}")
            for i in range(self.nq):
                wr.write("\n")
                wr.write("\\lstick{$\ket{0}$}")
                for l in range(len(self.read_circuit)):
                    if l == len(self.read_circuit)-1:
                        if self.read_circuit[l][0] == 'h':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\gate{H}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'x':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\gate{X}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'y':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\gate{Y}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'z':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\gate{Z}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 's':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\gate{S}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'cnot':
                            if self.read_circuit[l][1][0] == str(i):
                                lines_down = int(self.read_circuit[l][1][-1])
                                lines_down = lines_down - i 
                                wr.write(" & \\ctrl{%s}" % (int(lines_down)))
                            elif self.read_circuit[l][1][-1] == str(i):
                                wr.write(" & \\targ{}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'measure':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\meter{}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'c-x':
                            if self.read_circuit[l][1][0] == str(i):
                                lines_down = int(self.read_circuit[l][1][-1])
                                lines_down = lines_down - i 
                                wr.write(" & \\ctrl{%s}" % (int(lines_down)))
                            elif self.read_circuit[l][1][-1] == str(i):
                                wr.write(" & \\gate{c-x}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'c-z':
                            if self.read_circuit[l][1][0] == str(i):
                                lines_down = int(self.read_circuit[l][1][-1])
                                lines_down = lines_down - i 
                                wr.write(" & \\ctrl{%s}" % (int(lines_down)))
                            elif self.read_circuit[l][1][-1] == str(i):
                                wr.write(" & \\gate{c-z}")
                            else:
                                wr.write(" & \\qw")
                        else:
                            wr.write(" & \\qw")
                        wr.write(" \\\\")
                    else:
                        if self.read_circuit[l][0] == 'h':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\gate{H}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'x':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\gate{X}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'y':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\gate{Y}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'z':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\gate{Z}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 's':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\gate{S}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'cnot':
                            if self.read_circuit[l][1][0] == str(i):
                                lines_down = int(self.read_circuit[l][1][-1])
                                lines_down = lines_down - i 
                                wr.write(" & \\ctrl{%s}" % (int(lines_down)))
                            elif self.read_circuit[l][1][-1] == str(i):
                                wr.write(" & \\targ{}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'measure':
                            if self.read_circuit[l][1] == str(i):
                                wr.write(" & \\meter{}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'c-x':
                            if self.read_circuit[l][1][0] == str(i):
                                lines_down = int(self.read_circuit[l][1][-1])
                                lines_down = lines_down - i 
                                wr.write(" & \\ctrl{%s}" % (int(lines_down)))
                            elif self.read_circuit[l][1][-1] == str(i):
                                wr.write(" & \\gate{c-x}")
                            else:
                                wr.write(" & \\qw")
                        elif self.read_circuit[l][0] == 'c-z':
                            if self.read_circuit[l][1][0] == str(i):
                                lines_down = int(self.read_circuit[l][1][-1])
                                lines_down = lines_down - i 
                                wr.write(" & \\ctrl{%s}" % (int(lines_down)))
                            elif self.read_circuit[l][1][-1] == str(i):
                                wr.write(" & \\gate{c-z}")
                            else:
                                wr.write(" & \\qw")
                        else:
                            wr.write(" & \\qw")
            wr.write("\n")
            wr.write("\\end{quantikz}")

circuit1 = QASM_compiler("/home/matthew1303/Dropbox/PhD - TUDelft - MSteinberg/CodingClass(2022)/rep_code.qasm")
circuit1.visualize()
# print(circuit1.read_circuit)
# print(circuit1.time)
# circuit1.quantum_operations()
# print(circuit1.gates)