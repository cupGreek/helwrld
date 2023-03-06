pip install -r requirements.txt

minikube start

kubectl apply -f delegateSetup/harness-delegate.yml

kubectl apply -f jenkinsSetup/serviceAccount.yaml
sleep 10

kubectl create -f jenkinsSetup/volume.yaml
sleep 10

kubectl apply -f jenkinsSetup/deployment.yaml
sleep 10

kubectl apply -f jenkinsSetup/service.yaml

sleep 1m

pod_name=$(./shellCommands/jenkinsCred.sh)

adminPass=$(kubectl exec -n devops-tools -it $pod_name -- cat /var/jenkins_home/secrets/initialAdminPassword )
echo "Password: $adminPass" > ./JenkinsCredentials
echo "CLI: java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:${adminPass}" >> ./JenkinsCredentials

kubectl -n devops-tools port-forward $pod_name 8080:8080
