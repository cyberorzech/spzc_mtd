from python_on_whales import docker

output = docker.run(
    "webserver",
    ["-p 80:80"]
)
print(output)
from time import sleep
sleep(20)