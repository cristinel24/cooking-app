docker stop mongo1 mongo2 mongo3

docker run -d --rm -p 27017:27017 --name mongo1 --network mongoCluster mongo:7.0.2 mongod --replSet myReplicaSet --port 27017
docker run -d --rm -p 27018:27018 --name mongo2 --network mongoCluster mongo:7.0.2 mongod --replSet myReplicaSet --port 27018
docker run -d --rm -p 27019:27019 --name mongo3 --network mongoCluster mongo:7.0.2 mongod --replSet myReplicaSet --port 27019

sleep 3

docker exec -it mongo1 mongosh --eval "rs.initiate({
        _id: \"myReplicaSet\",
        members: [
            {_id: 0, host: \"mongo1:27017\", priority: 2},
            {_id: 1, host: \"mongo2:27018\", priority: 1},
            {_id: 2, host: \"mongo3:27019\", priority: 1}
        ]
    })"

echo "Done"