FOR /f "tokens=*" %%i IN ('docker ps -q --format={{.Names}}') DO (
    if NOT '%%i' == 'mysql' (
        docker kill %%i
    )
)

FOR /f "tokens=*" %%c IN ('docker ps -a -q --format={{.Names}}') DO (
    if NOT '%%c' == 'mysql' (
        docker rm %%c
    )
)

FOR /f "tokens=*" %%n IN ('docker network ls -q --format={{.Name}}') DO (
    if NOT '%%n' == 'someNetwork' (
        docker network rm %%n
    )
)

FOR /f "tokens=*" %%o IN ('docker images -q') DO docker rmi %%o

echo "Check if everything is removed:"
docker ps -a
docker images
