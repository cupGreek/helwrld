terraform {
  
  required_providers {
    
    harness = {
      source  = "harness/harness"
      version = "0.14.1"
    }

    github = {
      source  = "integrations/github"
      version = "5.17.0"
    }

  }

}


data "local_file" "pipeline_definition"{
    filename = var.pipelineSource
}

data "local_file" "trigger_definition"{
    filename = var.triggerSource
}


provider "github" {
  token = var.gitPAT
  owner = var.gitOwner
}

provider "harness" {  
    endpoint          = var.harnessEndpoint  
    account_id        = var.harnessAccId  
    platform_api_key  = var.harnessPlatApiKey  
}


resource "harness_platform_secret_text" "git_secret" {
  identifier  = "gitsecret"
  name        = "git_secret"
  description = "Personal Access Token to allow API Access to GitHub"
  project_id  = var.harnessProjectID  
  org_id      = var.harnessOrgID

  secret_manager_identifier = "harnessSecretManager"
  value_type                = "Inline"
  value                     = var.gitPAT
}

/* Unable to upload a json file
resource "harness_platform_secret_file" "gcp_secret" {
  identifier  = "gcpsecret"
  name        = "gcp_secret"
  description = "Service Account Key to allow API Access to GCP Services"
  project_id  = "default_project"  
  org_id      = "default"

  secret_manager_identifier = "harnessSecretManager"
  file_path                 = var.gcp_serviceAccount_secret
}
*/

resource "github_repository" "pipeline_repo" {  
  name        = var.pipelineRepoName
  description = "Repository to host Pipeline Definition"
  auto_init   = true
}

resource "harness_platform_connector_github" "pipeline_git_connector" {
  identifier  = "pipelineGitcon"
  name        = "pipelineGitCon"
  description = "GitHub connector to facilitate Pipeline Source Code Management"
  project_id  = var.harnessProjectID  
  org_id      = var.harnessOrgID

  url                = var.gitAccountURL
  connection_type    = "Account"
  validation_repo    = github_repository.pipeline_repo.name
  delegate_selectors = var.delegateSelector

  credentials {
    http {
      username  = var.gitOwner
      token_ref = harness_platform_secret_text.git_secret.identifier
    }
  }

  api_authentication {
    token_ref = harness_platform_secret_text.git_secret.identifier
  }
}

resource "harness_platform_connector_github" "code_git_connector" {
  identifier  = var.codebaseGitConID
  name        = "codeGitCon"
  description = "GitHub connector to facilitate Triggers. Triggers should point to this connector"
  project_id  = var.harnessProjectID  
  org_id      = var.harnessOrgID

  url                = var.codebaseUrl
  connection_type    = "Repo"
  delegate_selectors = var.delegateSelector

  credentials {
    http {
      username  = var.gitOwner
      token_ref = harness_platform_secret_text.git_secret.identifier
    }
  }

  api_authentication {
    token_ref = harness_platform_secret_text.git_secret.identifier
  }
}


resource "harness_platform_connector_gcp" "gcp_connector" {
  identifier  = var.gcpConID
  name        = "gcpCon"
  description = "GCP Service Account Connector"
  project_id  = var.harnessProjectID  
  org_id      = var.harnessOrgID

  manual {
    secret_key_ref     = "serviceAccount_Key" //harness_platform_secret_file.gcp_secret
    delegate_selectors = var.delegateSelector
  }
}

resource "harness_platform_pipeline" "test_pipeline" {  
    identifier  = "demo"  
    name        = "demo"  
    description = "Simple Approval Stage pipeline generated through Terraform"  
    project_id  = var.harnessProjectID  
    org_id      = var.harnessOrgID

    git_details {
        branch_name    = "main"
        commit_message = "commitMessage"
        file_path      = var.pipelineFileName
        connector_ref  = harness_platform_connector_github.pipeline_git_connector.identifier
        store_type     = "REMOTE"
        repo_name      = github_repository.pipeline_repo.name
    }  
  
    yaml = data.local_file.pipeline_definition.content
}

resource "harness_platform_triggers" "test_trigger" {
  name        = "name"
  identifier  = "identifier"
  project_id  = var.harnessProjectID  
  org_id      = var.harnessOrgID
  target_id   = harness_platform_pipeline.test_pipeline.identifier
  yaml        = data.local_file.trigger_definition.content
}