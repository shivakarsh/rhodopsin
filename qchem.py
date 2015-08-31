import re


class PDBATOM:
        resname=""
        chain=""
        pdbname=""
        resno=""
	atomname=""
        def __init__(self,mystring):
                self.resname=mystring[0]
                self.chain=mystring[1]
                self.pdbname=mystring[2]
                self.resno=mystring[3]
		self.atomname=mystring[4]


class PDB:
	atom={}
	def __init__(self,filename):
		with open(filename,"r") as thisfile:
                        for line in thisfile.readlines():
				if(line[0:4]=="ATOM" or line[0:4]=="HETA"):
					now_atom=PDBATOM([line[17:20].strip(),line[21].strip(),line[12:16].strip(),line[22:26].strip(),line[76:78]])
					self.atom[now_atom.resname+"-"+now_atom.chain+"-"+now_atom.pdbname+"-"+now_atom.resno]=([line[30:38].strip(),line[38:46].strip(),line[46:54].strip()])
	

					
			
class G09:
	atom={}
	pdb_set=False
	def __init__(self,filename,atom=atom):
		 with open(filename,"r") as thisfile:
			for line in thisfile.readlines():
	         		atom_list=re.search("((?=.*[A-Z])(?!.*[%#])).*(?:[0-9]*\\.[0-9\\t]).*(?:[0-9]*\\.[0-9]).*",line)
	#			residue_list=re.search("(?<=[(])(.*)(?=[)])",atom_list.group(0))
				if atom_list!=None:
					residue_list=re.search("(?<=[(])(.*)(?=[)])",atom_list.group(0))
					if residue_list!=None:
						 if self.pdb_set==False:
						 	self.pdb_set=True
						 now_atom=PDBATOM([residue_list.group(0).split(",")[1].split("=")[1],residue_list.group(0).split(",")[2].split("=")[1].split("_")[1],residue_list.group(0).split(",")[0].split("=")[1],residue_list.group(0).split(",")[2].split("=")[1].split("_")[0],atom_list.group(0).replace("("+residue_list.group(0)+")","").strip().split(" ",1)[0]])
						 atom[now_atom.resname+"-"+now_atom.chain+"-"+now_atom.pdbname+"-"+now_atom.resno+"-"+now_atom.atomname]= ','.join([atom_list.group(0).split()[1],atom_list.group(0).split()[2],atom_list.group(0).split()[3]])

	def __add__(self,PDB):
		PDB.value=100


#M=PDB('1U19.pdb')
N=G09('c2h4.com')
#N+M

#print "\n".join(M.atom)
print "\n".join(N.atom)
print N.atom

