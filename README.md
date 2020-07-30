# Cookies Pool

## Configurable variables

|  variable name                |  default value        | overridable |
| ----------------------------- | --------------------- | ----------- |
| GENERATOR\_PROCESS\_ENABLED   | TRUE                  | YES         |
| TESTER\_PROCESS\_ENABLED      | TRUE                  | YES         |
| REMOTE\_ENABLED               | TRUE                  | YES         |
| SELENIUM\_HUB                 | selenium-hub          | YES         |
| REDIS\_HOST                   | redis                 | YES         |
| REDIS\_PORT                   | 6379                  | YES         |

## Docker

Deploy

```
$ docker-compose up -d --build
```

Down

```
$ docker-compose down --rmi local
```

## Usage

### 添加一組帳號密碼

```
POST /account/<website>/
```

Example:

```
$ curl -X POST -H "Content-Type: application/json" -d '{"account" : "test_account", "password" : "123456789"}' "http://127.0.0.1:6250/account/ig/"
```

Success:

```
{
    "message": "Add account success",
    "params": {
        "website": "ig",
        "account": "test_account",
        "password": "123456789"
    }
}
```

Fail condition: 帳號已存在

```
{
    "message": "Account is exist!"
}
```

### 得到一組隨機的 cookies

```
GET /cookies/<website>/random/
```

Example:

```
$ curl -X GET "http://127.0.0.1:6250/cookies/ig/random/"
```

Success:

```
{
    "message": "Get ig cookies success",
    "cookies": "{\"ig_did\": \"BC7AF1D7-003D-4718-92F7-636B40C015CF\", \"rur\": \"FTW\", \"mid\": \"XyFBlQAEAAH6HmUhdqvYuwpS4s_s\", \"sessionid\": \"25659826982%3A2HItgj1QcoHA3G%3A16\", \"csrftoken\": \"fwVotsqlYS1HPhN5ZWZzAEFEadlCMH5E\", \"ds_user_id\": \"39662739281\", \"urlgen\": \"\\\"{\\\\\\\"72.320.332.83\\\\\\\": 3462}:1k0iPW:LAgs2u5cNYxmJxKEDJlHg1RrUA8\\\"\"}"
}
```

Fail condition: 尚未有可用的 cookies

```
{
    "message": "尚未有可用的 ig cookies!"
}
```

### 行程 (Process) 啟動 / 關閉，透過 `環境變數` 修改

```
# 模擬登入取得 cookies 後，添加至資料庫
export GENERATOR_PROCESS_ENABLED=TRUE

# 檢測資料庫中的 cookies 是否過期，如過期則刪除
export TESTER_PROCESS_ENABLED=TRUE
```

### 運行行程 (Process)

```
$ docker-compose exec api sh
/cookies-pool # pipenv run python main.py
```
