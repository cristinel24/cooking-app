#!/bin/bash
echo "Initializing mongo cluster..."

sleep 5

mongosh --host mongo1 --eval "
    rs.initiate({
        _id: \"myReplicaSet\", 
        members: [ 
            {_id: 0, host: \"mongo1:27017\", priority: 2}, 
            {_id: 1, host: \"mongo2:27017\", priority: 1}, 
            {_id: 2, host: \"mongo3:27017\", priority: 1}
        ]
    })
"

if [ "$?" -ne 0 ]; then
    exit 1
fi

echo "Letting it cook..."
sleep 20

mongosh --host mongo1 --eval "rs.status()"

echo "Done"
exit 0
