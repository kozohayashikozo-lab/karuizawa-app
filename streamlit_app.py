import matplotlib.pyplot as plt
import pandas as pd

# データの読み込み
df = pd.read_csv('ｵﾘｯｸｽｳﾞｨﾗ.xlsx - ｵﾘｯｸｽｳﾞｨﾗ.csv')

# グラフ作成
fig, ax1 = plt.subplots(figsize=(10, 6))

# 売上高（棒グラフ）
ax1.bar(df['月'], df['売上高'], color='skyblue', label='売上高', alpha=0.7)
ax1.set_xlabel('Month')
ax1.set_ylabel('Revenue (Yen)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# 外注費（折れ線グラフ）
ax2 = ax1.twinx()
ax2.plot(df['月'], df['外注費'], color='red', marker='o', label='外注費', linewidth=2)
ax2.set_ylabel('Outsourcing Cost (Yen)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.title('Revenue vs Outsourcing Costs (Orix Villa)')
fig.tight_layout()

# 保存
plt.savefig('orix_villa_analysis.png')
