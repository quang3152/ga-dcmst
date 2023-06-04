import pandas as pd

# Đọc file csv và chỉ định các cột cần đọc
df = pd.read_csv('result_nk/90_nodes/d90_3.csv', usecols=['STT', 'Best Solution', 'Best Tree', 'Time'])

# Lưu các cột đã chọn vào file csv mới
df.to_csv('result_nk/90_nodes/d90_3_new.csv', index=False)
