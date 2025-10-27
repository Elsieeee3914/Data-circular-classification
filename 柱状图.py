import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


import matplotlib.font_manager as fm

# ===== 设置 Comic Sans MS 字体 =====
# macOS 下 Comic Sans MS 的默认路径如下：
comic_path = "/Library/Fonts/Comic Sans MS.ttf"

# 检查字体文件是否存在
if not fm.findfont("Comic Sans MS", fallback_to_default=False):
    fm.fontManager.addfont(comic_path)

plt.rcParams['font.family'] = 'Comic Sans MS'
plt.rcParams['font.sans-serif'] = ['Comic Sans MS']
plt.rcParams['axes.unicode_minus'] = False  # 防止负号显示问题



# === 模仿示例代码的配色方案和样式 ===
male_color = '#942C32'
female_color = '#5B7899'

def style_axes(ax, title_text, ylabel_text):
    """一个通用的函数来美化坐标轴和标题。"""
    # 移除标题前面的额外文本，使用 set_title 替代
    # 调整标题文本以匹配您在调用中传入的值
    ax.set_title(title_text, loc='left', fontdict={'weight': 'bold', 'fontsize': 14})
    ax.set_ylabel(ylabel_text, fontdict={'weight': 'bold'})
    
    # 移除顶部和右侧的边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 调整左侧和底部的边框样式
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    
    # 设置刻度线向外，并调整其粗细和长度
    ax.tick_params(axis='both', direction='out', length=5, width=1.5)
    
    # 调整字体大小
    # ax.set_xlabel(ax.get_xlabel(), fontdict={'weight': 'bold'}) # 这里的get_xlabel可能为空，避免重复设置
    ax.set_ylabel(ax.get_ylabel(), fontdict={'weight': 'bold'})
    ax.tick_params(axis='both', labelsize=10)
    
    ax.tick_params(axis='both', labelsize=10, width=1.5)  # 保留已有
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontweight('bold')  # 加粗刻度文字


# 你的文件路径 (请根据你的实际路径调整)
# 注意：我在本地无法访问你的文件系统，所以使用一个虚拟路径和随机数据来保证代码可运行
# 请确保你的文件路径是正确的
file_path = '/Users/wuyueyi/Desktop/some_filllle/2025科研/数据集/科研绘图/其他/脱敏/your_file_with_time_date.csv'

# 为了保证代码可运行，我创建一个虚拟数据框
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"警告: 找不到文件 {file_path}，使用随机虚拟数据代替。")
    # 创建虚拟数据
    N = 1000
    np.random.seed(42)
    df = pd.DataFrame({
        'time_date': pd.to_datetime(pd.date_range(start='2023-01-01', periods=N, freq='D').to_series().sample(N, replace=True).sort_values().tolist()),
        'age': np.random.randint(15, 80, N),
        'sex': np.random.choice(['男', '女'], size=N) # 假设您的数据使用 '男', '女'
    })


# 数据预处理
# 确保 'time_date' 列是日期格式
df['time_date'] = pd.to_datetime(df['time_date'])

# 根据 'sex' 列拆分数据
male_data = df[df['sex'] == '男']
female_data = df[df['sex'] == '女']

# --- Part A: 按年龄分组的图表（使用你的 CSV 数据）---
male_age_data = male_data['age'].dropna()
female_age_data = female_data['age'].dropna()

# 计算直方图数据
bins = np.arange(0, 101, 1)
hist_male, _ = np.histogram(male_age_data, bins=bins)
hist_female, _ = np.histogram(female_age_data, bins=bins)

# --- Part B: 按时间分组的图表（使用你的 CSV 数据）---
# 按月统计男性和女性的数据数量
df_time = df.groupby([pd.Grouper(key='time_date', freq='M'), 'sex']).size().unstack(fill_value=0)
dates = df_time.index
male_time_data = df_time['男']
female_time_data = df_time['女']

# --- 开始绘制图表 ---
# 关键修改：移除 constrained_layout=True，以便手动设置间距
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6)) # 调整 figsize 可能会有帮助

# 第一个子图 (a) - 年龄分布
width = 0.8
ax1.bar(bins[:-1], hist_male, width=width, color=male_color, label='Male')
ax1.bar(bins[:-1], hist_female, width=width, bottom=hist_male, color=female_color, label='Female')
ax1.set_xlabel('Age')
ax1.set_ylabel('Number')
ax1.set_title('a', loc='left', fontdict={'weight': 'bold'})
ax1.legend(
    loc='upper right',
    bbox_to_anchor=(1, 1.15),
    frameon=False,
    prop={'weight': 'bold', 'size': 10}
)
ax1.set_ylim(0, max(hist_male + hist_female) * 1.1)
style_axes(ax1, 'a. Age Distribution ', 'Number')

# 第二个子图 (b) - 时间分布
ax2.bar(dates, male_time_data, color=male_color, label='Male', width=15)
ax2.bar(dates, female_time_data, bottom=male_time_data, color=female_color, label='Female', width=15)
ax2.set_xlabel('Time')
ax2.set_ylabel('Number')
ax2.set_title('b', loc='left', fontdict={'weight': 'bold'})
ax2.legend(
    loc='upper right',
    bbox_to_anchor=(1, 1.15),
    frameon=False,
    prop={'weight': 'bold', 'size': 10}
)

ax2.set_ylim(0, max(male_time_data + female_time_data) * 1.1)
style_axes(ax2, 'b. Time Distribution', 'Number')

# 调整X轴日期格式
ax2.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
ax2.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=2))
plt.xticks(rotation=45, ha='right')

# 关键修改：使用 fig.subplots_adjust 来手动设置子图间距，让右边的图向右移动
# wspace (width space) 是子图之间的水平间距比例。
# 默认值可能在 0.2 左右，增加到 0.35 或 0.4 会明显增大间距。
fig.subplots_adjust(wspace=0.25) 
plt.show()