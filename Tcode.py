
"""
       caseApis: "[{"method":"102",
       "url":"https://mitest.n.xiaomi.com/api/manager/v1/public/task/trigger/api",
       "account":"-1",
       "interval":"0",
       "params":[],
       "header":[{"name":"Token","value":"mitest#110#api"}],
       "body":{"type":"101","value":"{\"api_url\":\"https://mitest.n.xiaomi.com/\", \"api_user\":\"huhaitao\", \"api_debug\": \"true\"}"},
       "verify":{"type":"102","value":[]},
       "extract":{"type":"101","value":[]}}]"

"""
"""
        caseApis: "[

        {"method":"102",
        "url":"https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        "account":"-1",
        "interval":"0",
        "params":[],
        "header":[{"name":"Content-Type","value":"application/json"}],
        "body":{"type":"101","value":"123"},
        "verify":{"type":"102","value":[]},
        "extract":{"type":"101","value":[{"name":"token","value":"$.tenant_access_token"}]}},

        {"method":"102",
        "url":"https://open.feishu.cn/open-apis/message/v4/send/",
        "account":"-1",解释
        "interval":"0",间隔
        "params":[],
        "header":[{"name":"Authorization","value":"Bearer {{token}}"},{"name":"Content-Type","value":"application/json"}],
        "body":{"type":"101","value":""},
        "verify":{"type":"102","value":[]},
        "extract":{"type":"101","value":[]}}]"
"""

"""
        caseApis: "[
        {"key":"api#1574934330813",
        "method":"102",
        "url":"https:/e&淀清":"0",
        "params":[{"name":"q","value":"14"}],
        "header":[],
        "body":{"type":"101","value":""},
        "verify":{"type":"102","value":[{"name":"$.result[*].data[*].detail_url.weburl","value":"[2-3]\\d\\d","mode":"101"}]},
        "extract":{"type":"101","value":[]}}]"
"""

"""
caseApis: "[
{"method":"102",
"url":" http://api.keyou.site:8000/user/login/",
"account":"-1",
"interval":"0",
"params":[],
"header":[{"name":"Content-Type","value":"[{\"key\":\"Content-Type\",\"name\":\"Content-Type\",\"value\":\"application/json\",\"description\":\"\",\"type\":\"text\"}]"}],
"body":{"type":"101","value":"{"username":"keyou1","password":"123456"}"},  type {json form}
"verify":{"type":"102","value":[{"name":"$.user_id","value":"2","mode":"101"}]},  type(字段js, 完整)
"extract":{"type":"101","value":[]}}]"  type(jp,re)
"""
