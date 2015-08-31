#!/usr/bin/python
from chem import *

#Original PDB and modified Gaussian
M=PDB('1U19.pdb')
N=G09('ret_tddft.com')

#Gather coordinates from Gaussian file
L=M.filter("RET")
L.save("first.pdb")
L+=N
L.save("second.pdb")

