# RealityConvert #
##################
@uthor: Alexandre Borrel
Contact: aborrel[at]ncsu.edu 
https://www.fourches-laboratory.com/
Date: 03-21-2017

RealityConvert is a software tool, which allows users to easily convert molecular
objects (stored as pdb or sdf files) to high quality 3D models directly 
compatible for AR and VR applications. For chemical structures, in addition to
the 3D model generation, RealityConvert also generates image trackers, useful to
universally call and anchor that particular 3D model when used in various AR
applications.


### Dependencies  ###
#####################

Developed and tested on linux (Ubuntu 16.04) 

Requirements (Ubuntu 16.04): 
- Blender 2.76
- pymol 1.7.x
- molconvert (Marvin Beans suite Chemaxon)
- Open Babel 2.4.1

Python (2.7) modules:
- optparse
- os
- zipfile
- pymol
- bpy (Blender)
- sys
- shutil

### Scripts .py descriptions  ###
#################################

- realityconvert.py: MAIN including pymol processing
- command3D.py: script used by blender to convert WRL


## additional files ##
######################

- README.md: readme file
- aspirin.sdf: example of sdf input file
- aspirin.wrl: example of wrl input file

## command lines ##
###################

1. With wrl file
- ./realityconvert.py -w aspirin.wrl -o aspirin3D

2. With a sdf or a pdb file
./realityconvert.py -i aspirin.sdf -o model3D

3. With tracker
./realityconvert.py -i aspirin.sdf -t 1 -o model3D


