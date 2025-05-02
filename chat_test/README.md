# AIチャットボットアプリケーション

このアプリケーションは、StreamlitとPerplexity APIを使用した対話型AIチャットボットです。

## 機能
- Perplexity APIを利用したAIとのチャット機能（コスパの良いモデルを使用）
- 会話履歴の保存
- モデル選択機能（sonar-small-chat、sonar-medium-chat、mistral-7b-instruct）
- テンパレチャー（創造性）の調整
- カスタムアバター表示機能

## 必要条件
- Python 3.10以上
- Anaconda環境

## インストール方法

1. Anaconda環境を作成し有効化する
```bash
conda create -n streamlit_chat python=3.10 -y
conda activate streamlit_chat
```

2. 必要なパッケージをインストール
```bash
pip install streamlit requests python-dotenv Pillow
```

3. `.env`ファイルを作成し、Perplexity APIキーを設定
```
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

## 使い方

1. 環境を有効化
```bash
conda activate streamlit_chat
```

2. アプリケーションを起動
```bash
streamlit run app.py
```

3. ウェブブラウザで自動的に開かれたアプリケーションを使用

## 設定項目

- **モデル選択**: 使用するAIモデルを選択できます（sonar-small-chatはコスパが良いモデルです）
- **テンパレチャー**: AIの回答の創造性を調整できます（低いと一貫性が高く、高いと創造的になります）

## 注意事項

- Perplexity APIの使用には料金が発生する場合があります
- APIキーは他人と共有しないでください 