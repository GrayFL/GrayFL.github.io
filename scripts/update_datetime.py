import re
from datetime import datetime
from pathlib import Path
import sys


def update_datetime_in_file(file_path):
    if isinstance(file_path, str):
        file_path = Path(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    match = re.search(
        r'^---\s*(.*?)\s*---', content, re.DOTALL | re.MULTILINE
        )
    if match:
        yaml_block = match.group(1)
        # 在 YAML 块内查找并替换 date 值
        new_yaml_block = re.sub(
            r'date\s*:\s*\S+', f'date: {current_date}', yaml_block
            )

        date_pattern = re.compile(r'(date\s*:\s*)\S+')
        new_yaml_block = date_pattern.sub(
            rf'\g<1>{current_date}', yaml_block
            )

        # 将更新后的 YAML 块放回原内容
        new_content = content.replace(
            match.group(0), f'---\n{new_yaml_block}\n---'
            )

        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print("Date updated successfully.")
    else:
        print("No YAML block found.")


if __name__ == '__main__':
    print(sys.argv)
    update_datetime_in_file('pages/info.md')
