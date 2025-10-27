import pandas as pd
import plotly.express as px

# 1. 定义文件路径
file_path_central = "/Users/wuyueyi/Desktop/some_filllle/2025科研/数据集/科研绘图/其他/脱敏/centra_merged_all.csv"
file_path_huaxi = "/Users/wuyueyi/Desktop/some_filllle/2025科研/数据集/科研绘图/其他/脱敏/huaxi_merged_all.csv"

# 2. 读取数据并合并
try:
    df_central = pd.read_csv(file_path_central)
    df_huaxi = pd.read_csv(file_path_huaxi)
    df_combined = pd.concat([df_central, df_huaxi], ignore_index=True)
except FileNotFoundError as e:
    print(f"错误：无法找到文件。请检查文件路径是否正确。详细信息：{e}")
    exit()

# 3. 清理 'age' 列并进行分组
df_combined['age'] = pd.to_numeric(
    df_combined['age'].astype(str).str.extract(r'(\d+)', expand=False),
    errors='coerce'
)

age_bins = [0, 20, 30, 40, 50, 60, 70, 80, 100]
age_labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81+']

# 年龄段顺序（内圈）
ordered_age_labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81+']

df_combined['Age Group'] = pd.cut(
    df_combined['age'],
    bins=age_bins,
    labels=age_labels,
    right=False,
    ordered=True
)
df_combined['Age Group'] = pd.Categorical(
    df_combined['Age Group'],
    categories=ordered_age_labels,
    ordered=True
)

# 让外圈 measure 也变成有序分类（顺时针顺序按下面这个列表）
desired_measure_order = ['negative', 'non-emergency-positive', 'positive']
# 只保留数据里实际存在的类别顺序，避免出现 NaN
present_measures = [m for m in desired_measure_order if m in df_combined['measure'].astype(str).unique()]
df_combined['measure'] = pd.Categorical(
    df_combined['measure'].astype(str),
    categories=present_measures,
    ordered=True
)

# 4. 定义年龄组的颜色映射
age_colors_map = {
    '0-20': '#942C32',      # 最深的红色
    '21-30': '#A34F47',    # 红色
    '31-40': '#B27266',   # 中红色
    '41-50': '#C79E92',  # 浅粉色
    '51-60': '#7689A6',  # 浅蓝色
    '61-70': '#96A3B9',  # 中蓝色
    '71-80': '#B9C1CD',   # 深蓝色
    '81+':  '#E9EFF5'       # 最深的蓝色
}

# 5. 创建旭日图
fig = px.sunburst(
    df_combined.dropna(subset=['Age Group', 'measure']),
    path=['Age Group', 'measure'],
    title='患者年龄与测量结果分布',
    color='Age Group',
    color_discrete_map=age_colors_map
)

# 关键：禁止按数值自动排序，严格按分类顺序（顺时针）排布
fig.update_traces(sort=False)

fig.update_layout(
    hoverlabel=dict(
        font_size=24,                 # 整体字号
        font_family='Comic Sans MS, sans-serif',
        bgcolor=None,
        bordercolor=None            # 边框更清晰，可选
    )
)

# 6. 更新布局和字体样式
fig.update_layout(
    title=dict(
        text='<b>患者年龄与测量结果分布</b>',
        font=dict(size=24, family='Comic Sans MS, sans-serif')
    ),
)
fig.update_traces(
    insidetextfont=dict(
        size=20,
        family='Comic Sans MS, sans-serif'
    ),
    hovertemplate='<span style="font-size: 16px;"><b>%{label}</b><br><b>Count: %{value}</b><br><b>Percentage: %{percentEntry:.1%}</b></span>'
)

fig.write_html("sunburst_age_measure.html", auto_open=True)
