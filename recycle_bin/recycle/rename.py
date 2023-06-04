import os

folder_path = "../result/result_cv/60_nodes"
for i in range(1, 10):
	old_name = os.path.join(folder_path, "d60_" + str(i) + ".csv")
	new_name = os.path.join(folder_path, "d60_0" + str(i) + ".csv")
	os.rename(old_name, new_name)
	print(new_name)
