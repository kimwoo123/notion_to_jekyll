from datetime import date, datetime
from urllib import parse
import shutil
import zipfile
import os
import re

class NotiontoJekyll:
    def __init__(self):
        self.path_dir = './export'
        self.file_list = os.listdir(self.path_dir)
        self.unzipFile()
        self.modifyMD()


    def unzipFile(self):
        # Notion에서 export한 zip파일들을 압축 해제
        for file in self.file_list:
            regex = re.compile('.zip$')
            if regex.search(file):
                zipfile.ZipFile(f'./export/{file}').extractall('./unzip')


    def modifyMD(self):
        # 압축 해제한 파일들
        self.unzip_list = os.listdir('./unzip')
        for unzip_file in self.unzip_list:
            regex = re.compile('.md$')
            # MD 파일의 경우
            if regex.search(unzip_file):
                with open(f'./unzip/{unzip_file}', 'r', encoding='utf-8') as before_file:
                    # 파일을 읽어서 첫번째 줄을 제목 및 파일이름으로 설정
                    lines = before_file.readlines()
                    
                    # 작업이 완료된 파일
                    if lines[0].strip() == '---':
                        continue

                    print(lines[0])
                    file_title = input('파일 제목을 입력해주세요: ')
                    today = date.today()
                    file_name = f'{today}-{file_title}'

                    # 이미지 경로 퍼센트 인코딩
                    percent_encoding_file = parse.quote(unzip_file).split('.')[0]
                    image_path = f'../../../../../public/assets/{file_name}'

                    # 수정이 필요한 이미지 경로 수정
                    for i in range(len(lines)):
                        if percent_encoding_file in lines[i]:
                            lines[i] = lines[i].replace(percent_encoding_file, image_path)
                self.modifyDir(unzip_file, file_name, lines)


    def modifyDir(self, before_file, modify_name, lines):
        # 이미지 폴더명 변경
        if os.path.exists(f'./unzip/{before_file[:-3]}'):
            if os.path.exists(f'./unzip/{modify_name}'):
                shutil.rmtree(f'./unzip/{modify_name}')
            os.rename(f'./unzip/{before_file[:-3]}', f'./unzip/{modify_name}')

        # 수정전 MD 파일 삭제
        if os.path.exists(f'./unzip/{before_file}'):
            os.remove(f'./unzip/{before_file}')
    
        if os.path.exists(f'./unzip/{modify_name}.md'):
            os.remove(f'./unzip/{modify_name}.md')

        # 새로운 MD 파일
        with open(f'./unzip/{modify_name}.md', 'w', encoding='utf-8') as new_file:
            new_file.writelines(l + '\n' for l in self.addBookTag())
            new_file.writelines(lines)


    def addBookTag(self):
        t = input('게시글의 제목을 입력해주세요:')
        d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c = input('게시글의 카테고리를 입력해주세요:')
        o = input('게시글의 개요를 입력해주세요:')

        layout = 'layout: post'
        title = f'title: {t}'
        date = f'date: {d}'
        categories = f'categories: {c}'
        overview = f'overview: {o}'

        return ['---', layout, title, date, categories, overview, '---']



NotiontoJekyll()