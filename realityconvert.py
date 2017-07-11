#!/usr/bin/env python

import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI

from optparse import OptionParser
from os import system, listdir, path, remove
import zipfile

import pymol


def runBlender(pwrml, pout):

    cmd = "/home/aborrel/softwares/blender-2.76b-linux-glibc211-x86_64/blender --background --python command3D.py -- " + str(pwrml) + " " + str(pout)
    print "Run blender - wrml"
    print "blender2.76 --background --python command3D.py " + str(pwrml.split("/")[-1]) + " " +  str(pout.split("/")[-1])
    print "tmp folder:" + str(pwrml.split("/")[-2]) 
    system(cmd)
    print cmd

    lfilout = [path.dirname(pout) + "/" + i for i in listdir(path.dirname(pout))]
    #print lfilout

    ppng = pout + ".png"
    pobj = pout + ".obj"
    pmtl = pout + ".mtl"
    pstl = pout + ".stl"

    if not ppng in lfilout or not pobj in lfilout or not pmtl in lfilout:
        print "ERROR -> BLENDER CONVERSION - Check the WRML file"
        return []

    else:
        pzip = pout + ".zip"
        zipmodel = zipfile.ZipFile(pzip, "w")
        zipmodel.write(ppng, arcname=ppng.split("/")[-1])
        zipmodel.write(pobj, arcname=pobj.split("/")[-1])
        zipmodel.write(pmtl, arcname=pmtl.split("/")[-1])
        zipmodel.close()
	
        pzipstl = pout + "_stl.zip"
        zipmodel = zipfile.ZipFile(pzipstl, "w")
        zipmodel.write(ppng, arcname=ppng.split("/")[-1])
        zipmodel.write(pstl, arcname=pstl.split("/")[-1])
        zipmodel.close()
        return [pobj, pmtl, pstl, ppng, pzip, pzipstl]



def PDBtoWRL(pfilinPDB, pfilout, pseopt = 0):

    pfilinWRL = pfilout + ".wrl"

    pymol.finish_launching()

    pymol.cmd.load(pfilinPDB, "lig")
    pymol.cmd.hide(representation="line")
    pymol.cmd.show(representation="stick")
    pymol.cmd.show(representation="spheres")
    pymol.cmd.set("valence", 1)
    pymol.cmd.set("stick_radius", 0.25)
    pymol.cmd.set("sphere_scale", 0.30)
    pymol.cmd.color("cyan", "elem c")
    pymol.cmd.save(pfilinWRL)
    if pseopt == 1:
        pymol.cmd.save(pfilinPDB[:-4] + ".pse")
        pymol.cmd.save(pfilinPDB[:-4] + ".png")
    pymol.cmd.quit()

    return pfilinWRL



def main(clean=1):

    use = "%prog [-i file .pdb or .sdf] [-w file in wrml] [-o path out name] [-t tracker option (default = 0)] [-h help]\n\n" \
          "Dependencies: \n" \
          "- Blender 2.76\n" \
          "- pymol 1.7.x\n" \
          "- molconvert (Marvin Beans suite Chemaxon)\n" \
          "- Open Babel 2.4.1" \
          "\n\n" \
          "Exemples:\n" \
          "1. With wrl file\n" \
          "- ./realityconvert.py -w myfile.wrl -o model3D\n\n" \
          "2. With a sdf or a pdb file\n" \
          "./realityconvert.py -i myligand.sdf -o model3D\n" \
          "./realityconvert.py -i myligand.pdb -o model3D\n\n" \
          "3. With tracker\n" \
          "./realityconvert.py -i myligand.pdb -t 1 -o model3D\n\n"
    parser = OptionParser(usage=use)


    parser.add_option("-i","--input", dest="pfilin", default="0", help="File of structure in .pdb or .sdf format")
    parser.add_option("-w","--wrl", dest="pwrl", default="0", help="wrl file only for model conversion")
    parser.add_option("-o","--output", dest="pout", default="0", help="Name and path for output 3D object")
    parser.add_option("-t", "--tracker", dest="trackers", default="0", help="Equal 1, tracker in .jpeg is generated "
                                                                            "based on SMILES code")


    (options, args) = parser.parse_args()

    pfilin = options.pfilin
    pwrl = options.pwrl
    pout = options.pout
    trackers = options.trackers

    #absolute path
    pfilin = path.abspath(pfilin)
    pout = path.abspath(pout)

    if pout == "0":
        print "ERROR -> Use a correct output file"
        return

    # case if WRML is im input
    if pwrl != "0":
        lfilout = runBlender(pwrl, pout)
        if len(lfilout) == 4:
            print "Model 3D is generated -> " + lfilout[-1]
            if clean == 1:
                remove(lfilout[0])
                remove(lfilout[1])
                remove(lfilout[2])
                remove(lfilout[3])
            return
        else:
            print "ERROR -> No model 3D generated, please check your input files and paths"

    elif pfilin != "0":
        print "File in:" + pfilin.split("/")[-1]

        filetype = path.splitext(pfilin)[1]
        print "File type:", filetype
        if filetype != ".sdf" and filetype != ".pdb":
            print "ERROR -> File type in input not supported, please use pdb or sdf format"
            return



        # convert PDB to WRL
        pwrl = PDBtoWRL(pfilin, pout)
        lfilout = runBlender(pwrl, pout)
        if len(lfilout) == 4:
            print "Model 3D is generated -> " + lfilout[-1]
            if clean == 1:
                remove(lfilout[0])
                remove(lfilout[1])
                remove(lfilout[2])
                remove(lfilout[3])
        else:
            print "ERROR -> No model 3D generated, please check your input files and paths"
            return

    if trackers != "0":
        # convert in SMILES (lost 3D structure)
        psmiles = pfilin[:-4] + ".smi"
        cmdToSMILES = "babel " + pfilin + " " + psmiles
        system(cmdToSMILES)

        # general
        cmdMoldConvert = "molconvert \"jpeg:w500,Q95,#ffffff\" " + path.abspath(psmiles) + " -o " + path.abspath(pout) + "_tracker.jpeg"
        print "molconvert \"jpeg:w500,Q95,#ffffff\" " + psmiles.split("/")[-1] + " -o " + pout.split("/")[-1] + "_tracker.jpeg"
        system(cmdMoldConvert)
        if clean == 1:
            remove(path.abspath(psmiles))

main()




