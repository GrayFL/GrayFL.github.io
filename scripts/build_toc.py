# -*- coding: utf-8 -*-

import re
from pathlib import Path
import sys
import yaml
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 将文件路径按照字典形式递归存储，


class SafeDumperWithOrder(yaml.SafeDumper):
    pass


def dict_representer(dumper: yaml.SafeDumper, data: dict):
    return dumper.represent_mapping(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items()
        )


SafeDumperWithOrder.add_representer(dict, dict_representer)


def recursive_iterate(pages: list, path: Path):
    for file in path.iterdir():
        if file.is_file() and file.suffix == '.md':
            with open(file, 'r', encoding='utf-8') as f:
                fr = f.readline()  # 读取第一行
                if fr.startswith('---'):
                    for _ in range(30):
                        fr = f.readline()
                        match = re.match(r'^title\s*:\s*(.*)$', fr)
                        if fr.startswith('---'):
                            pages.append({
                                'text': file.stem, 'href': str(file)
                                })
                            break
                        elif match:
                            pages.append(str(file))
                            break
                else:
                    pages.append({'text': file.stem, 'href': str(file)})

        elif file.is_dir():
            directory = {
                'section':
                    re.match(r'^(?:\d+\.?\d*-)?(.*)$', file.name).group(1),
                'contents': []
                }
            recursive_iterate(directory['contents'], file)
            if directory['contents']:
                # 如果文件夹收录内容空，则删除该文件夹
                pages.append(directory)


def yaml_dumps(pages: list):
    f = io.StringIO()
    yaml.dump(
        pages,
        f,
        encoding='utf-8',
        allow_unicode=True,
        Dumper=SafeDumperWithOrder
        )
    data = f.getvalue()
    f.close()
    return data


if __name__ == '__main__':
    print("\n更新总目录", sys.argv)
    ROOT = Path('./pages/')
    PAGES = []
    recursive_iterate(PAGES, ROOT)
    data = yaml_dumps(PAGES)
    with open('_quarto.yaml', 'r', encoding='utf-8') as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
    cfg['website']['sidebar']['contents'] = PAGES
    with open('_quarto.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(
            cfg,
            f,
            encoding='utf-8',
            allow_unicode=True,
            Dumper=SafeDumperWithOrder
            )
