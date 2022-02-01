#
# File:   test3.qasm
# Date:   22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - simple teleportation circuit
#
    qubit 	q0
    qubit 	q1
	qubit 	q2

	h	q1	# create EPR pair
	cnot	q0,q1
	cnot	q0,q2	# encoding 
	cnot	q0,q1   # Z1 stabilizer  
	cnot    q1,q2   # Z2 stabilizer 
	cnot    q1,q0 	# decoding
	cnot    q2,q0 
	measure	q0