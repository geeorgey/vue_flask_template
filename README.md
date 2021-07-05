## flask-vue.js テンプレート
フロントエンド vue.js
バックエンド Flask
Heroku上でインストールするためのテンプレートです

## Macローカル環境で立ち上げるには
git clone 

//仮想環境を作る
python3 -m venv .venv
source .venv/bin/activate
//コマンドライン上に(.venv)が表示されれば成功

### pipenv のインストール
https://qiita.com/MasanoriIwakura/items/e9011e49bd225553ff47
brew install pipenv

## postgreSQLをインストール
MacにpostgreSQLをインストールするには
https://qiita.com/yorokobi_kannsya/items/f77d074e382a88dae971
結構時間かかります。

アプリからインストールする場合
https://postgresapp.com/downloads.html
ダウンロードしたらdmgファイルを展開し、アプリケーションフォルダに入れてから立ち上げる。
アプリの右側にあるイニシャライズボタンを押す。
Runningとなれば起動中。
起動状態と、存在するDB名がわかるだけなのでそれ以外の作業についてはコマンドラインから実行すること。

### postgreSQLにDBを作る
ターミナルから
psql

postgreSQL環境にログインしたらDBを作成する

username=#
となっている状態で
CREATE DATABASE yourDatabaseName;
これで作成されました。アプリを見ると、yourDatabaseName(任意の名前に変更してください。例：qa4u) というDBが追加されていると思います。
ユーザーを作る
CREATE ROLE role_sample WITH LOGIN PASSWORD 'password';
こんな感じでユーザーを作ります。
例：CREATE ROLE qa4u_user WITH LOGIN PASSWORD 'qa4upass';
ここまででDBとユーザーを作ったのでログアウトしましょう。
\q
でpostgreSQL環境からログアウトする。
\ は optionボタンと右上の¥マークを同時押し。


## pythonにパッケージをインストールする
cd backend
//Macにpsycopg2をインストールするために必要なおまじない
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
//必要なパッケージをインストールする
pipenv install -r requirements.txt

## DatabaseにUserテーブルを作る
ルートディレクトリに移動して実行してください
flask db init
flask db migrate
flask db upgrade

### Databaseの設定を更新する場合は
backend
 /flask-migrateDB.py
 /models.py
の２つのファイルを更新してください。
その後
flask db migrate
flask db upgrade
とすることで、postgreSQLのDatabaseのスキーマがupgradeされます。 

## フロントエンドについて
テンプレートはこちらから拝借
https://github.com/tookit/vue-material-admin
デモはここ
http://vma.isocked.com/#/dashboard

### ローカル環境(Mac)にnpmをインストールする
参考：https://qiita.com/non0311/items/664cf74d9ff4bad9cf46
brew install nodebrew
mkdir -p ~/.nodebrew/src
nodebrew install-binary latest
nodebrew list
nodebrew use v16.4.1

### yarnのインストール
npm install -g yarn

### frontendで使うモジュールのインストール
cd frontend
yarn install

### frontendのビルド
yarn build
こうすることでルートディレクトリに dist というディレクトリが作成されます。
フロントエンドを更新する場合は
/frontend/src
以下のファイルを更新してから yarn build をしてビルドすることで更新が反映されます。
注意：ビルド後にWebブラウザでアクセスしたときは、スーパーリロードしてブラウザキャッシュを消してください。
そうしないとおそらくビルドしても更新が反映されません。

## Herokuにデプロイする
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Heroku上にデプロイする場合はこちらのボタンからデプロイしてください。

## Herokuに環境変数を設定する

### Heroku postgresをインストールする
Heroku管理画面のResourcesタブを開き、Add-ons部分からHeroku Postgresを選択。
FreeプランでOKです。

### 環境変数を設定する
Settingsタブを開き、Reveal Config Varsボタンをクリック。
環境変数欄にすでにDATABASE_URL が入っているのがわかると思います。
その下に４つ追加します。
Key　｜　Value
ENV　｜　development
FLASK_APP　｜　backend
FLASK_DEBUG　｜　1
VUE_APP_BASE_API　｜　ここには、右上にあるOpen App ボタンを押して開いたURLを入れてください。

## 現時点で実装してある機能
ログイン画面でメールアドレスとパスワードを入力してログインすることが可能です。
ログイン画面でメールアドレスとパスワードを入力してRegisterボタンを押すとユーザー登録できます。
DBに登録されるパスワードはハッシュ化されておらず平文で保存されます。

## 今後の予定
開発しやすいようにマニュアルを整備する予定。
