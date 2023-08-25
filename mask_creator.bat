@echo off

rem カレントディレクトリをこの .bat ファイルの場所にする
cd /d %~dp0

rem 初回起動時に venv 環境を作成
if not exist venv (
  python -m venv venv
)

rem venv を有効化
call .\venv\Scripts\activate.bat

rem 依存パッケージがインストール済みかチェック
python -m pip list | findstr -i numpy > nul

rem 依存パッケージがインストール済みじゃなかったら入れる
if "%ERRORLEVEL%" neq "0" (
  python -m pip install -r requirements.txt
)

rem スクリプトを起動
python mask_creator.py %*
