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
デプロイ前に、必ずForkしてください。
mainブランチから直接デプロイしても動きません。

### やるべきこと
Herokuにログインしたらアプリを作成してURLを取得しましょう。
アプリ作成後に右上あたりに現れるOpen Appボタンを押すとURLがわかります。

frontend/.env.development
にかかれているVUE_APP_BASE_APIを先程取得したURLに変えます。

次はターミナルで
yarn install
をしてパッケージのインストールを行ったあとに
yarn build
をして、distディレクトリの中身を更新して下さい。

これが終わったら、ファイルを先程Forkしたリポジトリにアップします。
git add frontend/.env.development
git add dist
git commit -m'Heroku用の調整'
git push -u origin main
(ブランチ名によりmainかどうかは分かりませんので適宜変更して下さい)

これをやったら、Herokuの管理ページにあるDeployタブを開きます。
自分のGithubアカウントとアプリ名で検索して設定しましょう。
Deploy a GitHub branchのChoose a branch to deployからブランチを選択して
Deploy Branchボタンを押すことで、変更が反映されます。

## Herokuに環境変数を設定する

### Heroku postgresをインストールする
Heroku管理画面のResourcesタブを開き、Add-ons部分からHeroku Postgresを選択。
FreeプランでOKです。

### 環境変数を設定する
Settingsタブを開き、Reveal Config Varsボタンをクリック。
環境変数欄にすでにDATABASE_URL が入っているのがわかると思います。
その下に5つ追加します。
Key　｜　Value
ENV　｜　development
FLASK_APP　｜　backend
FLASK_DEBUG　｜　1
VUE_APP_BASE_API　｜　ここには、右上にあるOpen App ボタンを押して開いたURLを入れてください。
SQLALCHEMY_DATABASE_URI　｜　ここには、DATABASE_URLの中身を若干加工して入れます。
postgres://ユーザー名:パスワード@Host名:5432/DB名
となっていると思うのですが、冒頭にあるpostgresをpostgresqlに変更して
postgresql://ユーザー名:パスワード@Host名:5432/DB名
という形式にして入れて下さい。


### DBをセットアップする
右上にあるMoreボタンを押すと、Run consoleというメニューがあるのでそれを開きます。
heroku runの横に bash と書かれた入力欄があるので、そこに
flask db upgrade
と入れて下さい。
これでDBの初期設定は完了です。
Open Appボタンからサイトを開けば、こちらと同様に見えるはずです。
https://vueflasktestgeeorgey.herokuapp.com/#/

## 現時点で実装してある機能
ログイン画面でメールアドレスとパスワードを入力してログインすることが可能です。
ログイン画面でメールアドレスとパスワードを入力してRegisterボタンを押すとユーザー登録できます。
DBに登録されるパスワードはハッシュ化されておらず平文で保存されます。

## 今後の予定
開発しやすいようにマニュアルを整備する予定。
