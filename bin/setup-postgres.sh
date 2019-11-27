#!/bin/bash

brew services start postgres
sleep 3
createuser -s "postgres"

createdb "goforbroca-${FLASK_ENV}"
./goforbroca db migrate
