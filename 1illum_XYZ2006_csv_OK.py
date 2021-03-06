'''
Created on 28 janv. 2014

@author: gary
'''
import csv
import color


f = open('measurementsMA68II.csv')
reader = csv.reader(f, delimiter = ',')
spect_data = dict()

for row in reader:
    if not row[0] in spect_data:
        spect_data[row[0]] = dict()
    spect_data[row[0]][row[1]] = row[2]
    # file structure is: name, wavelength, measurement 
        

#print spect_data['1']['400']

f = open('CMF_MA68II.csv')
reader = csv.reader(f, delimiter = ',')
cmf = dict()
    
for row in reader:
    cmf[row[0]] = {'x_bar':row[1], 'y_bar':row[2], 'z_bar':row[3]}
    # voir s'il y a moyen d'importer des floats avec le module csv
    # file structure is wavelength, x_bar, y_bar, z_bar



f = open('D65.csv')
reader = csv.reader(f, delimiter = ',')
illuminant = dict()
    
for row in reader:
    illuminant[row[0]] = row[1]
    # file structure is wavelength, amplitude

norm_Y = 0


for wavelength in illuminant.keys():
    norm_Y = norm_Y + float(cmf[wavelength]['y_bar']) * float(illuminant[wavelength])
    
print "norm_Y = " + str(norm_Y)

XYZ = dict()

for name in spect_data.keys():
    X = 0
    Y = 0
    Z = 0
    
    temp=[]
    
    for wavelength in spect_data[name].keys():
        
        X += float(cmf[wavelength]['x_bar']) * float(illuminant[wavelength]) * float(spect_data[name][wavelength])
        Y += float(cmf[wavelength]['y_bar']) * float(illuminant[wavelength]) * float(spect_data[name][wavelength])
        Z += float(cmf[wavelength]['z_bar']) * float(illuminant[wavelength]) * float(spect_data[name][wavelength])
        
        temp.append((wavelength,float(spect_data[name][wavelength]) ))
    
    XYZ[name] = {'X': X/norm_Y, 'Y': Y/norm_Y, 'Z': Z/norm_Y}   
    s = color.Spectrum(temp)
    
    c = color.Color(name, XYZ[name]['X'], XYZ[name]['Y'], XYZ[name]['Z'], spectrum = s )
    print c.spectrum
    print c

ofile = file('XYZcolorlist.csv', 'w')

for name in XYZ.keys():
    ofile.write(str(name) + ',' + str(XYZ[name]['X']) + ',' + str(XYZ[name]['Y']) + ',' + str(XYZ[name]['Z']) + '\n')
    


    
    
