
**EMS(Elevator Maintenance System)**

This is an elevator maintaince system built using django.This application just contains the backed apis
to maintain the state of an elevator.It also listens to all the state changes when an elevator is called to
a floor and when the users sends request to go to a particular floor.
The workflow of this is mentioned later in this doc.

*How to Start*

Use below commant to run the application. This will build the docker image and all the requirements,
and will start the server at port 8000.

```
docker-compose up
```


*Process Flow*

elevator creation
    req-
    - no of floors 
    - no of elevators
    - time for each floor // This is considered as average time. Waiting time of lift is ignored here

get current state at any time
    resp-
    - cout of elevator
    - state of each elevator [moving, stopped, maintenance ]
    - current floor
    - action (up/down)
    {"elevator_no": [state, action, current_floor, stops[] -> heapq ]}

assign an elevator-
    req-
    - requested floor
    - requested action (up/down)

    resp-
    - elevator_no

    algo-
    - check for nearest elevator
        dir = 0, dist = 0
        loop in all elevators
            dist = mod(curr floor - requested floor)
            if state is moving
                if requested action == elevator current action
                    dir = -1
                else
                    dir = 1 // dont store in this case as the lift is moving in reverse
            insert into heapq (dist, dir, elevator_no)
    - add requested floor in stops
    - update state as moving
    return index of elevator of top

update floor no
    req-
    - elevator_no (received from assign elevator response)
    - destination floor
    resp-
    - success

    process-
    - add destination floor in stops heap
    - update state as moving

status updater (background task)
    - runs for each floor time
    - loops for each elevator
        if state == stopped or maintenance -> pass
        check the stops[top] == current_floor then delete stops[top] // This can be tweaked to include waiting time
        current_floor = current_floor + 1
        if stops.length == 0 then update state as stopped

update maintaince:
    req-
    - elevator_no
    - mark_maintainence: (true/false)
    
    process-
    - if true update [maintaince, up, 0, stops[] ]
    - if false update state = stopped


*curls*

curl --location --request POST 'http://127.0.0.1:8000/ems/create-elavators' \
--header 'Content-Type: application/json' \
--data-raw '{
    "floors": 9,
    "elevators": 3,
    "floor_time": 3
}'

curl --location --request GET 'http://127.0.0.1:8000/ems/get-elavators'

curl --location --request POST 'http://127.0.0.1:8000/ems/assign-elavator' \
--header 'Content-Type: application/json' \
--data-raw '{
    "requested_floor": 4,
    "requested_action": "moving up"
}'

curl --location --request POST 'http://127.0.0.1:8000/ems/update-floor' \
--header 'Content-Type: application/json' \
--data-raw '{
    "elevator_no": 0,
    "destination_floor": 7
}'

curl --location --request PUT 'http://127.0.0.1:8000/ems/mark-maintaince' \
--header 'Content-Type: application/json' \
--data-raw '{
    "elevator_no": 0,
    "mark_maintainence": true
}'