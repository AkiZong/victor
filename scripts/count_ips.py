import os
import chardet
import re
from collections import Counter
import pandas as pd

DATA = []
OUTOUT_FILE_TXT = "ip出现次数.txt"
OUTOUT_FILE_EXCEL = "ip出现次数.xlsx"

def get_ips():
    log_dir = os.path.join(os.getcwd(), "log")
    log_files = os.listdir(log_dir)
    for log_file in log_files:
        if log_file.endswith(".log"):
            log_file_path = os.path.join(log_dir, log_file)
            parse_log_file(log_file_path)


def parse_log_file(file_path):
    global DATA
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    with open(file_path, "r", encoding=encoding) as f:
        raw_data = f.readlines()
        for line in raw_data:
            pattern = r'机器码:\w* IP:[\w\.]*'
            matches = re.findall(pattern, line)
            if matches:
                DATA.append(matches[0])


def write_to_file(file_format="txt"):
    output_file = OUTOUT_FILE_TXT
    count = Counter(DATA)
    sorted_count = count.most_common()
    if file_format == "excel":
        output_file = OUTOUT_FILE_EXCEL
        # write to excel
        df = pd.DataFrame(sorted_count, columns=['Item', 'Count'])
        df.to_excel(output_file, index=False)
    elif file_format == "txt":
        with open(output_file, "w") as file:
            for item in sorted_count:
                print("出现次数：{} {}".format(
                    (str(item[1]) + ",").ljust(10), item[0]))
                file.write("出现次数：{} {}".format(
                    (str(item[1]) + ",").ljust(8), item[0]) + "\n")
    print("数据已写入文件<{}>".format(output_file))


if __name__ == "__main__":
    os.system("pip3 install -r requirements.txt")
    get_ips()
    write_to_file()
