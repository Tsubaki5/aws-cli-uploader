# AWS S3ストレージ用 ファイルアップローダー  
S3ストレージにファイルをフォルダごとアップロードする子です。  
## 使用方法  
config.txtをpythonファイルと同じ場所に作成し、以下のテンプレートで作成してください。
```
access_key=YOUR_ACCESS_KEY
secret_key=YOUR_SECRET_KEY
endpoint=YOUR_ENDPOINT_URL
bucket_name=YOUR_BUCKET_NAME
processes=5
```
## 注意点  
フォルダーを選択する際は最下層のディレクトリを選択してください。エラーが出ます。(修正予定)
