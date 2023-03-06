success='1/1'

output=$(kubectl get pods --namespace=devops-tools | grep jenkins-.)
read -ra arr <<< "$output"

while [ ${arr[1]} != $success ]
do
    output=$(kubectl get pods --namespace=devops-tools | grep jenkins-.)
    read -ra arr <<< "$output"
    sleep 1m
done

pod_name=$arr

echo $pod_name