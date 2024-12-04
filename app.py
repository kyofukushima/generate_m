import streamlit as st
import random
import os

# GIFとテキストのリストを用意
gifs = [
    "images/muscle_maeno.gif",
    "images/spalta_maeno.gif",
    "images/SPOILER_capcut_test.gif",
    "images/SPOILER_maeno_oogiri.gif"
]
videos = [
    'videos/gay_maeno.MP4',
    'videos/jedi_maeno.MP4',
    'videos/SPOILER_capcut_test.mov',
    'videos/SPOILER_maeno_oogiri.mov',
    'videos/muscle_maeno.mov',
    'videos/spalta_maeno.mov',
    'videos/sw1.mp4',
    'videos/mask_maeno.mp4',

]
videos = list(os.listdir('videos'))

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
ストレージもいつでも拡張出来たり、バックアップも取得出来ったり、コンソール画面で
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

# タイトルを設定
st.title("押すと出る")
st.write('最終更新 2024/12/4')

# ボタンを作成
if st.button("ボタン"):
    # ランダムにGIFとテキストを選択
    # random_gif = random.choice(gifs)
    random_video = random.choice(videos)
    random_text = random.choice(texts)
    col1, col2 = st.columns(2)
    with col1:
        # GIFを表示
        # st.image(random_gif)
        st.video(f'videos/{random_video}',autoplay=True,loop=True)
    with col2:
        st.header("今日のひとこと", divider=True)
        # テキストを表示
        st.write(random_text)

manual_mode = st.toggle("任意の動画を再生する")
if manual_mode:
    selected_video = st.selectbox("リストから選択してください",videos,)
    st.video(f'videos/{selected_video}')
