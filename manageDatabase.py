from os import listdir, makedirs, system


def splitSDF(pfilin, kin, prout):

    filin = open(pfilin, "r")
    filinread = filin.read()
    l_sdf = filinread.split("$$$$\n")

    for sdf in l_sdf:
        try: nameChem = sdf.split(kin)[-1].split("\n")[1].lower().replace(" ", "")
        except: continue
        print nameChem
        pfilout = prout + nameChem + ".sdf"
        filout = open(pfilout, "w")
        filout.write(sdf)
        filout.close




def runAll(prin):
    lfilin = listdir(prin)
    for filin in lfilin :
        if filin.split(".")[-1] == "sdf":
            prout = prin + filin.split(".")[0] + "/"
            try: makedirs(prout)
            except: pass
            cmd = "./main.py -i " + prin + filin + " -t 1 -o " + prout + filin.split(".")[0]
            print cmd
            system(cmd)





####### MAIN ######
splitSDF("/home/aborrel/3D_model/database_approved/e-Drug3D_1822_v2.sdf", "> <name>", "/home/aborrel/3D_model/database_approved/e-Drug3D/")
runAll("/home/aborrel/3D_model/database_approved/e-Drug3D/")
