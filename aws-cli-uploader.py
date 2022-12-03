import os
from tkinter import filedialog
from tkinter import *
import boto3
import subprocess
import multiprocessing

# アクセスキーとシークレットキーとエンドポイントを読み取る
with open('config.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
      line = line.strip()
      if line.startswith('access_key='):
        access_key = line.split('=')[1]
      if line.startswith('secret_key='):
        secret_key = line.split('=')[1]
      if line.startswith('endpoint='):
        endpoint = line.split('=')[1]
      if line.startswith('bucket_name='):
        bucket_name = line.split('=')[1]
      if line.startswith('processes='):
        processes = int(line.split('=')[1])

# ファイルを1つずつ取り出し、コマンドを実行
def file_upload(file_path, local_final_folder):
    # コマンドを実行する
    subprocess.run(["aws","s3","cp",file_path,"s3://"+bucket_name+"/"+local_final_folder,"--endpoint-url",endpoint])

if __name__ == '__main__':
          
  # S3クライアントを作成する
  s3 = boto3.client('s3',
                    endpoint_url=endpoint,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key)
    
  # フォルダのパスを指定
  iDir = os.path.abspath(os.path.dirname(__file__))
  folder = filedialog.askdirectory(initialdir = iDir)
  folder_path = folder

  # フォルダ内のファイルをすべて取得
  files = os.listdir(folder_path)
  # フルパス名に変換
  files = [os.path.join(folder_path, file) for file in files]

  # バケットのフォルダーを取得する
  response = s3.list_objects(Bucket=bucket_name)

  # 取得したフォルダーを表示する
  folders = []
  if 'Contents' in response:
      for obj in response['Contents']:
          key = obj['Key']
          if key.endswith('/'):
              folders.append(key)
  else:
      print('Bucket is empty')

  #ローカルのフォルダーとバケット内のフォルダを比較
  local_final_folder = folder_path.split('/')[-1] + "/"
  if not local_final_folder in folders:
      s3.put_object(Bucket=bucket_name, Key=local_final_folder)

  #マルチスレッドリングで任意の処理を実行する
  pool = multiprocessing.Pool(processes=processes)
  for file in files:
      pool.apply_async(file_upload, (file, local_final_folder))
  pool.close()
  pool.join()
