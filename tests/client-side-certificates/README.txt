To help with testing the 'Create Client Cert Session' keyword, a Docker container definition for a simple
nginx HTTPS server is provided in the docker-https-server directory.

=================================================================================================================
PRE-REQUISITES:
- docker (version 17.03.1-ce, build c6d412e was used for this testing)
   - Reference: https://docs.docker.com/get-started/
- docker-compose (version 1.11.2, build dfed245 was used for this testing)
   - Reference: https://docs.docker.com/compose/compose-file/compose-file-v2/
=================================================================================================================

To create and start the nginx HTTPS server container, change into the docker-https-server directory and execute:

    docker-compose up -d


If the container startup is successful, then the HTTPS server will be running in a container called
'https-svr-requiring-client-certs' and will be available at https://localhost.

After the HTTPS container is started, you can execute the provided test case:

    python -m robot client-certs-testcase.txt

=================================================================================================================
Docker Cleanup
=================================================================================================================
To stop the container, change into the docker-https-server directory and execute:

    docker-compose stop

To destroy the container, change into the docker-https-server directory and execute:

    docker-compose rm -f

