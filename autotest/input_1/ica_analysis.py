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
delta = 10000.0
reactive_ratio = 0.1

def link_property(objname,propname,nonzero=True,noexception=True,output_to=gridlabd.warning):

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
        if noexception:
            output_to(f"unable to link to {objname}.{propname}")
            pass
        else:
            raise

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
            objdata = gridlabd.get_object(objname)
            if "phases" in objdata.keys():
                classdata = gridlabd.get_class(classname)
                pattern = target_properties[classname].replace("[ABC]",f"[{objdata['phases']}]")
                for propname in classdata.keys():
                    if re.match(pattern,propname):
                        link_property(objname,propname,nonzero=False)
    return True

def on_sync(t):

    global property_list
    global limit_list

    dt = datetime.datetime.fromtimestamp(t)
    gridlabd.debug(f"*** onsync({dt}) ***")
    violation_active = int(gridlabd.get_global("powerflow::violation_active"))
    if violation_active:
        gridlabd.debug(f"{dt}: violation detected (violation_active={violation_active})")

    done = None
    if property_list:
        objname = list(property_list.keys())[0]
        gridlabd.debug(f"{dt}: updating {objname}")
        proplist = property_list[objname]
        if proplist:
            for propname, specs in proplist.items():
                prop = specs[0]
                base = specs[1]
                if base.real == 0.0:
                    value = prop.get_value() - complex(delta,delta*reactive_ratio)
                else:
                    value = prop.get_value() - base/base.real*delta
                if not violation_active:
                    gridlabd.debug(f"{dt}: updating {objname}.{propname} = {value}")
                    prop.set_value(value)
                    load_limit = base - value
                    limit_list[objname][propname] = {"timestamp":t, "real":load_limit.real, "reactive":load_limit.imag}
                else:
                    gridlabd.debug(f"{dt}: resetting {objname}.{propname} to base {base}")
                    prop.set_value(base)
                    if violation_active:
                        done = objname
        else:
            done = objname
        if done:
            gridlabd.debug(f"{dt}: finished with {objname}")
            if proplist == {}:
                del property_list[objname]
            else:
                property_list[objname] = {}
            if property_list:
                gridlabd.debug(f"{dt}: next is {list(property_list.keys())[0]}")
        if violation_active:
            gridlabd.debug(f"{dt}: clearing violation")
            gridlabd.set_global("powerflow::violation_active","0")
        tt = t+60
        gridlabd.debug(f"updating to {datetime.datetime.fromtimestamp(tt)}")
        return tt
    else:
        gridlabd.debug(f"updating to NEVER")
        return gridlabd.NEVER

def on_term(t):

    global output_folder
    global limit_list

    with open(f"{output_folder}/solar_capacity.csv","w") as fh:
        writer = csv.writer(fh)
        writer.writerow(["load","solar_capacity[kW]"])
        for objname, property_data in limit_list.items():
            power = 0.0
            for propname, data in property_data.items():
                power += data["real"]/1000.0   
            writer.writerow([objname,round(power,1)])
    return None

