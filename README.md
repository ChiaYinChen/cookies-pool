# Cookies Pool

[![Build Status](https://travis-ci.com/ChiaYinChen/cookies-pool.svg?branch=master)](https://travis-ci.com/ChiaYinChen/cookies-pool)

Docker + Flask + Selenium 實現 Cookies Pool 服務，維護多個帳號的登入資訊，目前僅支援 Facebook 和 Instagram 網站。

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

## API Usage

- [x] 添加一組帳號密碼 [`/account/<website>/`] `POST`
- [x] 更新一組帳號的密碼 [`/account/<website>/`] `PUT`
- [x] 隨機獲取一組 cookies [`/cookies/<website>/random/`] `GET`

該服務僅支援 Facebook 和 Instagram，而 url 上需要提交的 `website` 變數，Facebook 以 `fb` 表示，Instagram 以 `ig` 表示。

### 添加一組帳號密碼

```
POST /account/<website>/
```

Example:

```bash
$ curl -X POST \
  "http://localhost:6250/account/ig/" \
  -H "Content-Type: application/json" \
  -d '{
        "account" : "test_account",
        "password" : "123456789"
  }'
```

Success:

```bash
{
    "message": "Add account success",
    "website": "ig",
    "params": {
        "account": "test_account",
        "password": "123456789"
    }
}
```

Fail condition: 帳號已存在

```bash
{
    "message": "Account is exist!"
}
```

### 更新一組帳號的密碼

```
PUT /account/<website>/
```

Example:

```bash
$ curl -X PUT \
  "http://localhost:6250/account/ig/" \
  -H "Content-Type: application/json" \
  -d '{
        "account" : "test_account",
        "password" : "987654321"
  }'
```

Success:

```bash
{
    "message": "Update account success",
    "website": "ig",
    "params": {
        "account": "test_account",
        "password": "987654321"
    }
}
```

Fail condition: 帳號不存在

```bash
{
    "message": "Account not found!"
}
```

### 隨機獲取一組 cookies

```
GET /cookies/<website>/random/
```

Example:

```bash
$ curl -X GET "http://localhost:6250/cookies/ig/random/"
```

Success:

```bash
{
    "message": "Get ig cookies success",
    "cookies": "{\"ig_did\": \"BC7AF1D7-003D-4718-92F7-636B40C015CF\", \"rur\": \"FTW\", \"mid\": \"XyFBlQAEAAH6HmUhdqvYuwpS4s_s\", \"sessionid\": \"25659826982%3A2HItgj1QcoHA3G%3A16\", \"csrftoken\": \"fwVotsqlYS1HPhN5ZWZzAEFEadlCMH5E\", \"ds_user_id\": \"39662739281\", \"urlgen\": \"\\\"{\\\\\\\"72.320.332.83\\\\\\\": 3462}:1k0iPW:LAgs2u5cNYxmJxKEDJlHg1RrUA8\\\"\"}"
}
```

Fail condition: 尚未有可用的 cookies

```bash
{
    "message": "尚未有可用的 ig cookies!"
}
```

## Process Usage

模擬登入網站取得 cookies，並檢測該 cookies 是否過期。隨後即可使用該 cookies 爬取已登入的頁面。

### 行程 (Process) 啟動 / 關閉，透過 `環境變數` 修改

```shell
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
