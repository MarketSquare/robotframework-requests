RequestsLibrary is a [Robot Framework](http://code.google.com/p/robotframework/)
test library that uses the [Requests](https://github.com/kennethreitz/requests) HTTP client. 


Usage
=====

You need to have requests installed

NOTE: Only support requests 0.9.0 or lower

``` pip install -U requests==0.9.0```

Now install robotframework-requests

```pip install -U robotframework-requests```

<table border=1>
    <tr>
        <td>Settings</td>
    </tr>
    <tr>
        <td> Library </td>
        <td> Collections </td>
    </tr>

    <tr>
        <td> Library </td>
        <td> RequestsLibrary</td>
    </tr>

    <tr>
        <td>Test Cases</td>
    </tr>

    <tr>
        <td>Get Requests</td>
    </tr>

    <tr>
        <td></td>
        <td>Create Session</td>
        <td>github</td>
        <td>http://github.com/api/v2/json</td>
    </tr>
    <tr>
        <td></td>
        <td>Create Session</td>
        <td>google</td>
        <td>http://www.google.com</td>
    </tr>
    <tr>
        <td></td>
        <td>${resp}=</td>
        <td>Get</td>
        <td>github</td>
        <td>/</td>
    </tr>
    <tr>
        <td></td>
        <td>Should Be Equal As Strings</td>
        <td>${resp.status_code}</td>
        <td>200</td>
    </tr>

    <tr>
        <td></td>
        <td>${resp}=</td>
        <td>Get</td>
        <td>github</td>
        <td>/user/search/bulkan</td>

    </tr>

    <tr>
        <td></td>
        <td>Should Be Equal As Strings</td>
        <td>${resp.status_code}</td>
        <td>200</td>
    </tr>
    <tr>
        <td></td>
        <td>${jsondata}=</td>
        <td>To JSON</td>
        <td>${resp.content}</td>
    </tr>

    <tr>
        <td></td>
        <td>Dictionary Should Contain Value</td>
        <td>${jsondata['users'][0]}</td>
        <td>Bulkan Savun Evcimen</td>
    </tr>
</table>
