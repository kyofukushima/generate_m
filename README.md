# まえのとアプリ

このStreamlitアプリは「まえの」とのコミュニケーションをシミュレートするWebアプリケーションです。

## 機能

- **ボタン機能**: ランダムなビデオとテキストを表示します
- **チャット機能**: Perplexity APIを使用して「まえの」とチャットができます
- **音声読み上げ機能**: ElevenLabs APIを使用してチャット応答を音声で読み上げます

## セットアップ

### 必要なライブラリのインストール

```bash
pip install streamlit pillow requests
```

### Streamlit Secretsの設定

1. `.streamlit`ディレクトリをプロジェクトルートに作成します（存在しない場合）
2. `secrets.toml`ファイルを作成し、以下の内容を記入します：

```toml
[api_keys]
perplexity = "あなたのPerplexity APIキーをここに入力"
elevenlabs = "あなたのElevenLabs APIキーをここに入力"
```

> **注意**: `secrets.toml`ファイルはGitなどのバージョン管理システムにコミットしないでください。

### システムプロンプトの設定

`system_prompt.json`ファイルがプロジェクトルートに存在しない場合は、アプリ起動時に自動的に作成されます。カスタマイズする場合は、このファイルを編集してください。

## 動画の追加方法

1. 動画をYouTubeにアップロードします
   - 動画は「限定公開」または「非公開」に設定してください
   - 限定公開の場合は、アプリケーションにアクセスするユーザーに共有設定を追加してください

2. `videos.json`ファイルを編集します
   ```json
   {
       "videos": [
           {
               "id": "YouTubeの動画ID",
               "title": "動画のタイトル"
           }
       ]
   }
   ```
   - `id`: YouTubeの動画URLの `v=` パラメータの値（例：`https://www.youtube.com/watch?v=XXXXXXXXXXX` の `XXXXXXXXXXX` 部分）
   - `title`: 動画のタイトル（アプリケーションの選択リストに表示されます）

3. アプリケーションを再起動すると、新しい動画が選択リストに追加されます

## アプリの実行

以下のコマンドでアプリを起動します：

```bash
streamlit run app.py
```

## デプロイ

Streamlit Cloudにデプロイする場合は、以下の手順で行います：

1. GitHubにリポジトリをプッシュします
2. [Streamlit Cloud](https://streamlit.io/cloud)にアクセスしてサインインします
3. 「New app」ボタンをクリックし、GitHubリポジトリを選択します
4. APIキーなどの機密情報を「Secrets」セクションに設定します：
   - Perplexity APIキー
   - ElevenLabs APIキー

## ディレクトリ構造

```
project/
├── .streamlit/
│   └── secrets.toml     # APIキーなどの機密情報（Gitに含めない）
├── images/              # アバター画像やGIF画像を格納
├── videos/              # 動画ファイルを格納
├── gifs/                # GIFファイルを格納
├── app.py               # メインアプリケーションコード
├── system_prompt.json   # AIのシステムプロンプト設定
├── videos.json          # YouTube動画の設定ファイル
└── README.md            # このファイル
```

## カスタマイズ

- `videos.json`を編集することで、表示される動画を管理できます
- `images/ai_avatar.png`を置き換えることで、チャットアバターを変更できます
- `system_prompt.json`を編集することで、AIの応答特性を変更できます 