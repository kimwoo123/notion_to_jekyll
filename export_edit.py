from urllib import parse
import shutil
import zipfile
import os
import re

path_dir = './export'
file_list = os.listdir(path_dir)

# Notion에서 export한 zip파일들을 압축 해제
for file in file_list:
    zipfile.ZipFile(f'./export/{file}').extractall('./unzip')

# 압축 해제한 파일들
unzip_list = os.listdir('./unzip')
for unzip_file in unzip_list:
    regex = re.compile('.md$')
    # MD 파일의 경우
    if regex.search(unzip_file):
        try:
            with open(f'./unzip/{unzip_file}', 'r', encoding='utf-8') as before_file:
                # 파일을 읽어서 첫번째 줄을 제목 및 파일이름으로 설정
                lines = before_file.readlines()
                title = lines[0]
                file_name = title[2:].rstrip()
                # 이미 작업이 완료된 파일
                if unzip_file[:-3] == file_name:
                    continue
                # 이미지 경로 퍼센트 인코딩
                percent_encoding_file = parse.quote(unzip_file)[:-3]
                title_encoding = parse.quote(file_name)

                # 수정이 필요한 이미지 경로 수정
                for i in range(len(lines)):
                    if percent_encoding_file in lines[i]:
                        lines[i] = lines[i].replace(percent_encoding_file, title_encoding)

                # 새로운 MD 파일
                with open(f'./unzip/{file_name}.md', 'w', encoding='utf-8') as new_file:
                    new_file.writelines(lines)
                # 이미지 폴더명 변경
                os.rename(f'./unzip/{unzip_file[:-3]}', f'./unzip/{file_name}')
            # 수정전 MD 파일 삭제
            os.remove(f'./unzip/{unzip_file}')

        except:
            with open(f'./unzip/{unzip_file}', 'r', encoding='utf-8') as file:
                file_title = file.readline()[2:]
            # 이미 작업이 완료된 파일 및 폴더
            if unzip_file[:-3] != file_title:
                os.remove(f'./unzip/{unzip_file}')
                shutil.rmtree(f'./unzip/{unzip_file[:-3]}')






