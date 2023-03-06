Version 1.0
Authors: TMT West Solutions Team


I. Prerequisites

    1. The solution is currently built to be ran on a Linux environment.

    2. The entire setup is broken down into smaller shell scripts with each one designed to do a certain task.
        a. As a prerequisite, all the shell scripts should be provided with executable access.
           This can be achieved by simply running the commands "chmod +x ./*sh" and "chmod +x ./shellCommands/*.sh"

    3. The following needs to be created and will be used in Section II 
        a. 2 GCP service account keys (One for Jenkins and Another for Harness) of an service account with Storage Admin privileges in JSON format.
        b. 2 Google account app password (One for Jenkins and Another for Harness) for the account from which email notification is to be sent
            DO NOT USE THE SAME CREDENTIALS ACROSS JENKINS AND HARNESS. THIS MIGHT LEAD TO PROBLEMS.
        c. A Harness Platform account with atleast a default_project.

II. Setting up the infrastructure

    1. Harness Delegate Setup:
        a. Copy the harness-delegate.yml from Harness Platform under the "(older) Create Delegate" tab and paste it under the delegateSetup folder with the same file name
                            or 
           Make a copy of the template-harness-delegate.yml under the delegateSetup folder. Fill the required details within it and rename it to "harness-delegate.yml"

    2. run the setup.sh shell script (no arguments required) 
        a. the command to run the script is "./setup.sh"
            i. This will install python dependencies, setup a local minikube instance and deploy Jenkins & Harness pods under devops-tools & harness-delegate-ng namespaces respectively.
        
        b. The Jenkins dashboard can be accessed from Cloud Shell Web Preview - port 8080
        c. The admin credentials will be saved within the "JenkinsCredentials" file in the home directory

    3. Jenkins Setup
        a. Basic Setup
            i.   Open the dashboard via Cloud Shell Web Preview on port 8080 and use the admin credentials present in "JenkinsCredentials" file to proceed with the setup.
            ii.  Choose "Install suggested plugins" option and wait till the installation is complete. 
            iii. On the next screen, choose "Skip and continue as admin". Then click on "Save and Finish".
            iv.  Click on "Start using Jenkins"

        b. Google Cloud storage and Email Extenstion setup
            i.   Navigate to "Manage Jenkins" -> "Manage Plugins" -> "Avaialable Plugins" and search and select the "Google Cloud Storage" plugin. Proceed with "Install without restart".
            ii.  Once the installation is complete, return back to the "Manage Jenkins" tab. Click on "Manage Credentials" and then click on "(global)"
            iii. Click on "Add Credentials". Select "Username with Password" option and enter the email ID  as username and app password as the password. ID of the credential can be anything. Proceed to create the credential.
            iv.  Click on "Add Credentials". Select Google Service Account from Private Key. The Project Name should be "demo". Upload the GCP Service Account key under the JSON key file. Proceed to create the credential.
            v.   Navigate back to "Manage Jenkins" -> "Configure System". Scroll down to the Extended E-mail Notification section.
                - SMTP server: smtp.gmail.com (in case of a gmail account)
                - SMTP Port: 587
                - Click on "Advanced.." then choose the credential created earlier and make sure to tick the "Use TLS" checkbox.
                - Apply and Save

    4. Harness Setup
        a. GCP Secret creation
            i.   The GCP Service account key could not be uploaded as a harness_secret_file via Terraform. So we will be creating the secret, which the connector (created via Terraform) will be making use of.
            ii.  Sign in to Harness Platform and click on "Deployments". Navigate to "PROJECT SETUP" -> "Secrets". Click on "New Secret" and select "File".
            iii. Name it "serviceAccount_Key", Upload the Service Account Key (JSON File) and Save.

        b. SMTP configuration
            i.   Go to "Account Settings" -> "Account Resources" -> "SMTP Configuration" and Click on "Setup"
                  - Name: Provide as needed
                  - Host: smtp.gmail.com (in case of a gmail account)
                  - Port: 587
                  - Check the "Start TLS" checkbox
                  - From Address: email ID of the gmail account
            ii.  Click continue to proceed to the next page
                  - Username: Username of the email account
                  - Password: App Password of the email account
            iii. In the next screen you can test the SMTP by sending a sample notification to one of the email present within the project.
            

III. Deploying the solution

    1. Under terraform directory, fill the required fields in "creds.tfvars" and "conversion.tfvars"
    
    2. Copy the admin password from "JenkinsCredentials" and replace the variable "$adminPass" within the shell script "deploy.sh".
        a. Facing issues passing the credentials as variable to the java command and hence the temporary fix

    3. Run the "deploy.sh" shell script with the relative path to the job description as the single arguement to start the execution
        a. an Example will look like the following:
            "./deploy.sh ./jobs/demo4/java_gcs.xml"
        b. the solution currently only supports the 4 demos present under the "jobs" directory
        c. it's crucial that the relative path specified starts with './'


IV. Clean up

    1. The entire infrastructure setup by the solution can be brought down by running the "destroy.sh" shell script with no arguements
        a. Due to the reasons mentioned above in III.2.a, copy the admin password from "JenkinsCredentials" file and replace the variable "$adminPass" within the shell script "destroy.sh".
        b. the command to run the script is "./destroy.sh"