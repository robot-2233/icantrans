#encoding:gbk
import pandas as pd

input_file = 'raw_data/datasets.csv'
output_file = 'raw_data/dataset.csv'

# 读取原始CSV文件
df = pd.read_csv(input_file)

# 减半行数
half_df = df.iloc[:len(df) // 4]

# 将结果写回新的CSV文件
half_df.to_csv(output_file, index=False)

print(f"原始文件行数: {len(df)}")
print(f"新文件行数: {len(half_df)}")