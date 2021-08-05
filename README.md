# Steps to run the project 

## A. Locally via command line
1. ```cd app/```
2. ```flask run --host <HOST> --port <PORT>```


## B. Docker/docker-compose
1. `docker-compose build`
2. `docker-compose up`



# if your local port 80 is already occupied
1. Check using ```netstat -a -b``` and you can kill the process at that PID through `Resource Monitor` (on Windows)
2. Alternatively, `net stop http` could be used to kill all processes at `http`
