variable "gitOwner" {
    default = ""
}

variable "gitPAT" {
    default = ""
}

variable "gitAccountURL"{
    default = ""
}

variable "harnessAccId"{
    default = ""
}

variable "harnessPlatApiKey" {
  default = ""
}

variable "codebaseUrl" {
    default = ""
}

variable "harnessProjectID" {
    default = "default_project"
}

variable "harnessOrgID" {
    default = "default"
}

variable delegateSelector{
    type = list
    default = ["demo"]
}

variable "pipelineSource" {
    default = "demo.yml"
}

variable "triggerSource" {
    default = "trigger-sample.yml"
}

variable "harnessEndpoint" {
    default = "https://app.harness.io/gateway"
}

variable "pipelineRepoName"{
    default = "pipeline-repo"
}

variable "pipelineFileName" {
    default = ".harness/demopipeline.yml" 
}

variable "codebaseGitConID" {
    default = "gitconnect" 
}

variable "gcpConID" {
    default = "demo" 
}


variable "gcp_serviceAccount_secret" {
    default = ""
}