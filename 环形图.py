import pandas as pd
import plotly.express as px


# 1. 定义文件路径
# 请确保这些路径是正确的
file_path_central = "/Users/wuyueyi/Desktop/some_filllle/2025科研/数据集/科研绘图/其他/脱敏/centra_merged_all.csv"
file_path_huaxi = "/Users/wuyueyi/Desktop/some_filllle/2025科研/数据集/科研绘图/其他/脱敏/huaxi_merged_all.csv"

# 2. 读取数据并添加医院名称列
try:
    df_central = pd.read_csv(file_path_central)
    df_central['Hospital'] = 'Central Hospital'
    
    df_huaxi = pd.read_csv(file_path_huaxi)
    df_huaxi['Hospital'] = 'West China Medical Center'
    
except FileNotFoundError as e:
    print(f"错误：无法找到文件。请检查文件路径是否正确。详细信息：{e}")
    exit()

# 3. 合并两个数据集
df_combined = pd.concat([df_central, df_huaxi], ignore_index=True)

# 4. 清理 'age' 列
df_combined['age'] = pd.to_numeric(
    df_combined['age'].astype(str).str.extract('(\d+)', expand=False),
    errors='coerce'
)

# 5. 对年龄数据进行分组
age_bins = [0, 20, 30, 40, 50, 60, 70, 80, 100]
age_labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81+']

df_combined['Age Group'] = pd.cut(df_combined['age'], bins=age_bins, labels=age_labels, right=False)

# 6. 定义颜色方案
central_color = '#942C32'
huaxi_color = '#5B7899'

color_map = {
    'Central Hospital': central_color,
    'West China Medical Center': huaxi_color
}

# 7. 创建并显示旭日图，并设置字体加粗
fig = px.sunburst(
    df_combined.dropna(subset=['Age Group']), 
    path=['Hospital', 'Age Group'], 
    title='患者年龄分布：不同医院的对比',
    color='Hospital', 
    color_discrete_map=color_map,
)

fig.update_layout(
    hoverlabel=dict(
        font_size=24,                 # 整体字号
        font_family='Comic Sans MS, sans-serif',
        bgcolor=None,
        bordercolor=None            # 边框更清晰，可选
    )
)

# 8. 更新所有可定制的字体样式
fig.update_layout(
    # 加粗标题
    title=dict(
        text='<b>患者年龄分布：不同医院的对比</b>',
        font=dict(size=24, family='Arial, sans-serif') 
    ),
    # 加粗图例的字体（如果图表有图例的话）
    legend=dict(
        font=dict(family='Comic Sans MS, sans-serif')
    )
)

fig.update_traces(
    # 加粗并增大扇形内部标签的字体
    insidetextfont=dict(
        size=20, 
        family='Comic Sans MS, sans-serif'
    ),
    # 增加外部文本字体大小（如果设置了show_text="outer"的话）
    textfont=dict(
        size=20, 
        family='Comic Sans MS, sans-serif'
    ),
    # 使用HTML标签加粗并放大悬浮框内的文本
    hovertemplate='<span style="font-size: 16px; font-family: Arial, sans-serif;"><b>%{label}</b><br><b>Count: %{value}</b><br><b>Percentage: %{percentEntry:.1%}</b></span>'
)

fig.write_html("sunburst_age_measure.html", auto_open=True)