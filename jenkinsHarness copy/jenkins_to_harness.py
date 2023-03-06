# imports
import sys
import json
import xmlplain

# custom imports

from codebase import step_builder
from codebase import components_extractor
from codebase.miscellaneous import get_template, get_stage
from codebase.miscellaneous import get_component_function, get_build_function
from codebase.miscellaneous import from_xml_to_dict, from_yaml_to_dict, dict_to_json


# function to build the harness pipeline
# input: steps, input xml 
# output: harness pipeline as yaml

def j2h(steps, input_file, output_file):

    step_number = 1
    xml_dict = from_xml_to_dict(input_file)

    with open(get_template("pipeline"), "r") as file:
        pipeline = json.load(file)

    for step_name in steps:

        stage_type = get_stage(step_name)
        stage_list = []
        for stg in pipeline["pipeline"]["stages"]:
            stage_list.append(stg["stage"]["type"])
        if stage_type not in stage_list:
            with open(get_template(stage_type)) as file:
                stage = json.load(file)
                pipeline["pipeline"]["stages"].append(stage)

        with open(get_template(step_name)) as file:
            step_template = json.load(file)

        compenent_function_name = get_component_function(step_name)
        component_function = getattr(components_extractor, compenent_function_name)
        step_components = component_function(xml_dict)

        build_function_name = get_build_function(step_name)
        build_function = getattr(step_builder, build_function_name)
        step = build_function(step_components, step_template, step_number)

        pipeline["pipeline"]["stages"][-1]["stage"]["spec"]["execution"]["steps"].append(step)
        step_number += 1

    with open(output_file, "w") as file:
        xmlplain.obj_to_yaml(pipeline, file)

# main execution

steps = {
    "./jobs/demo/shell.xml": ["ShellScript"],
    "./jobs/demo2/gitClone.xml": ["GitClone"],
    "./jobs/demo3/email.xml": ["GitClone", "Run", "Email"],
    "./jobs/demo4/java_gcs.xml": ["GitClone", "Run", "SaveCacheGCS", "Email"]
}

j2h(steps[sys.argv[1]], sys.argv[1], "./terraform/demo.yml")


# dict_to_json(from_yaml_to_dict("./jobs/demo4/javaGCS.yml"), "javaGCS yml.json")
# dict_to_json(from_xml_to_dict("./jobs/demo4/javaGCS.xml"), "javaGCS xml.json")