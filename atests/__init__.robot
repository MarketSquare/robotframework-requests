*** Settings ***
Resource            res_setup.robot

Suite Setup         Setup Flask Http Server
Suite Teardown      Teardown Flask Http Server And Sessions
