import matplotlib.pyplot as plt
import japanize_matplotlib  # 日本語フォント対応ライブラリ（環境に合わせて設定してください）

# データ定義
labels = ['夕食', '朝食', 'その他\n(宿泊・飲料・売店等)']
sizes = 
colors = ['#ff9999', '#66b3ff', '#99ff99']  # 色の設定

# 円グラフの作成
fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                  startangle=90, colors=colors,
                                  counterclock=False, shadow=True)

# テキストのスタイル設定
plt.setp(texts, size=12)
plt.setp(autotexts, size=12, color="white", weight="bold")

# タイトルの追加
plt.title('売上構成比（期間：2026/01/02 ～ 2026/02/01）', fontsize=14)
plt.text(0, -1.3, '※総売上 1,014,588円 に対する割合', ha='center', fontsize=10)

# 表示
plt.show()
