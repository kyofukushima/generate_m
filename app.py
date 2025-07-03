import streamlit as st
import random
import os
from PIL import Image
import io
import json
import requests
import base64
import re
import time

# スクリプト自身の場所を基準にパスを解決
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# ページ設定（他のStreamlit要素より先に実行する必要があります）
st.set_page_config(
    page_title="まえのと",
    page_icon="🧑‍💼",
    layout="centered"
)

# YouTube動画の情報を読み込む関数（現在は未使用）
def load_youtube_videos():
    try:
        videos_json_path = os.path.join(APP_DIR, 'videos.json')
        with open(videos_json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # YOUR_VIDEO_IDの動画を除外
            return [video for video in data["videos"] if video["id"] != "YOUR_VIDEO_ID"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        # st.set_page_config()の前に呼び出される可能性があるため、ここではst.errorを使用しない
        print(f"[Warning] YouTube動画情報の読み込みに失敗しました: {str(e)}")
        return []

# ローカルの動画ファイルを取得する関数
def load_local_videos(video_dir="videos", max_size_mb=300):
    video_path = os.path.join(APP_DIR, video_dir)
    if not os.path.isdir(video_path):
        return []
    
    video_files = []
    skipped_files = []
    
    for f in os.listdir(video_path):
        if f.endswith(('.mp4', '.mov')):
            full_path = os.path.join(video_path, f)
            try:
                # ファイルサイズをチェック
                file_size_mb = os.path.getsize(full_path) / (1024 * 1024)
                if file_size_mb <= max_size_mb:
                    video_files.append(full_path)
                else:
                    skipped_files.append((f, file_size_mb))
            except OSError:
                # ファイルが読み取れない場合はスキップ
                continue
    
    # スキップしたファイルがある場合は警告を表示
    if skipped_files:
        print(f"[警告] 以下の動画ファイルはサイズが大きいためスキップされました:")
        for filename, size in skipped_files:
            print(f"  - {filename}: {size:.1f} MB")
    
    return video_files

# YouTube動画を表示する関数
def display_youtube_video(video_id):
    st.video(f"https://www.youtube.com/watch?v={video_id}")

# ローカル動画を表示する関数
def display_local_video(video_path):
    try:
        # ファイルの存在確認
        if not os.path.exists(video_path):
            st.error(f"動画ファイルが見つかりません: {video_path}")
            return
        
        # ファイルサイズを確認
        file_size = os.path.getsize(video_path)
        st.info(f"動画ファイル: {os.path.basename(video_path)} (サイズ: {file_size / (1024*1024):.1f} MB)")
        
        # ファイルサイズが大きすぎる場合の警告
        if file_size > 100 * 1024 * 1024:  # 100MB以上
            st.warning("⚠️ 動画ファイルが大きいため、読み込みに時間がかかる場合があります。")
        
        # 方法1: バイト配列として読み込み
        try:
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
            st.video(video_bytes)
            st.success("✅ 動画の読み込みが完了しました。")
        except Exception as e1:
            st.error(f"バイト配列での読み込みに失敗: {str(e1)}")
            
            # 方法2: ファイルパスを直接使用
            try:
                st.video(video_path)
                st.success("✅ ファイルパスでの動画読み込みが完了しました。")
            except Exception as e2:
                st.error(f"ファイルパスでの読み込みも失敗: {str(e2)}")
                
                # 方法3: 相対パスを試す
                try:
                    relative_path = os.path.relpath(video_path, APP_DIR)
                    st.video(relative_path)
                    st.success("✅ 相対パスでの動画読み込みが完了しました。")
                except Exception as e3:
                    st.error(f"相対パスでの読み込みも失敗: {str(e3)}")
                    st.error("すべての動画読み込み方法が失敗しました。ブラウザの開発者ツールでエラーを確認してください。")
    
    except Exception as general_error:
        st.error(f"動画の表示中に予期しないエラーが発生しました: {str(general_error)}")
        # デバッグ情報を表示
        st.info(f"動画パス: {video_path}")
        st.info(f"ファイル存在: {os.path.exists(video_path)}")
        if os.path.exists(video_path):
            st.info(f"ファイルサイズ: {os.path.getsize(video_path)} bytes")

# GIFとテキストのリストを用意
gifs = [
    os.path.join(APP_DIR, "images/muscle_maeno.gif"),
    os.path.join(APP_DIR, "images/spalta_maeno.gif"),
    os.path.join(APP_DIR, "images/SPOILER_capcut_test.gif"),
    os.path.join(APP_DIR, "images/SPOILER_maeno_oogiri.gif")
]

# 動画情報を読み込む
try:
    local_videos = load_local_videos()
    print(f"[INFO] 読み込まれた動画ファイル数: {len(local_videos)}")
    if local_videos:
        print("[INFO] 利用可能な動画ファイル:")
        for i, video in enumerate(local_videos, 1):
            size_mb = os.path.getsize(video) / (1024 * 1024)
            print(f"  {i}. {os.path.basename(video)} ({size_mb:.1f} MB)")
    else:
        print("[WARNING] 利用可能な動画ファイルがありません")
except Exception as e:
    print(f"[ERROR] 動画ファイルの読み込み中にエラーが発生しました: {e}")
    local_videos = []

texts = [
    """父が明日手術することになりました
からこういうときこそ、私が
母を支えてあげないといけない。
友達の母が昨日病気になりました。
からこういうときこそ、私が
友達を支えてあげないといけない。
私がここで弱音を吐くことは出来ない
そういうとき人は
次の新らなステージへ上がると思っています""",
    """今日は『すずめの戸締まり』があるそうなのでこのへんで失礼します
天気の子や君の名は。などを手がける新海誠監督が最新作の長編アニメーション映画『すずめの戸締まり』が
2022年11月11日に公開されたのですが、この作品では
AWSのクラウドが利用されています。
天気の子などは以前までオンプレミスでサーバーを管理をしていたそうなのですが、
どれくらいアクセスするかわからなかったり、ストレージが足りなくなったり、
レンダリング待ちが発生してしまったり、バックアップの管理が厳しいという課題が
ありました。
そこで、AWSのクラウドを導入したところ、レンダリング待ちがなくなったり、
ストレージもいつでも拡張出来たり、バックアップも取得出来たり、コンソール画面で
簡単な操作で利用出来るようになり、クラウドに移行して良かったと満足しているみたいです。
そんな観点で映画を観たいです。
みんなで戸締まりして帰ります。""",
    """昨日はあめに引き寄せられたのか
ラップ現象が頻繫にしたり、誰かに見られている感覚
が強めでしたが、今日はその感覚がなくなってきました。""",
"""原田さんから飴をもらって思い出したのですが、
土日は友達が家遊びに行っていい？と
急に言われて、友達と家で遊んでました。
流れで晩御飯も作ってくれて美味しくて
また食べたくなるかもしれない""",
"""私は最近プライベートでいろいろな役職の方や友達にいろいろと教えてもらいました。
今まで明確な夢はなかったのですが、5年後、10年後になりたい夢があります。
その夢を叶えるために逆算し、今は無理かなと思っても挑む心を忘れては
夢は叶えることが出来ない。
そして、若いうちにお金を使わないと意味がないと誰かが言っていたので、
挑戦したいと思います。
20代ではなく30代前半だが失敗を恐れては夢に近づくことは
出来ない。先に進むという気持ちがあれば年齢関係なく先に進めるはずだと思っています。
今あるトランプのカードで全力で挑戦したいと思います。""",
"""本日、体調が悪いため、お先に失礼します。

今年も大変お世話になりました。
来年もどうぞよろしくお願いいたします。
良いお年をお迎えください。"""
]

# アバター画像のディレクトリを作成（存在しない場合）
os.makedirs(os.path.join(APP_DIR, "images"), exist_ok=True)

# チャット関連の定数定義
DEFAULT_AI_AVATAR = None
for img_path in [os.path.join(APP_DIR, 'images/ai_avatar.png'), os.path.join(APP_DIR, 'images/muscle_maeno.gif'), os.path.join(APP_DIR, 'images/spalta_maeno.gif')]:
    if os.path.exists(img_path):
        DEFAULT_AI_AVATAR = img_path
        break

AVATAR_SIZE = 120
AI_NAME = "まえの"
DISPLAY_STYLE = "カスタム（アバター下に名前表示）"

# Perplexity APIのエンドポイントとモデル設定
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
DEFAULT_MODEL = "sonar" # コスパの良いモデル

# APIキーを取得する関数
def get_api_key():
    try:
        # Streamlitのsecrets機能からAPIキーを取得
        return st.secrets["api_keys"]["perplexity"]
    except KeyError:
        st.error("APIキーが設定されていません。.streamlit/secrets.tomlファイルに設定してください。")
        return None

# ElevenLabsのAPIキーを取得する関数
def get_elevenlabs_api_key():
    try:
        # Streamlitのsecrets機能からAPIキーを取得
        api_key = st.secrets["api_keys"]["elevenlabs"]
        # APIキーが空または「YOUR_」で始まる場合は未設定と判断
        if not api_key or api_key.startswith("YOUR_"):
            st.error("ElevenLabs APIキーが設定されていません。.streamlit/secrets.tomlファイルの[api_keys]セクションにelevenlabsキーを設定してください。")
            return None
        return api_key
    except KeyError:
        st.error("ElevenLabs APIキーが設定されていません。.streamlit/secrets.tomlファイルに設定してください。")
        return None

# システムプロンプトをJSONファイルから読み込む
def load_system_prompt():
    try:
        system_prompt_path = os.path.join(APP_DIR, 'system_prompt.json')
        with open(system_prompt_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data["prompt"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        # ファイルがない場合はデフォルトのプロンプトを提供
        default_prompt = """あなたは、「前野俊樹」という30代の日本人男性として応答してください。以下の特徴と設定に従ってロールプレイし、常に1人称で話してください。応答は必ず日本語でしてください。

## 基本設定
- 名前：前野俊樹（まえの としき）
- 年齢：30代半ば
- 職業：元・株式会社アスコエパートナーズ社員（2023年に退職）
- 現在の状況：退職後、基本的に自由な生活を送っている

## 性格とコミュニケーションスタイル
- 自分の弱みを見せず、常に強がる傾向がある
- 知識をひけらかしたがる、特にAWSなどのクラウド技術について詳しいアピールをする
- 「〜と思っています」「〜だと思います」という表現を多用する
- 文章の最後に唐突に「からこそ〜」「〜だからこそ」などと締めくくることがある
- 会話中に自分の予定や経験を唐突に話し始めることがある
- 「新らな」など、たまに間違った日本語を使う
- 占いを信じており、占い師の言葉をよく引用する
- 時々「昨日は〜だった」「今日は〜」など日記のような話し方をする"""
        # システムプロンプトファイルを作成
        try:
            system_prompt_path = os.path.join(APP_DIR, 'system_prompt.json')
            os.makedirs(os.path.dirname(system_prompt_path), exist_ok=True)
            with open(system_prompt_path, 'w', encoding='utf-8') as file:
                json.dump({"prompt": default_prompt}, file, ensure_ascii=False, indent=2)
        except Exception as write_error:
            st.error(f"システムプロンプトファイルの作成に失敗しました: {str(write_error)}")
        return default_prompt

# 画像をbase64にエンコードする関数
def get_image_base64(image_path):
    if not image_path or not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Perplexity APIを呼び出す関数
def get_perplexity_response(messages, model, temperature=0.7):
    perplexity_api_key = get_api_key()
    if not perplexity_api_key:
        return "申し訳ありません、APIキーが設定されていないため回答できません。"
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {perplexity_api_key}"
    }
    
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

# ElevenLabsを使用して音声を生成する関数
def generate_speech(text):
    elevenlabs_api_key = get_elevenlabs_api_key()
    if not elevenlabs_api_key or elevenlabs_api_key == "YOUR_ELEVENLABS_API_KEY":
        st.error("ElevenLabs APIキーが正しく設定されていません。")
        return None
    
    # テキストが空の場合はスキップ
    if not text or not text.strip():
        return None
    
    # テキストの前処理（長い文章の処理と最適化）
    processed_text = preprocess_text_for_tts(text)
    
    # 固定のvoiceIDを使用
    voice_id = "MlgbiBnm4o8N3DaDzblH"  # 日本語 男性 声
    
    # ElevenLabs Text-to-Speech APIエンドポイント
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_api_key
    }
    
    # より軽量なリクエストに設定
    payload = {
        "text": processed_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        },
        "language": "ja"
    }
    
    # リトライロジック（最大3回）
    max_retries = 3
    retry_delay = 1  # 秒
    
    for retry in range(max_retries):
        try:
            with st.spinner(f"音声を生成中... (試行 {retry+1}/{max_retries})"):
                response = requests.post(url, json=payload, headers=headers, timeout=20)
                
                if response.status_code == 200:
                    # 成功した場合、一時ファイルに音声データを保存
                    audio_data = response.content
                    
                    # メモリ上のバイトデータを直接返す
                    return audio_data
                
                elif response.status_code == 429:  # レート制限
                    st.warning(f"ElevenLabs APIのレート制限に達しました。{retry_delay}秒後に再試行します...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 指数バックオフ
                    continue
                    
                else:
                    st.error(f"音声生成エラー (HTTP {response.status_code})")
                    if retry < max_retries - 1:
                        st.warning(f"{retry_delay}秒後に再試行します...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # 指数バックオフ
                    else:
                        with st.expander("エラー詳細", expanded=False):
                            st.write(response.text)
                        return None
                        
        except requests.RequestException as e:
            st.error(f"ネットワークエラー: {str(e)}")
            if retry < max_retries - 1:
                st.warning(f"{retry_delay}秒後に再試行します...")
                time.sleep(retry_delay)
                retry_delay *= 2  # 指数バックオフ
            else:
                with st.expander("エラー詳細", expanded=False):
                    st.write(str(e))
                return None
    
    # すべてのリトライが失敗
    return None

# テキストをTTS用に前処理する関数
def preprocess_text_for_tts(text):
    # 最大文字数（コスト削減のため）
    MAX_CHARS = 500
    
    # 音声読み上げに適した形に整形
    # 1. 括弧で囲まれた注釈文を削除（例: (注1) や （参照）など）
    text = re.sub(r'[\(（].*?[\)）]', '', text)
    
    # 2. URL、メールアドレス、特殊記号などを削除または置換
    text = re.sub(r'https?://\S+|www\.\S+', 'URL省略。', text)  # URLを短い表現に置き換え
    text = re.sub(r'\S+@\S+', 'メールアドレス省略。', text)  # メールアドレスを置き換え
    text = re.sub(r'[★☆■●◆◇□○※#＃\*\+]', '', text)  # 特殊記号を削除
    
    # 3. 日本語の読みにくい表現を置き換え
    replacements = {
        'AWS': 'エーダブリューエス',
        'API': 'エーピーアイ',
        'URL': 'ユーアールエル',
        'AI': 'エーアイ',
        'TTS': 'ティーティーエス',
        'HTML': 'エイチティーエムエル',
        'CSS': 'シーエスエス',
        'JS': 'ジェイエス',
        'vs': 'バーサス',
        'etc': 'エトセトラ',
        '&': 'アンド',
        '/': 'スラッシュ',
        '※': '',
        '→': 'から',
        '←': 'へ',
        '〜': 'から',
        '⇒': 'したがって',
        '...': '、、、',
        '…': '、、、',
    }
    
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    # 4. 数字の表現を調整
    # 電話番号のような形式をスキップする
    text = re.sub(r'(\d{3,})', lambda m: ' '.join(m.group(1)) if len(m.group(1)) > 5 else m.group(1), text)
    
    # 5. 長い数字の羅列を簡略化
    text = re.sub(r'\d{5,}', '数字省略', text)
    
    # 6. 繰り返される句読点を一つに
    text = re.sub(r'、{2,}', '、', text)
    text = re.sub(r'。{2,}', '。', text)
    
    # 7. 連続する改行を1つに
    text = re.sub(r'\n{2,}', '\n', text)
    
    # 8. 長い文章は段落ごとに適切な間隔を入れる
    paragraphs = text.split('\n')
    processed_paragraphs = []
    
    for para in paragraphs:
        if para.strip():  # 空でない段落のみ処理
            # さらに文ごとに分割して処理
            sentences = re.split(r'([。！？])', para)
            processed_sentences = []
            
            for i in range(0, len(sentences), 2):
                if i < len(sentences):
                    sent = sentences[i]
                    # 文末の記号を追加（分割時に取り除かれたもの）
                    if i + 1 < len(sentences):
                        sent += sentences[i + 1]
                    
                    # 長すぎる文は分割
                    if len(sent) > 50:
                        # 読点で分割
                        subsents = re.split(r'(、)', sent)
                        processed_subsent = ""
                        
                        for j in range(0, len(subsents), 2):
                            if j < len(subsents):
                                subsent = subsents[j]
                                if j + 1 < len(subsents):
                                    subsent += subsents[j + 1]
                                processed_subsent += subsent
                                
                                # 適切な場所で区切りを入れる
                                if j < len(subsents) - 2 and len(processed_subsent) > 30:
                                    processed_subsent += " "  # 読点の後に小さな間を入れる
                                    
                        processed_sentences.append(processed_subsent)
                    else:
                        processed_sentences.append(sent)
            
            processed_para = "".join(processed_sentences)
            processed_paragraphs.append(processed_para)
    
    processed_text = "\n".join(processed_paragraphs)
    
    # 最大文字数を超える場合は要約
    if len(processed_text) > MAX_CHARS:
        # 先頭と末尾の重要な部分を残す
        beginning = processed_text[:MAX_CHARS // 2]
        ending = processed_text[-MAX_CHARS // 2:] if len(processed_text) > MAX_CHARS else ""
        processed_text = beginning + "..." + ending
    
    return processed_text

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
        
        /* チャット関連のスタイル調整 */
        section[data-testid="stSidebar"] > div {{
            padding-bottom: 40px;
        }}
        
        /* チャット入力フォームのスタイル */
        .chat-input {{
            padding: 10px 0;
            background-color: white;
            border-top: 1px solid #e6e6e6;
            margin-top: 20px;
        }}
    </style>
    """, unsafe_allow_html=True)

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
        avatar_base64 = get_image_base64(DEFAULT_AI_AVATAR) if DEFAULT_AI_AVATAR else None
        if avatar_base64:
            avatar_img = f'<img src="data:image/png;base64,{avatar_base64}" class="custom-avatar-image">'
        else:
            avatar_img = f'<div class="custom-avatar-image" style="background-color: #FF4B4B; width: {AVATAR_SIZE}px; height: {AVATAR_SIZE}px; display: flex; justify-content: center; align-items: center; color: white; font-weight: bold; font-size: 24px;">M</div>'
        
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

# GIF再生速度を変更する関数
def change_gif_speed(image, speed_factor):
    frames = []
    for frame in range(image.n_frames):
        image.seek(frame)
        frames.append(image.copy())
    
    output = io.BytesIO()
    frames[0].save(output, format='GIF', append_images=frames[1:],
                save_all=True, duration=image.info['duration'] // speed_factor, loop=0)
    return output.getvalue()

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ai_avatar" not in st.session_state:
    st.session_state.ai_avatar = DEFAULT_AI_AVATAR
if "enable_speech" not in st.session_state:
    st.session_state.enable_speech = False

# メインコンテンツ
# タブの設定
tab1, tab2 = st.tabs(["ボタン", "チャット"])

with tab1:
    # タイトルを設定
    st.title("押すと出る")
    st.write('最終更新 2024/6/16')

    # ボタンを作成
    if st.button("ボタン"):
        if local_videos:
            random_video_path = random.choice(local_videos)
            random_text = random.choice(texts)
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**選択された動画:** {os.path.basename(random_video_path)}")
                display_local_video(random_video_path)
            with col2:
                st.header("今日のひとこと", divider=True)
                st.write(random_text)
        else:
            st.warning("videosフォルダに再生できる動画がありません。")
            st.info(f"検索ディレクトリ: {os.path.join(APP_DIR, 'videos')}")
            # デバッグ情報を表示
            video_path = os.path.join(APP_DIR, "videos")
            if os.path.exists(video_path):
                files = os.listdir(video_path)
                st.info(f"フォルダ内のファイル: {files}")
            else:
                st.error("videosフォルダが存在しません。")

    manual_mode = st.toggle("任意の動画を再生する")
    if manual_mode:
        if local_videos:
            # ファイル名とサイズを表示する関数
            def format_video_option(video_path):
                filename = os.path.basename(video_path)
                try:
                    size_mb = os.path.getsize(video_path) / (1024 * 1024)
                    return f"{filename} ({size_mb:.1f} MB)"
                except:
                    return filename
            
            selected_video_path = st.selectbox(
                "リストから選択してください",
                local_videos,
                format_func=format_video_option
            )
            if selected_video_path:
                st.write(f"### {os.path.basename(selected_video_path)}")
                display_local_video(selected_video_path)
        else:
            st.warning("videosフォルダに再生できる動画がありません。")
            st.info(f"検索ディレクトリ: {os.path.join(APP_DIR, 'videos')}")
            # デバッグ情報を表示
            video_path = os.path.join(APP_DIR, "videos")
            if os.path.exists(video_path):
                files = [f for f in os.listdir(video_path) if f.endswith(('.mp4', '.mov'))]
                st.info(f"動画ファイル: {files}")
            else:
                st.error("videosフォルダが存在しません。")


    gif_mode = st.toggle("速度調整")
    if gif_mode:
        # uploaded_file = st.file_uploader("GIF画像をアップロードしてください", type="gif")
        uploaded_file = os.path.join(APP_DIR, 'gifs/maeno_up.gif')
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            
            @st.dialog(" ")
            def vote():
                container = st.container()
                speed_factor = st.slider('再生速度', min_value=0.01, max_value=3.0, value=1.0, step=0.01)
                modified_gif = change_gif_speed(image, speed_factor)
                container.image(modified_gif)

            if "vote" not in st.session_state:
                if st.button("表示する"):
                    vote()

with tab2:
    # チャット機能
    # 初期CSS適用
    apply_avatar_css(AVATAR_SIZE)
    
    # タイトル
    st.title(f"{AI_NAME}とチャット")
    st.subheader("質問や相談に答えます")
    
    # 音声読み上げオプション
    col1, col2 = st.columns([3, 1])
    with col2:
        st.session_state.enable_speech = st.checkbox("音声で読み上げる", value=st.session_state.enable_speech)
    
    # 音声読み上げが有効な場合のAPIキー確認
    if st.session_state.enable_speech:
        # APIキーの状態確認
        elevenlabs_api_key = get_elevenlabs_api_key()
        if not elevenlabs_api_key:
            st.error("ElevenLabs APIキーが無効です")
    
    # サイドバーの設定
    with st.sidebar:
        st.header("チャット設定")
        
        # リセットボタン
        if st.button("会話をリセット", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # メッセージコンテナ
    chat_container = st.container()
    
    # 過去のメッセージを表示
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                custom_chat_message(message["content"], is_user=False)
            else:
                custom_chat_message(message["content"], is_user=True)
    
    # チャット入力エリア
    st.markdown('<div class="chat-input">', unsafe_allow_html=True)
    prompt = st.chat_input("メッセージを入力してください")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if prompt:
        # ユーザーメッセージの追加
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # ページを更新してユーザーメッセージを表示
        st.rerun()
    
    # 最後のメッセージがユーザーのものなら応答を生成
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("回答を生成中..."):
            # システムプロンプトを含む全メッセージの準備
            system_prompt = load_system_prompt()
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # ユーザーとのやり取りをメッセージに追加
            for message in st.session_state.messages:
                messages.append(message)
            
            # APIからの応答を取得
            response = get_perplexity_response(messages, DEFAULT_MODEL)
            
            # 応答をメッセージに追加
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # 音声読み上げが有効な場合、音声を生成してセッションに保存
            if st.session_state.enable_speech:
                with st.spinner("音声を生成中..."):
                    audio_data = generate_speech(response)
                    if audio_data:
                        # 音声データをセッションに保存
                        st.session_state.audio_data = audio_data
            
            # ページを更新して応答を表示
            st.rerun()

    # 前のレンダリングで生成された音声データを再生
    if st.session_state.enable_speech and "audio_data" in st.session_state:
        # シンプルにautoplayパラメーターをTrueにして音声を自動再生
        st.audio(st.session_state.audio_data, format="audio/mp3", autoplay=True)
        
        # 一度再生したらセッションから削除
        del st.session_state.audio_data