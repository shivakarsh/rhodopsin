import re


class PDBATOM:
        resname=""
        chain=""
        pdbname=""
        resno=""
	atomname=""
	hashkey=""
        def __init__(self,mystring):
                self.resname=mystring[0]
                self.chain=mystring[1]
                self.pdbname=mystring[2]
                self.resno=mystring[3]
		self.atomname=mystring[4]
		self.hashkey="-".join(mystring)
	
	#def __hash__(self):
	#	return(str(self))

class PDB:
        atom={}
	raw=""

	def separate_pdb(self,line):
		if(line[0:4]=="ATOM" or line[0:4]=="HETA"):
                	return(PDBATOM([line[17:20].strip(),line[21].strip(),line[12:16].strip(),line[22:26].strip(),line[76:78].strip()]))
		else:		
			return(None)
	
	def reconstruct(self):
                self.atom={}
                for line in self.raw.splitlines():
                         now_atom=self.separate_pdb(line)
                         if now_atom!=None:
                                self.atom[now_atom.resname+"-"+now_atom.chain+"-"+now_atom.pdbname+"-"+now_atom.resno+"-"+now_atom.atomname]=([line[30:38].strip(),line[38:46].strip(),line[46:54].strip()])
		

        def __init__(self,filename=None):
		if filename!=None:
	                with open(filename,"r") as thisfile:
        	                for line in thisfile.readlines():
					self.raw+=line
				self.reconstruct()
                                        #self.atom[now_atom]=([line[30:38].strip(),line[38:46].strip(),line[46:54].strip()])


	def real83(self,line):
		return(str("%8.3f"%float(line)))

        def __iadd__(self,G09):	
		raw1=""
		for line in self.raw.splitlines():
			new_line=line
			now_atom=self.separate_pdb(line)
			if now_atom!=None:
				if now_atom.hashkey in G09.atom:
					new_coordinates=G09.atom[now_atom.hashkey].split(",")
					new_line=line[:30]+self.real83(new_coordinates[0])+self.real83(new_coordinates[1])+self.real83(new_coordinates[2])+line[54:]

			raw1+=new_line+"\n"
		self.raw=raw1
		raw1=""
		self.reconstruct()
		return(self)


	def filter(self,what_to):
		 new_pdb=PDB()
		 what_to=what_to.upper()
		 size_comparison=len(what_to.split("-"))
		 for line in self.raw.splitlines():
                         now_atom=self.separate_pdb(line)
			 if now_atom!=None:
				 if "-".join(now_atom.hashkey.split("-")[0:size_comparison]).upper()==what_to:
					new_pdb.raw+=line+"\n"
		 return(new_pdb)


	def save(self,filename):
		text=open(filename,"w")
		text.write(self.raw)
		text.close()



class G09:
	atom={}
	raw=""
	pdb_set=False
	def __init__(self,filename):
		 with open(filename,"r") as thisfile:
			for line in thisfile.readlines():
	         		atom_list=re.search("((?=.*[A-Z])(?!.*[%#])).*(?:[0-9]*\\.[0-9\\t]).*(?:[0-9]*\\.[0-9]).*",line)
	#			residue_list=re.search("(?<=[(])(.*)(?=[)])",atom_list.group(0))
				if atom_list!=None:
					self.raw+=line	
					residue_list=re.search("(?<=[(])(.*)(?=[)])",atom_list.group(0))
					if residue_list!=None:
						 if self.pdb_set==False:
						 	self.pdb_set=True
						 now_atom=PDBATOM([residue_list.group(0).split(",")[1].split("=")[1],residue_list.group(0).split(",")[2].split("=")[1].split("_")[1],residue_list.group(0).split(",")[0].split("=")[1],residue_list.group(0).split(",")[2].split("=")[1].split("_")[0],atom_list.group(0).replace("("+residue_list.group(0)+")","").strip().split(" ",1)[0]])
						 self.atom[now_atom.resname+"-"+now_atom.chain+"-"+now_atom.pdbname+"-"+now_atom.resno+"-"+now_atom.atomname]= ','.join([atom_list.group(0).split()[1],atom_list.group(0).split()[2],atom_list.group(0).split()[3]])

						 #self.atom[now_atom]=','.join([atom_list.group(0).split()[1],atom_list.group(0).split()[2],atom_list.group(0).split()[3]])

	def __add__(self,PDB):
		PDB.value=100
