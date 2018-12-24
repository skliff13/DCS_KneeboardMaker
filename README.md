# DCS_KneeboardMaker

This tool allows generating kneeboard slides 
that can be used for navigation in Digital 
Combat Simulator (DCS) missions.

## Input data

First, let's consider what kind data must be prepared 
prior to using the scripts. 
Examples of the input data files are stored in 
`input_BurningSkies_Normandy/` directory.   

#### 1) High-resolution map of the region

Slides for the kneeboard will be extracted from the image
containing map of the region of interest. 
The map image must have sufficient resolution.
Such image can be made from in-game screenshots, 
or by scanning a vintage military map... 
It's up to the user.

Example (see file `stitched.png`, 2742 x 1544 pixels):

 ![Alt text](readme_figs/01_stitched_small.jpg?raw=true "Title")

#### 2) List of landmarks

Standard Comma-Separated-Values (CSV) data format is used 
to store the information about the landmarks.
The user defines the locations of the landmarks 
by himself.

The information is stored as a table with columns:

* `ID` - landmark unique identifier
* `Name` - full name of the landmark
* `ShortName` - short name of the landmark, 
will be displayed on the slides
* `X`,`Y` - landmark coordinates on the original map image
* `R` - radius of the landmark to be displayed
* `Color` - color of the landmark 
(see Python color designations)
* `Grid` - coordinates of the landmark on the grid

Example (see file `landmarks.txt`):

```
ID,Name,ShortName,X,Y,R,Color,Grid  
1,Carpiquet,CQ,107,895,58,c,XV85  
2,Beny-sur-Mer,BM,139,611,58,c,XV86  
3,Blue-1,B1,874,130,50,b,BQ88  
4,Blue-2,B2,1307,560,50,b,CQ06  
7,Evreux,ER,2597,1121,58,m,CQ63  
8,Red-1,R1,1502,391,50,r,CQ17 
```  

#### 3) List of connections between the landmarks

Also a CSV-file with two columns:

* `NM1` - short name of landmark-1
* `NM2` - short name of landmark-2

The connections are symmetrical: if you already have a
connection from landmark-1 to landmark-2, there's no need 
for a connection from landmark-2 to landmark-1.

Example (see file `connections_all.txt`):

```
NM1,NM2 
CQ,BM  
CQ,B4  
CQ,F1  
BM,B1  
BM,F1  
```

## Editing script files

Once the input data is prepared, some manipulations 
are needed to be done with the script files.

#### 1) Setting up configuration

Information about the region map, landmarks and 
connections need to be put in the `Configuration` 
class in `configuration.py` file. 

Paths to the input files need to be put as values of 
`path_to_map`, `path_to_landmarks` and 
`path_to_connections` class fields. 
Output directory can be specified using 
`output_dir` field.

Size (in pixels) of each slide to be extracted from the
original map image can be specified using 
`slide_extraction_size` field. 
Slide positions are defined using a list of top-left
corner (`X`,`Y`) coordinates `slide_topleft_XYs`.
The output size of slides in pixels is defined using 
`slide_output_size`.

Distances between landmarks are calculated 
automatically based on their distance measured in pixels.
Therefore, for correct calculation of distances image
scale need to be assessed and put as a value of 
`scaleKilometersPerPixel` field. 
Possible scheme of scale assessment is shown below. 
 
 ![Alt text](readme_figs/02_scale_measurement.jpg?raw=true "Title")
  
#### 2) Altering display settings

Various display settings are stored in `DisplaySettings` 
class (file `display_settings.py`). Editing this class one can change the sizes and 
colors of different elements.

## Running the script

Once everything is done, the script can be run `main.py` 
script using your favourite Python3.7 interpreter. 
Required python packages are listed in `requirements.txt`.
All these are standard packages and can be easily 
installed using `pip`. 

If succeeded, the script must generate a number of files 
in the specified `output_dir`. 
Among them there should be larger and smaller versions 
of the region map with marked landmarks and connections, 
looking similar to this:

 ![Alt text](readme_figs/03_map_preview.jpg?raw=true "Title")
 
 And a list of ready-to-use kneeboard slides which can
 be built into a user mission. 
 Looking like this:
 
 ![Alt text](readme_figs/04_out_slides.png?raw=true "Title")
 
 