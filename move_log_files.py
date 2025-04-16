import os
import re
import shutil
import argparse
import logging

def move_log_files(src_dir):
    # 匹配 2013-1xxx.md 或 2013-12xxx.md 这样的文件名
    pattern = re.compile(r'^(?P<year>\d{4})-(?P<month>\d{1,2})[^\d]?.*\.md$', re.IGNORECASE)
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            match = pattern.match(file)
            if match:
                year = match.group('year')
                month = match.group('month').zfill(2)
                # 构造目标目录
                target_dir = os.path.join(src_dir, f"{year}日志", f"{year}{month}")
                os.makedirs(target_dir, exist_ok=True)
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                # 如果源文件和目标文件路径不同才移动
                if os.path.abspath(src_file) != os.path.abspath(dst_file):
                    logging.info(f"原路径: {src_file} -> 目标路径: {dst_file}")
                    shutil.move(src_file, dst_file)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        filename="move_log_files.log",  # 日志输出到当前目录下的 move_log_files.log 文件
        filemode="w" ,
        encoding="utf-8"
    )
    parser = argparse.ArgumentParser(description="整理日志文件到对应目录")
    parser.add_argument("dir", help="要整理的目录")
    args = parser.parse_args()
    move_log_files(args.dir)
