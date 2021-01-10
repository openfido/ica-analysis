"""
Created on Tue Sep 22 12:17:43 2020

Locate the ICA files with GLPATH, e.g.,

    host% export GLPATH=<ica-folder>:$GLPATH
    
To use this use the following command line:
    
    host% gridlabd <mymodel>.glm ica_analysis.glm
    
ica_analysis.glm:
    
    #set ...
    #input "ica_config.csv" -f ...
    import ica_analysis;

@author: saraborchers
"""

import re
import csv
import gridlabd
import datetime

# Create global lists to access and modify on_commit
output_folder = "."
object_list = []
target_properties = {"load":"constant_power_[ABC]$"}
property_list = {}
limit_list = {}

def link_property(objname,propname,nonzero=True,noexception=True):

    global property_list
    
    try:
        prop = gridlabd.property(objname,propname)
        value = prop.get_value()
        if not nonzero or value != 0.0:
            if not objname in property_list.keys():
                property_list[objname]={propname:[prop,value]}
                limit_list[objname] = {}
            else:
                property_list[objname][propname] = [prop,value]
    except:
        gridlabd.error(f"unable to link to {objname}.{propname}")
        pass

def on_init(t):
    
    global output_folder
    global object_list
    global target_properties

    # get the output folder name from the global variable list
    output_folder = gridlabd.get_global("OUTPUT")
    if not output_folder:
        output_folder = "."

    if not object_list:
        object_list = gridlabd.get("objects")
    for objname in object_list:
        classname = gridlabd.get_value(objname,"class")
        if classname in target_properties.keys():
            pattern = target_properties[classname]
            classdata = gridlabd.get_class(classname)
            for propname in classdata.keys():
                if re.match(pattern,propname):
                    link_property(objname,propname)

    return True

def on_sync(t):

    global property_list
    global limit_list

    violation_active = int(gridlabd.get_global("powerflow::violation_active"))

    changed = False
    done = None
    if property_list:
        objname = list(property_list.keys())[0]
        proplist = property_list[objname]
        for propname, specs in proplist.items():
            prop = specs[0]
            base = specs[1]
            value = prop.get_value() - base / 100.0
            if violation_active:
                prop.set_value(base)
                gridlabd.set_global("powerflow::violation_active","0")
                done = objname
                changed = True
            elif value.real >= -10*base.real:
                prop.set_value(value)
                load_limit = base - value
                limit_list[objname][propname] = {"timestamp":t, "real":load_limit.real, "reactive":load_limit.imag}
                changed = True            

    if done:
        del property_list[objname]
    if changed:
        return t+30
    else:
        return gridlabd.NEVER

def on_term(t):

    global output_folder
    global limit_list

    with open(f"{output_folder}/solar_limits.csv","w") as fh:
        writer = csv.writer(fh)
        writer.writerow(["object","property","timestamp","real","reactive"])
        for objname, property_data in limit_list.items():
            for propname, data in property_data.items():
                writer.writerow([objname,propname,datetime.datetime.fromtimestamp(data["timestamp"]),data["real"],data["reactive"]])
    return None

