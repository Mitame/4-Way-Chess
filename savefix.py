import pickle,os
version = "001"
directory = "TESTSAVE001"
pickle.dump(version, open(os.path.join("saves",directory,"version.txt"),"wb"))