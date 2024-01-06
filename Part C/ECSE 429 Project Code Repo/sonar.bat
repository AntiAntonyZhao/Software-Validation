@REM C:\Users\peter\Downloads\apache-maven-3.9.5\bin\mvn.cmd clean verify sonar:sonar -Dsonar.projectKey=resapi -Dsonar.projectName='resapi' -Dsonar.host.url="http://localhost:9000" -Dsonar.token=sqp_0ce3de0c8b8ab7e7ddfca3021be4ac2da48f24a1

@REM mvn clean verify sonar:sonar -Dsonar.projectKey='restapi' -Dsonar.token=<SONAR TOKEN>

cd thingifier-1.5.5
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=restapi \
  -Dsonar.projectName='restapi' \
  -Dsonar.host.url=https://sonarecse429.azurewebsites.net \
  -Dsonar.token=sqp_35a76ca8c8065978fd7b145287752180e71d0ba2