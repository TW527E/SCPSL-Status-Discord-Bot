# SCPSL Status Discord Bot

[English](README.en.md)

這個專案會透過 SCPSL 官方 API 取得伺服器狀態，並用多個 Discord bot 分別更新各伺服器的狀態訊息與機器人狀態。

## 重要說明

這個專案使用的是「幾年前」SCPSL 官方伺服器列表 API。這不是一般用途的新 API 範例；如果要使用，你必須已經擁有一個上了官方列表的 SCPSL 伺服器，並且自行找到當年分配給該伺服器使用的 API token / account 資料。

這次整理的目的只是把手頭上原本設為私人的老案子整理成比較安全、可讀、可重新開源的狀態；不保證這套 API 對新伺服器或新申請流程仍然適用。

## 檔案用途

- `start.py`：主程式入口，負責載入設定、啟動多個 Discord bot、同步 slash command、查詢 SCPSL API、更新 Discord Embed。
- `setting.json`：非敏感的全域設定，例如時區、API URL、bot 清單與每台 bot 對應的資料檔。
- `setting.example.json`：`setting.json` 範例。這個專案實際使用的檔名是 `setting.json`。
- `.env`：本機敏感資料，例如 SCPSL API token、Account ID、Discord bot token。此檔案不應提交到 Git。
- `.env.example`：`.env` 範例。
- `data/server_*.json`：每台 bot/server 的獨立資料，包含 SCPSL server codename、Discord 訊息位置、Embed 文字與 bot 狀態文字。
- `data/server.example.json`：`data/server_*.json` 範例。
- `data/scpsl_status_cache.json`：最近一次 API 回應快取，執行時自動更新。

## 安裝

1. 安裝 Python 3.10 或更新版本。
2. 安裝依賴：

```powershell
pip install -r requirements.txt
```

3. 參考 `.env.example` 建立 `.env`，填入真實 token。
4. 確認 Discord bot invite URL 有包含 `applications.commands` scope，否則 slash command 不會出現。
5. 編輯 `setting.json` 的 `bots` 清單。
6. 編輯或複製 `data/server_*.json`。
7. 啟動：

```powershell
python start.py
```

## Slash Command

目前只有一個管理指令：

```text
/here
```

用途：在目前頻道建立狀態訊息，並把 `guild_id`、`channel_id`、`message_id` 寫回對應的 `data/server_*.json`。

限制：只有該 Discord bot 的 owner 可以使用。

## setting.json 格式

完整範例請看 `setting.example.json`。

```json
{
  "description": "設定說明文字",
  "timezone": "Asia/Taipei",
  "fallback_cooldown_seconds": 24,
  "footer_text": "Made by YourName",
  "owner_id": 123456789012345678,
  "api": {
    "base_url": "https://api.scpslgame.com/serverinfo.php",
    "token_env": "SCPSL_API_TOKEN",
    "account_id_env": "SCPSL_ACCOUNT_ID",
    "cache_file": "scpsl_status_cache.json"
  },
  "bots": [
    {
      "key": "server_1",
      "name": "Server #1",
      "token_env": "DISCORD_BOT_TOKEN_1",
      "data_file": "server_1.json",
      "sync_guild_ids": [
        123456789012345678
      ],
      "enabled": true
    }
  ]
}
```

欄位說明：

- `timezone`：顯示更新時間用的時區。
- `fallback_cooldown_seconds`：API 失敗或沒有回傳 cooldown 時的重試間隔。
- `footer_text`：Embed footer 後綴文字。
- `owner_id`：footer 頭像使用者 ID，也可用來辨識維護者。
- `api.token_env`：`.env` 裡 SCPSL API token 的變數名稱。
- `api.account_id_env`：`.env` 裡 SCPSL Account ID 的變數名稱。
- `bots[].key`：內部識別名稱，建議用 `server_1`、`server_2`。
- `bots[].name`：log 中顯示的名稱。
- `bots[].token_env`：`.env` 裡 Discord bot token 的變數名稱。
- `bots[].data_file`：對應的 `data/*.json` 檔名。
- `bots[].sync_guild_ids`：要立即同步 slash command 的 Discord guild ID。留空陣列時會改用全域同步，但 Discord 全域 slash command 可能需要較久才出現。
- `bots[].enabled`：是否啟用這台 bot。

## data/server_*.json 格式

完整範例請看 `data/server.example.json`。

```json
{
  "server_codename": 0,
  "message": {
    "guild_id": 123456789012345678,
    "channel_id": 123456789012345678,
    "message_id": 123456789012345678
  },
  "embed": {
    "Server Icon": "https://example.com/server-icon.png",
    "Message Title": "Example SCPSL Server Status",
    "Server Description": "Live server status",
    "Last Updated": "Last updated %Time% (UTC+8)",
    "Separate line": "----------",
    "Status": [
      true,
      "Status",
      "狀態",
      "Status"
    ],
    "Status Started": [
      "已正常啟動",
      "Server started"
    ]
  },
  "presence": {
    "Bot Status Started": "%Players%",
    "Bot Status Closed": "伺服器已關閉",
    "Bot Status Warning": "無法獲取狀態"
  }
}
```

上面的 `embed` 只示範一個欄位群組；實際可用群組如下：

- `Status`
- `Port`
- `Players`
- `Version`
- `Pastebin`
- `Infomation`
- `LastOnline`

每個欄位群組都有相同格式：

```json
"Status": [
  true,
  "區塊標題",
  "左欄欄位名稱",
  "右欄欄位名稱"
],
"Status Started": [
  "伺服器在線時左欄顯示值",
  "伺服器在線時右欄顯示值"
],
"Status Closed": [
  "伺服器離線時左欄顯示值",
  "伺服器離線時右欄顯示值"
],
"Status Warning": [
  "API 失敗時左欄顯示值",
  "API 失敗時右欄顯示值"
]
```

第一個陣列值是 `true` 或 `false`，用來決定是否顯示該欄位群組。

可用替換變數：

- `%Time%`
- `%Port%`
- `%Players%`
- `%Version%`
- `%Pastebin%`
- `%LastOnline%`
- `%FriendlyFire%`
- `%Whitelist%`
- `%Modded%`

`Infomation` 是為了相容舊設定保留的 key 名稱，請先維持這個拼法。

## 新增一台 bot

1. 在 `.env` 新增一個 token，例如：

```env
DISCORD_BOT_TOKEN_7=your_discord_bot_token_7
```

2. 複製 `data/server.example.json` 成 `data/server_7.json`，修改 `server_codename`、Embed 文字與訊息位置。
3. 在 `setting.json` 的 `bots` 加一筆：

```json
{
  "key": "server_7",
  "name": "Server #7",
  "token_env": "DISCORD_BOT_TOKEN_7",
  "data_file": "server_7.json",
  "sync_guild_ids": [
    123456789012345678
  ],
  "enabled": true
}
```

4. 啟動 bot 後，在目標頻道使用 `/here`。
