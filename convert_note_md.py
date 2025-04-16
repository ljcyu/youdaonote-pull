#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import argparse
from core import log
from core.covert import YoudaoNoteConvert

def init_args():
    """初始化命令行参数"""
    parser = argparse.ArgumentParser(description='递归转换 .note 文件为 Markdown 格式')
    parser.add_argument('dir_path', nargs='?', default=os.getcwd(),
                        help='要处理的目录路径，默认为当前目录')
    return parser.parse_args()

def convert_note_files(dir_path):
    """递归遍历目录，转换所有 .note 文件为 Markdown"""
    converted_count = 0
    failed_count = 0
    
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.note'):
                file_path = os.path.join(root, file)
                logging.info(f"正在转换文件: {file_path}")
                
                try:
                    # 尝试使用 HTML 转换方法
                    YoudaoNoteConvert.covert_html_to_markdown(file_path)
                    # 转换成功后删除原始 .note 文件
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logging.info(f"已删除原始文件: {file_path}")
                    converted_count += 1
                    logging.info(f"成功转换: {file_path}")
                except Exception as e:
                    failed_count += 1
                    logging.error(f"转换失败: {file_path}, 错误: {str(e)}")
    
    return converted_count, failed_count

def main():
    """主函数"""
    log.init_logging()
    args = init_args()
    dir_path = args.dir_path
    
    if not os.path.exists(dir_path):
        logging.error(f"目录不存在: {dir_path}")
        sys.exit(1)
    
    if not os.path.isdir(dir_path):
        logging.error(f"指定路径不是目录: {dir_path}")
        sys.exit(1)
    
    logging.info(f"开始处理目录: {dir_path}")
    converted_count, failed_count = convert_note_files(dir_path)
    
    logging.info(f"处理完成! 成功转换: {converted_count} 个文件, 失败: {failed_count} 个文件")

if __name__ == "__main__":
    main()