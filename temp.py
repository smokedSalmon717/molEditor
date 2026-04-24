from pysmiles import read_smiles


smile = 'C1CC[13CH2]CC1C1CCCCC1'
mol = read_smiles(smile)

print(mol)

