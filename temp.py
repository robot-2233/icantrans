#encoding:gbk
import pandas as pd

input_file = 'raw_data/datasets.csv'
output_file = 'raw_data/dataset.csv'

# ��ȡԭʼCSV�ļ�
df = pd.read_csv(input_file)

# ��������
half_df = df.iloc[:len(df) // 4]

# �����д���µ�CSV�ļ�
half_df.to_csv(output_file, index=False)

print(f"ԭʼ�ļ�����: {len(df)}")
print(f"���ļ�����: {len(half_df)}")