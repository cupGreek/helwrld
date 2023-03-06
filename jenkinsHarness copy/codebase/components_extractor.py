# Static Variable to store repo name
class stat:
    git_repo_name = "."

# function to extract the GitClone components from the xml dict
# input: data from the xml file as a dictionary/json
# output: GitClone components

def extract_GitClone_components(xml_dict):
    GitClone_components = {}
    GitClone_components["type"] = "GitClone"
    GitClone_components["repoName"] = xml_dict["project"]["scm"]["userRemoteConfigs"]["hudson.plugins.git.UserRemoteConfig"]["url"].split("/")[-1]
    stat.git_repo_name = GitClone_components["repoName"]
    GitClone_components["branch"] = xml_dict["project"]["scm"]["branches"]["hudson.plugins.git.BranchSpec"]["name"].split("/")[-1]
    return GitClone_components

# function to extract the ShellScript components from the xml dict
# input: data from the xml file as a dictionary/json
# output: ShellScript components

def extract_ShellScript_components(xml_dict):
    ShellScript_components = {}
    if type(xml_dict['project']['builders']) == list:
        for i in xml_dict['project']['builders']:
            for j in i.keys():
                if j == 'hudson.tasks.Shell':
                    cmd = i['hudson.tasks.Shell']['command']
                    ShellScript_components["type"] = "ShellScript"
                    ShellScript_components["command"] = cmd
                    return ShellScript_components
    else:
        i = xml_dict['project']['builders']
        for j in i.keys():
            if j == 'hudson.tasks.Shell':
                cmd = i['hudson.tasks.Shell']['command']
                ShellScript_components["type"] = "ShellScript"
                ShellScript_components["command"] = cmd
                return ShellScript_components

# function to extract the Email components from the xml dict
# input: data from the xml file as a dictionary/json
# output: Email components

def extract_Email_components(xml_dict):
    Email_components = {}
    Email_components["to"] = xml_dict["project"]["publishers"]["hudson.plugins.emailext.ExtendedEmailPublisher"]["recipientList"]
    Email_components["subject"] = xml_dict["project"]["publishers"]["hudson.plugins.emailext.ExtendedEmailPublisher"]["defaultSubject"]
    Email_components["body"] = xml_dict["project"]["publishers"]["hudson.plugins.emailext.ExtendedEmailPublisher"]["defaultContent"]
    return Email_components

# function to extract the Run components from the xml dict
# input: data from the xml file as a dictionary/json
# output: Run components

def extract_Run_components(xml_dict):
    Run_components = {}
    if type(xml_dict['project']['builders']) == list:
        for i in xml_dict['project']['builders']:
            for j in i.keys():
                if j == 'hudson.tasks.Shell':
                    cmd = i['hudson.tasks.Shell']['command']
                    cmd = f"cd {stat.git_repo_name}\n" + cmd
                    Run_components["type"] = "Run"
                    Run_components["command"] = cmd
                    return Run_components
    else:
        i = xml_dict['project']['builders']
        for j in i.keys():
            if j == 'hudson.tasks.Shell':
                cmd = i['hudson.tasks.Shell']['command']
                cmd = f"cd {stat.git_repo_name}\n" + cmd
                Run_components["type"] = "Run"
                Run_components["command"] = cmd
                return Run_components

# function to extract the SaveCacheGCS components from the xml dict
# input: data from the xml file as a dictionary/json
# output: SaveCacheGCS components

def extract_SaveCacheGCS_components(xml_dict):
    SaveCacheGCS_components = {}
    SaveCacheGCS_components["bucket"] = xml_dict["project"]["publishers"]["com.google.jenkins.plugins.storage.GoogleCloudStorageUploader"]["uploads"]["com.google.jenkins.plugins.storage.ClassicUpload"]["bucketNameWithVars"].split("//")[1].split("/")[0]
    SaveCacheGCS_components["key"] = xml_dict["project"]["publishers"]["com.google.jenkins.plugins.storage.GoogleCloudStorageUploader"]["uploads"]["com.google.jenkins.plugins.storage.ClassicUpload"]["bucketNameWithVars"].split("//")[1].split("/")[1]
    SaveCacheGCS_components["sourcePaths"] = [f"{stat.git_repo_name}/" + xml_dict["project"]["publishers"]["com.google.jenkins.plugins.storage.GoogleCloudStorageUploader"]["uploads"]["com.google.jenkins.plugins.storage.ClassicUpload"]["sourceGlobWithVars"]]
    return SaveCacheGCS_components