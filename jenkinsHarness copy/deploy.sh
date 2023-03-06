pod_name=$(./shellCommands/jenkinsCred.sh)
adminPass=$(kubectl exec -n devops-tools -it $pod_name -- cat /var/jenkins_home/secrets/initialAdminPassword )

# Validating Jenkins Job
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:$adminPass -webSocket create-job demo < $2 
out=$(java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:$adminPass -webSocket build demo -s | grep SUCCESS)


echo $out

if [ ${#out} -ge 27 ]

then 
    echo "Job Validated"

    #Code Conversion
    python ./jenkins_to_harness.py $1

    #Deploying the pipeline
    terraform -chdir=terraform init
    terraform -chdir=terraform apply -var-file=<(cat ./terraform/creds.tfvars ./terraform/conversion.tfvars) -auto-approve

else
    echo "Invalid Job"

fi