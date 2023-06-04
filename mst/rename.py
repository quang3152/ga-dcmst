import os

folder_path = 'result_nk/15_nodes'  # đường dẫn đến thư mục chứa các file cần đổi tên
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        old_name = os.path.join(folder_path, filename)
        parts = filename.split('_')
        # print(parts)
        # print(parts[0], len(parts[0]))
        if len(parts[0]) == 1:
            parts[0] = "0" + parts[0]
        new_name = 'd{}_{}.csv'.format(parts[1], parts[0])
        print(new_name)
        new_name = os.path.join(folder_path, new_name)
        os.rename(old_name, new_name)
