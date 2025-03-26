import time
import subprocess
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

# 環境変数から設定を取得
SERVICE_ACCOUNT_FILE = "Base Ninja IAM Admin.json"
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
ADMIN_PRIVATE_KEY = os.getenv('ADMIN_PRIVATE_KEY')
RPC_URL = os.getenv('RPC_URL')
RANGE_NAME = "Sheet1!A2:A"
POLL_INTERVAL = 5  # シートチェックの間隔（秒）
NFT_URI = os.getenv('NFT_URI')

# ===== Google Sheets API の認証 =====
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# 前回処理済みの行数を保持する変数
last_processed_row = 0

def check_for_new_addresses():
    """
    Google Sheets から現在のアドレス一覧を取得し、
    前回以降に追加された新規アドレスのリストを返す。
    """
    global last_processed_row
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    new_addresses = []
    
    if not values:
        print("シートにデータが見つかりません。")
    else:
        # 前回処理済みの行以降の新規行をチェック
        if len(values) > last_processed_row:
            for row in values[last_processed_row:]:
                if row and row[0]:
                    new_addresses.append(row[0])
            # 最新の行数を記録
            last_processed_row = len(values)
    return new_addresses

def mint_nft(recipient_address):
    """
    Foundry の cast コマンドを利用して NFT の mint 処理を実行する関数
    """
    cmd = [
        "cast", "send", CONTRACT_ADDRESS, "mintTo(address,string)", recipient_address, NFT_URI,
        "--private-key", ADMIN_PRIVATE_KEY, "--rpc-url", RPC_URL
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"ミント処理成功: {recipient_address}")
        print("出力:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ミント処理失敗: {recipient_address}")
        print("エラー:", e.stderr)

if __name__ == "__main__":
    print("自動ミントタスク開始...")
    while True:
        addresses = check_for_new_addresses()
        if addresses:
            for addr in addresses:
                print(f"新しいウォレットアドレス検出: {addr}")
                mint_nft(addr)
        time.sleep(POLL_INTERVAL)
