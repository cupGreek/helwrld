# imports

import json

# function to build the ShellScript step
# input: ShellScript components, the step template, step number
# output: step as a dict

def build_step_ShellScript(component, step, step_number):
    step["step"]["name"] = "ShellScript-" + str(step_number)
    step["step"]["identifier"] = "ShellScript" + str(step_number)
    step["step"]["spec"]["source"]["spec"]["script"] = component["command"]
    return step

# function to build the GitClone step
# input: GitClone components, the step template, step number
# output: step as a dict

def build_step_GitClone(component, step, step_number):
    step["step"]["name"] = "GitClone-" + str(step_number)
    step["step"]["identifier"] = "GitClone" + str(step_number)
    step["step"]["spec"]["repoName"] = component["repoName"]
    step["step"]["spec"]["build"]["spec"]["branch"] = component["branch"]
    return step

# function to build the Email step
# input: Email components, the step template, step number
# output: step as a dict

def build_step_Email(component, step, step_number):
    step["step"]["name"] = "Email-" + str(step_number)
    step["step"]["identifier"] = "Email" + str(step_number)
    step["step"]["spec"]["to"] = component["to"]
    step["step"]["spec"]["subject"] = component["subject"]
    step["step"]["spec"]["body"] = component["body"]
    return step

# function to build the Run step
# input: Run command, the step template, step number
# output: step as a dict

def build_step_Run(component, step, step_number):
    step["step"]["name"] = "Compile-" + str(step_number)
    step["step"]["identifier"] = "Compile" + str(step_number)
    step["step"]["spec"]["command"] = component["command"]
    return step

# function to build the SaveCacheGCS step
# input: SaveCacheGCS components, the step template, step number
# output: step as a dict

def build_step_SaveCacheGCS(component, step, step_number):
    step["step"]["name"] = "Push to GCS Repository-" + str(step_number)
    step["step"]["identifier"] = "PushtoGCSRepository" + str(step_number)
    step["step"]["spec"]["bucket"] = component["bucket"]
    step["step"]["spec"]["key"] = component["key"]
    step["step"]["spec"]["sourcePaths"] = component["sourcePaths"]
    return step
    