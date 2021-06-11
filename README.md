***LOCKDOWN PROGRAMMING PRACTICE

Things to do:
    
    [x] Create URL versioning
    [x] AuthenticatMion
    [x] Middleware
    [x] test swagger
    [x] add documentation in swagger
    [ ] creating postgreSQL db with docker
    [ ] connect endpoinds to db

docker db:
        
    sudo docker run --name=bookstore-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRESS_DB=bookstore -p 5432:5432 -d postgres:latest

*i download datagrip for db UI

    sudo snap install datagrip --classic
*make sure db connect with db docker
