import re
from datetime import datetime
from pathlib import Path
import sys
import subprocess as sps
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def update_datetime_in_file(file_path):
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if not file_path.exists():
        return
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    match = re.search(
        r'^---\s*(.*?)\s*---', content, re.DOTALL | re.MULTILINE
        )
    if match:  # 匹配到 YAML 块
        date_pattern = re.compile(r'(date\s*:\s*)\S+')
        yaml_block = match.group(1)

        if not date_pattern.search(yaml_block):
            print(f"File[ {file_path} ]", ": No date found.")
            return
        # 在 YAML 块内查找并替换 date 值
        new_yaml_block = re.sub(
            date_pattern, f'date: {current_date}', yaml_block
            )
        # new_yaml_block = date_pattern.sub(
        #     rf'\g<1>{current_date}', yaml_block
        #     )

        # 将更新后的 YAML 块放回原内容
        new_content = content.replace(
            match.group(0), f'---\n{new_yaml_block}\n---'
            )

        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"File[ {file_path} ]", ": Date updated successfully.")
    else:
        print(f"File[ {file_path} ]", ": No YAML block found.")


def get_modified_files():
    raw = sps.run(
        "git status --porcelain",
        # shell=True,
        capture_output=True
        ).stdout.decode()
    f_list = [s[3:] for s in raw.split('\n') if s.endswith('.html')]
    # print(f_list)
    return f_list


if __name__ == '__main__':
    print("\n更新已修改文件的日期", sys.argv)
    f_list = get_modified_files()
    ROOT = Path('./pages/')
    # for path_doc in ROOT.rglob('*.md'):
    for f_name in f_list:
        path_doc = re.sub(
            '\.html$', '.md', str(Path(f_name).relative_to('./docs'))
            )
        update_datetime_in_file(path_doc)
