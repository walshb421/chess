# Example Chess Application

## Development 

You will need to install Docker and the docker-compose standalone script to run the docker env. 
Otherwise you will need a compatible NodeJS and Python environment. 


To build the application run:
```bash
docker-compose build
```

To run the application run:
```bash
docker-compose up 
```

Additionally, you can build and run the application in the background.
```bash
    docker-compose up --build -d
```


You can stop the development server by running:
```bash
docker-compose down
```

After running you can open your browser to [localhost:8080](http://localhost:8080)