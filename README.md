# セットアップ

以下のコマンドを実行して必要なパッケージをインストールしてください:

```bash
pip install
```

## 起動方法

以下のコマンドを実行してスクリプトを起動してください:

```bash
python nft_mint_task.py
```

スクリプトが正常に動作するためには、事前に `.env` ファイルに必要な値を設定してください。

### `.env` に設定する値

- **SPREADSHEET_ID**: ウォレットアドレスの読み込みと書き込みを行うスプレッドシートの ID  
- **CONTRACT_ADDRESS**: Thirdweb 上で作成した NFT のコントラクトアドレス  
- **OWNER_ADDRESS**: コントラクトアドレスを作成したウォレットアドレス  
- **ADMIN_PRIVATE_KEY**: コントラクトアドレスを作成したウォレットアドレスの秘密鍵  
- **RPC_URL**: Infura の RPC URL  
- **NFT_URI**: NFT の URI  