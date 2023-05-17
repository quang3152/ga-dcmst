import pandas as pd
import random
import os


def gen_data(path, number_of_line, loop):
    # Đọc file csv
    df = pd.read_csv(path)
    for i in range(loop):
        # Lấy ngẫu nhiên n dòng
        sample_df = df.sample(number_of_line)
        # Đánh số lại city
        sample_df = sample_df.reset_index(drop=True)
        sample_df['city'] = sample_df.index
        file_name = path.split("/")[-1]
        # file_name = str(i+1) + "_" + str(number_of_line) + "_" + file_name
        file_name = "d" + str(number_of_line) + "_" + str(i+1) + ".csv"
        sample_df = sample_df.drop_duplicates()

        folder_name = str(number_of_line) + "_nodes"
        if not os.path.exists("data/" + folder_name):
            os.mkdir("data/" + folder_name)
        # Lưu kết quả vào file csv mới
        new_path = "data/" + folder_name + "/" + file_name
        sample_df.to_csv(new_path, index=False)


# gen_data("data/fi10k.csv", 15, 30)
# gen_data("data/fi10k.csv", 30, 30)
# gen_data("data/fi10k.csv", 60, 30)
# gen_data("data/fi10k.csv", 90, 30)
gen_data("data/fi10639.csv", 8, 30)

