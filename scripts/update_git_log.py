import subprocess as sps
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def get_all_commit_details():
    try:
        # 执行 git log 命令，获取提交哈希、作者、日期和备注信息
        # '--pretty=format:%h %an %ad \n%B\n',
        result = sps.run(
            [
                'git',
                'log',
                '--pretty=format:`%as` `%an` `%ae` `%H` `%B` <br>'
                ],
            capture_output=True,  # text=True,
            )
        if result.returncode == 0:
            lst_commit: list[str] = re.findall(
                r'`(.*?)` `(.*?)` `(.*?)` `(.*?)` `([\s\S]*?)` <br>',
                result.stdout.decode()
                )
            # print(lst_commit)
            return lst_commit
        else:
            print(f"执行 Git 命令时出错: {result.stderr}")
            return []
    except Exception as e:
        print(f"发生未知错误: {e}")
        return []


FrontMatter = '''---
title: 更新日志
lang: zh-CN
---
'''

if __name__ == '__main__':
    print("\n更新日志", sys.argv)
    lst_commit = get_all_commit_details()
    with open('Pages/关于/Log.md', 'w', encoding='utf-8') as f:
        f.write(FrontMatter)
        for commit in lst_commit:
            txt_conmit = f'\n[{commit[0]}] {commit[1]} <{commit[2]}> `{commit[3]}`\n\n'
            txt_conmit += '\n'.join([
                f'> {_line}' for _line in commit[-1].strip().split('\n')
                ])
            f.write(txt_conmit + '\n')
