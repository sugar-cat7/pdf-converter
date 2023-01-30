alias exec='docker exec -it python3 bash'
alias rmc='docker rm -f $(docker ps -a -q)'
alias rmi='docker rmi -f $(docker images -q)'
alias rmall='rmc && rmi'
