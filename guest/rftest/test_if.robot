#查询发布会
*** Setting ***
Library  RequestsLibrary
Library  Collections

*** Test Cases ***
#查询发布会接口
test_get_event_list
    ${payload}=    Create Dictionary    eid=1
    Create Session    event    http://127.0.0.1:8000/api
    ${r}=    Get Request    event    /get_event_list/    params=${payload}
    Should Be Equal As Strings    ${r.status_code}    200
    log    ${r.json()}
    ${dict}    Set variable    ${r.json()}

    #断言
    ${msg}    Get From Dictionary    ${dict}    message
    Should Be Equal    ${msg}    success
    ${sta}    Get From Dictionary    ${dict}    status
    ${status}    Evaluate    int(200)
    Should Be Equal    ${sta}    ${status}

#嘉宾签到
test_user_sign_success
    Create Session    sign    http://127.0.0.1:8000/api
    &{headers}    Create Dictionary    Content-Type=application/x-www-form-urlencoded
    &{payload}    Create Dictionary    eid=3    phone=15227105153
    ${r}=    Post Request    sign    /user_sign/    data=${payload}    headers=${headers}
    Should Be Equal As Strings    ${r.status_code}    200
    log    ${r.json()}
    ${dict}    Set variable    ${r.json()}

    #断言
    ${msg}    Get From Dictionary    ${dict}    message
    Should Be Equal    ${msg}    sign success
    ${sta}    Get From Dictionary    ${dict}    status
    ${status}    Evaluate    int(200)
    Should Be Equal    ${sta}    ${status}


#新增发布会
test_add_event
    Create Session    event    http://127.0.0.1:8000/api
    &{headers}    Create Dictionary    Content-Type=application/x-www-form-urlencoded
    &{payload}    Create Dictionary    eid=6    name=robot    limit=123    status=1    address=chaoyang    start_time=2020-04-05 12:00:00
    ${r}=    Post Request    event    /add_event/    data=${payload}    headers=${headers}
    Should Be Equal As Strings    ${r.status_code}    200
    log    ${r.json()}
    ${dict}    Set Variable    ${r.json()}

    #断言
    ${msg}    Get From Dictionary    ${dict}    message
    Should Be Equal    ${msg}    添加成功
    ${sta}    Get From Dictionary    ${dict}    status
    ${status}    Evaluate    int(200)
    Should Be Equal    ${sta}    ${status}

#查询嘉宾接口
test_get_guest_list
    Create Session    guest    http://127.0.0.1:8000/api
    ${payload}=    Create Dictionary    eid=3    phone=15227105153
    ${r}=    Get Request    guest    /get_guest_list/    params=${payload}
    Should Be Equal As Strings    ${r.status_code}    200
    log    ${r.json()}
    ${dict}    Set variable    ${r.json()}

    #断言
    ${msg}    Get From Dictionary    ${dict}    message
    Should Be Equal    ${msg}    success
    ${sta}    Get From Dictionary    ${dict}    status
    ${status}    Evaluate    int(200)
    Should Be Equal    ${sta}    ${status}

#新增嘉宾
test_add_guest
    Create Session    guest    http://127.0.0.1:8000/api
    &{headers}    Create Dictionary    Content-Type=application/x-www-form-urlencoded
    &{payload}    Create Dictionary    eid=7    realname=robotname    phone=123311    email=1123@123.com
    ${r}=    Post Request    guest    /add_guest/    data=${payload}    headers=${headers}
    Should Be Equal As Strings    ${r.status_code}    200
    log    ${r.json()}
    ${dict}    Set Variable    ${r.json()}

    #断言
    ${msg}    Get From Dictionary    ${dict}    message
    Should Be Equal    ${msg}    success add
    ${sta}    Get From Dictionary    ${dict}    status
    ${status}    Evaluate    int(200)
    Should Be Equal    ${sta}    ${status}
#test_add_guest
#    Create Session    guest    http://127.0.0.1:8000/api
#    &{headers}    Create Dictionary    Content-Type=application/x-www-form-urlencoded
#    &{payload}    Create Dictionary    eid=7    realname=robot    phone=1233    email=152@123.com
#    ${r}=    Post Request    guest    /add_guest/    data=${payload}    headers={headers}
#    Should Be Equal As Strings    ${r.status_code}    200
#    log    ${r.json()}
#    ${dict}    Set Variable    ${r.json()}

    #断言
#    ${msg}    Get From Dictionary    {dict}    message
#    Should Be Equal    ${msg}    success add
#    ${sta}    Get From Dictionary    {dict}    status
#    ${status}    Evaluate    int(200)
#    Should Be Equal    ${sta}    ${status}