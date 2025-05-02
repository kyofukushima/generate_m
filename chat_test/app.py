import streamlit as st
import os
from PIL import Image
import base64
import json
import requests
from dotenv import load_dotenv

# ページ設定（他のStreamlit要素より先に実行する必要があります）
st.set_page_config(
    page_title="まえのとのチャット",
    page_icon="🧑‍💼",
    layout="centered"
)

# 環境変数の読み込み
load_dotenv()


# Perplexity APIキーの設定
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
if not perplexity_api_key:
    st.error("Perplexity APIキーが設定されていません。.envファイルに PERPLEXITY_API_KEY を設定してください。")

# アバター画像のディレクトリを作成（存在しない場合）
os.makedirs("images", exist_ok=True)

# 定数定義
DEFAULT_AI_AVATAR = "images/ai_avatar.png"
AVATAR_SIZE = 120
AI_NAME = "まえの"
DISPLAY_STYLE = "カスタム（アバター下に名前表示）"

# Perplexity APIのエンドポイントとモデル設定
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
DEFAULT_MODEL = "sonar" # コスパの良いモデル

# システムプロンプトをJSONファイルから読み込む
def load_system_prompt():
    try:
        with open('system_prompt.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data["prompt"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        st.error(f"システムプロンプトの読み込みに失敗しました: {str(e)}")
        return "あなたは親切なアシスタントです。ユーザーからの質問に対して、簡潔で役立つ回答を提供してください。"

# 画像をbase64にエンコードする関数
def get_image_base64(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Perplexity APIを呼び出す関数
def get_perplexity_response(messages, model, temperature=0.7):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {perplexity_api_key}"
    }
    
    # モデル名はドキュメント(https://docs.perplexity.ai/guides/model-cards)に合わせる
    # 'llama-3'接頭辞を削除
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }
    
    try:
        response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers)
        if response.status_code != 200:
            st.error(f"APIリクエストエラー: {response.status_code} {response.text}")
            return "すみません、回答の取得中にエラーが発生しました。"
        
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"APIリクエストエラー: {str(e)}")
        return "すみません、回答の取得中にエラーが発生しました。"

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ai_avatar" not in st.session_state:
    st.session_state.ai_avatar = DEFAULT_AI_AVATAR

# アバターサイズを適用するカスタムCSS
def apply_avatar_css(size):
    # 最も具体的なCSSセレクタを使用
    st.markdown(f"""
    <style>
        /* すべての可能性のあるセレクタを網羅 */
        div.stChatMessage div.avatar-image img,
        div.stChatMessage img.avatar-image,
        div.stChatMessage .stAvatar img,
        div.stChatMessage .stImage img,
        div.stChatMessage img,
        .stChatMessage .stAvatar img {{
            width: {size}px !important;
            height: auto !important;
            min-width: {size}px !important;
            max-width: {size}px !important;
            object-fit: contain !important;
            border-radius: 0px !important;
        }}
        
        /* コンテナの大きさ */
        div.stChatMessage .stAvatar,
        div.stChatMessage .avatar-image,
        div.stChatMessage [data-testid="stImage"] {{
            width: {size}px !important;
            height: auto !important;
            min-width: {size}px !important;
            max-width: {size}px !important;
        }}
        
        /* メッセージの余白を調整 */
        div.stChatMessage [data-testid="stChatMessageContent"] {{
            margin-left: {size + 20}px !important;
        }}
        
        /* !importantを使用して他のスタイルを上書き */
        div.stChatMessage .stAvatar * {{
            width: {size}px !important;
            height: auto !important;
        }}
        
        /* カスタムチャットレイアウト */
        .custom-chat-container {{
            display: flex;
            margin-bottom: 20px;
        }}
        
        .custom-avatar-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-right: 15px;
            width: {size + 20}px;
        }}
        
        .custom-avatar-image {{
            width: {size}px;
            height: auto;
            border-radius: 0px;
            object-fit: contain;
        }}
        
        .custom-avatar-name {{
            margin-top: 5px;
            font-size: 12px;
            text-align: center;
            color: #666;
            font-weight: bold;
            max-width: {size}px;
            word-wrap: break-word;
        }}
        
        .custom-message-container {{
            flex: 1;
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 10px 15px;
            max-width: calc(100% - {size + 40}px);
        }}
        
        .custom-user-container {{
            display: flex;
            flex-direction: row-reverse;
            margin-bottom: 20px;
        }}
        
        .custom-user-message {{
            background-color: #e6f7ff;
            border-radius: 10px;
            padding: 10px 15px;
            max-width: 80%;
            align-self: flex-end;
            margin-left: auto;
        }}
    </style>
    """, unsafe_allow_html=True)

# 初期CSS適用
apply_avatar_css(AVATAR_SIZE)

# タイトル
st.title(f"{AI_NAME}とチャット")
st.subheader("質問や相談に答えます")

# サイドバーの設定
with st.sidebar:
    st.header("設定")
    
    # リセットボタンのみ残す
    if st.button("会話をリセット", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# カスタムメッセージコンポーネント
def custom_chat_message(content, is_user=False):
    if is_user:
        # ユーザーメッセージ（右側に表示）
        st.markdown(f"""
        <div class="custom-user-container">
            <div class="custom-user-message">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # AIメッセージ（左側に表示、アバター付き）
        avatar_base64 = get_image_base64(DEFAULT_AI_AVATAR)
        if avatar_base64:
            avatar_img = f'<img src="data:image/png;base64,{avatar_base64}" class="custom-avatar-image">'
        else:
            avatar_img = f'<div class="custom-avatar-image" style="background-color: #FF4B4B;"></div>'
        
        st.markdown(f"""
        <div class="custom-chat-container">
            <div class="custom-avatar-container">
                {avatar_img}
                <div class="custom-avatar-name">{AI_NAME}</div>
            </div>
            <div class="custom-message-container">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)

# 過去のメッセージを表示（常にカスタム表示を使用）
for message in st.session_state.messages:
    if message["role"] == "assistant":
        custom_chat_message(message["content"], is_user=False)
    else:
        custom_chat_message(message["content"], is_user=True)

# ユーザー入力
if prompt := st.chat_input("メッセージを入力してください"):
    # ユーザーメッセージの追加
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # ユーザーのメッセージを表示
    custom_chat_message(prompt, is_user=True)
    
    # システムプロンプトを含む全メッセージの準備
    system_prompt = load_system_prompt()
    messages = [
        {"role": "system", "content": system_prompt}
    ] + st.session_state.messages
    
    # アシスタントの回答を取得
    with st.spinner("考え中..."):
        try:
            # Perplexity APIを使用して回答を取得（固定モデルを使用、temperature=0.7に固定）
            full_response = get_perplexity_response(messages, "sonar", 0.7)
            
            # AIの回答を表示
            custom_chat_message(full_response, is_user=False)
            
            # 回答をセッションに保存
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}") 