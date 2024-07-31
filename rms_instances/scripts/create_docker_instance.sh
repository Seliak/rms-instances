EMAIL=$1
DATABASE_NAME=$2
BASE_PORT=8070

get_free_docker_compose_file() {
  # Maximum number of instances we are allowing to check for free ports
  MAX_INSTANCES=10
  
  for ((i=0; i<$MAX_INSTANCES; i++)); do
    port=$((BASE_PORT + i))
    if ! docker ps -a | grep -q ":$port->"; then
      docker_compose_file="rms_instances/scripts/compose-$DATABASE_NAME-$port.yml"
      cp rms_instances/scripts/docker-compose-template.yml $docker_compose_file
      sed -i "s/8069:8069/$port:8069/g" $docker_compose_file
      echo $docker_compose_file
      return 0
    fi
  done
  return 1
}

docker_compose_file=$(get_free_docker_compose_file)
if [ $? -eq 0 ]; then
  docker-compose -p $DATABASE_NAME -f $docker_compose_file up --build --abort-on-container-exit &> rms_instances/logs/${DATABASE_NAME}.log
  echo $docker_compose_file
else
  echo "No available ports found." >&2
  exit 1
fi
