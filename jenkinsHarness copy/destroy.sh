terraform -chdir=terraform destroy -var-file=<(cat ./terraform/creds.tfvars ./terraform/conversion.tfvars) -auto-approve

pod_name=$(./shellCommands/jenkinsCred.sh)
adminPass=$(kubectl exec -n devops-tools -it $pod_name -- cat /var/jenkins_home/secrets/initialAdminPassword )
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:$adminPass -webSocket delete-job demo

minikube delete