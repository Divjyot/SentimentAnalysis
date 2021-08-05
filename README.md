# Steps to run the project 

## Dockerfile
Main Features:
1. Installs `Anaconda` (`x86_64`architecture) on fresh `Ubuntu:bionic`  [refer](https://github.com/Divjyot/SentimentAnalysis/blob/e3fc87f7a1681085597d30b93c63919377261dd5/Dockerfile#L22)

    * ❌ M1 Macbooks
    * ✅ Windows
    * ✅ Non-M1 Macbooks 
2. Adds a sudo user named `Ubuntu`
3. Installs `conda` environment from `environment.yml` file
4. Makes `bash` shell initialise with said-installed `conda` environment. 
[refer](https://github.com/Divjyot/SentimentAnalysis/blob/e3fc87f7a1681085597d30b93c63919377261dd5/Dockerfile#L38)


## A. Locally via command line
1. ```cd app/```
2. ```flask run --host <HOST> --port <PORT>```


## B. Docker/docker-compose
1. `docker-compose build`
2. `docker-compose up`



# if your local port 80 is already occupied
1. Check using ```netstat -a -b``` and you can kill the process at that PID through `Resource Monitor` (on Windows)
2. Alternatively, `net stop http` could be used to kill all processes at `http`
