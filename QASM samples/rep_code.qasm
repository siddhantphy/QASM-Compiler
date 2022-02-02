#
# File:   rep_code.qasm
# Date:   02-Feb-22
# Author: Siddhant and Matthew
#
#
    qubit 	q0
    qubit 	q1
	qubit 	q2

	h	q0
	cnot	q0,q1
	cnot	q0,q2	# encoding
	x 	q1 	# bit flip Error
	cnot	q0,q1   # Z1 stabilizer  
	cnot    q1,q2   # Z2 stabilizer 
	cnot    q1,q0 	# decoding
	cnot    q2,q0 
	measure	q0