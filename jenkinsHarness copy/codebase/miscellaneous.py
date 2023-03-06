# imports

import json
import xmlplain

# function to convert yaml file to a dict object
# input: path to the yaml file
# output: data from the yaml file as a dict object

def from_yaml_to_dict(yaml_file):
    with open(yaml_file) as inf:
        root = xmlplain.obj_from_yaml(inf)
    return root

# function to convert dict object to a json file
# input: dict object, path to output json file

def dict_to_json(dict, name):
    with open(name, "w") as inf:
        json.dump(dict, inf, indent = 4)

# function to convert xml file to a dictionary
# input: path to the xml file
# output: data from the xml file as a dictionary/json

def from_xml_to_dict(xml_file):
    with open(xml_file) as fp:
        xml_dict = xmlplain.xml_to_obj(fp, strip_space=True, fold_dict=True)
    return xml_dict

# function to extract the right template
# input: template identifier
# output: relative path to the template

def get_template(identifier):
    with open("./config.json", "r") as file:
        config_data = json.load(file)
    if identifier == "pipeline":
        return config_data["pipeline"]["template"]
    elif identifier in config_data["pipeline"]["stage"].keys():
        return config_data["pipeline"]["stage"][identifier]["template"]
    else:
        for stage in config_data["pipeline"]["stage"].keys():
            if identifier in config_data["pipeline"]["stage"][stage]["step"].keys():
                return config_data["pipeline"]["stage"][stage]["step"][identifier]["template"]
        return "Template Not Found"

# function to find the parent stage of a step
# input: step whose stage needs to be found
# output: parent stage of the step

def get_stage(step):
    with open("./config.json", "r") as file:
        config_data = json.load(file)
    for stage in config_data["pipeline"]["stage"].keys():
        if step in config_data["pipeline"]["stage"][stage]["step"].keys():
            return stage
    return "Stage Not Found"

# function to extract the name of the function that extracts the components
# input: the step whose components need to be extracted
# output: name of the component function

def get_component_function(step):
    with open("./config.json", "r") as file:
        config_data = json.load(file)
    for stage in config_data["pipeline"]["stage"].keys():
        if step in config_data["pipeline"]["stage"][stage]["step"].keys():
            return config_data["pipeline"]["stage"][stage]["step"][step]["component_function"]
    return "Function Not Found"

# function to extract the name of the function to build a step
# input: the step which need to be built
# output: name of the build function

def get_build_function(step):
    with open("./config.json", "r") as file:
        config_data = json.load(file)
    for stage in config_data["pipeline"]["stage"].keys():
        if step in config_data["pipeline"]["stage"][stage]["step"].keys():
            return config_data["pipeline"]["stage"][stage]["step"][step]["build_function"]
    return "Function Not Found"
