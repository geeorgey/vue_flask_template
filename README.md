## flask-vue.js テンプレート
フロントエンド vue.js  
バックエンド Flask  
Heroku上にデプロイして稼働させるWebアプリのテンプレートです。

## 関連リンク
- [pythonを使ってリアクティブなWebアプリをお手軽に1分で作りたい](https://qiita.com/geeorgey/items/ace37bd92841c9d1a378)
- [pythonを使ってリアクティブなWebアプリを作りたい【基礎編】](https://qiita.com/geeorgey/items/3f86b207cd412680b835)
- [pythonを使ってリアクティブなWebアプリを作りたい【開発編】](https://qiita.com/geeorgey/items/ea60afe0c44a5f9db483)
- [pythonを使ってリアクティブなWebアプリを作りたい【開発編2】](https://qiita.com/geeorgey/items/961c1d1092ec60bb06bd)
- [pythonを使ってリアクティブなWebアプリを作りたい【開発編3】](https://qiita.com/geeorgey/items/1f5544b12e7d26a1216c)
- [pythonを使ってリアクティブなWebアプリを作りたい【開発編3-2】](https://qiita.com/geeorgey/items/54b4fb22351a3e941cf6)
- [pythonを使ってリアクティブなWebアプリを作りたい【開発編4】パスワードの暗号化](https://qiita.com/geeorgey/items/85905a4772903b180fad)
- [pythonを使ってリアクティブなWebアプリを作りたい【開発編5】Herokuの開発環境と本番環境](https://qiita.com/geeorgey/items/b080617f5332ab7255c4)

## 開発環境
Macでローカル開発することを前提に以下の文章は書かれています。Windowsの場合は多少やり方が変わると思いますが、調べてみてください。

## はじめに
READMEを上から実行していく事で、Herokuへのデプロイと、ローカルの開発環境が構築できるように書いてあります。  
開発初心者向けに書いてありますので、分かっている部分については読み飛ばしてください。

## MacにHome brewをインストールする
https://brew.sh/index_ja  
書いてあるコマンドをターミナルにコピペしてインストールしてください。

## Macにgitをインストールする
Home brewを使ってインストールします。  
ターミナルで以下のコマンドを実行してインストールしてください。  
brew install git

## GithubでリポジトリをForkしましょう。
やり方はこちらを参照：https://docs.github.com/ja/github/getting-started-with-github/quickstart/fork-a-repo  
このプロジェクトを自分のGithubレポジトリにForkしてください。  
注意：geeorgey/vue_flask_template のmainブランチから直接デプロイしても動きません。

###　そのままデプロイしても動かない理由
Vue.jsからビルドする事でdistディレクトリが作られるのですが、ビルドの際にVUE_APP_BASE_APIという環境変数が読み込まれています。  
これをこれから作るHerokuアプリのURLに変えないとうまく動きません。

### ローカル環境(Mac)にリポジトリをcloneしてください
Forkしたリポジトリをローカル環境にcloneしましょう。  
ターミナルで、作業フォルダに移動しましょう。  
cd ~/  
mkdir QA  
cd QA  
git clone git@github.com:geeorgey/vue_flask_template.git ←ここはForkしたリポジトリのものを入れてください  
cd vue_flask_template  
ここが作業ディレクトリになります。  
こちらの例で言うと   
~/QA/vue_flask_template/  
以下にファイルがすべてDLされます。

## Herokuでアプリを作る
https://heroku.com/  
アカウントを作って、ログインしてください。  
Herokuにログインしたらアプリを作成してURLを取得しましょう。  
https://dashboard.heroku.com/apps  
こちらのURLから、右上にあるNew>Create New Appを選択して、適当な名前でアプリを作ってください。  
アプリ作成後に右上あたりに現れるOpen Appボタンを押すとURLがわかります。  

### Herokuとは？(気になる人向け)
PaaSと言われるサービスの一つです。
自分でWebサーバを立ち上げずとも、必要なサービスを組み合わせる事で各種アプリを動かすことができます。
無料枠があるので、その範囲でやれることをやってみてください。
Herokuの特徴として、Github からソースコードをデプロイすることができます。
逆に、普通のWebサーバと違い、Heroku上のファイルを直接編集するということができません。
必ずローカル環境もしくはGithub上に静的ファイルを生成し、それをデプロイする形で使います。
プログラムでファイルを生成してHeroku上に保存するという使い方はできないので注意してください。
動的に生成されるデータは必ずデータベースに格納する必要があります。

以下について詳細はこちらをご覧ください  
https://qiita.com/geeorgey/items/b080617f5332ab7255c4  

## ローカル環境(Mac)で、frontendのビルドの準備をする
frontend/.env.development  
にかかれているVUE_APP_BASE_APIがビルドに使われます。  
VUE_APP_BASE_API="http://localhost:5000"

次はターミナルから、frontendディレクトリに移りましょう。  
cd frontend  
この時点での場所は  
~/QA/vue_flask_template/frontend/  
です。  

## 同様にローカル環境でHeroku用のfrontendのビルドの準備をする
frontend/.env.production  
にかかれているVUE_APP_BASE_APIを先程取得したURLに変えます。  

以下でフロントエンド側パッケージ管理システムであるyarnのインストールを行います

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
yarn install  
インストールは先ほどと同じ  
~/QA/vue_flask_template/frontend/  
で行います。

### frontendのビルド
yarn build  
こうすることでルートディレクトリに dist_dev というディレクトリが作成されます。  
VUE_APP_BASE_APIが組み込まれた状態でビルドされます。

### Heroku用のfrontendのビルド
yarn build:prod  
こうすることでルートディレクトリに dist というディレクトリが作成されます。  
VUE_APP_BASE_APIが組み込まれた状態でビルドされます。

## 更新したファイルをGithubのリポジトリにpushする
これが終わったら、ファイルを先程Forkしたリポジトリにアップします。  
作業ディレクトリはルートディレクトリの ~/QA です。  
cd ~/QA  
git add frontend/.env.production  
git add dist  
git commit -m'Heroku用の調整'  
git push -u origin main  
(ブランチ名によりmain かどうかは分かりませんので適宜変更して下さい)  
これでForkしたリポジトリが更新されたと思います。

## Herokuにデプロイする
これをやったら、Herokuの管理ページを開き、Deployタブを開きます。  
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
その下に7つ追加します。  
Key　｜　Value  
ENV　｜　development  
FLASK_APP　｜　backend  
FLASK_DEBUG　｜　1  
STATIC_FOLDER_PATH　｜ ../dist/static
TEMPLATE_FOLDER_PATH　｜　../dist
VUE_APP_BASE_API　｜　ここには、右上にあるOpen App ボタンを押して開いたURLを入れてください。  
SQLALCHEMY_DATABASE_URI　｜　ここには、DATABASE_URLの中身を若干加工して入れます。  
postgres://ユーザー名:パスワード@Host名:5432/DB名  
となっていると思うのですが、冒頭にあるpostgresをpostgresqlに変更して  
postgresql://ユーザー名:パスワード@Host名:5432/DB名  
という形式にして入れて下さい。

### DBをセットアップする
Heroku管理画面の右上にあるMoreボタンを押すと、Run consoleというメニューがあるのでそれを開きます。  
heroku runの横に bash と書かれた入力欄があるので、そこに  
flask db upgrade  
と入れて下さい。  
これでDBの初期設定は完了です。  
Open Appボタンからサイトを開けば、こちらと同様に見えるはずです。  
https://vueflasktestgeeorgey.herokuapp.com/#/

## Macローカル環境を整備する
作業フォルダで以下の設定をしましょう

### backend(python)用の設定をする
仮想環境を作る  
ルートディレクトリでpythonの仮想環境を作っておきます。  
cd ~/QA  
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

## ローカル環境でアプリを立ち上げる
作業ディレクトリのルートから実行してください。  

cd ~/QA  
flask run  

これでアプリが立ち上がります。  
http://localhost:5000/  
でブラウザからアクセスできるようになっているはずです。


## フロントエンドについて
テンプレートはこちらから拝借  
https://github.com/tookit/vue-material-admin  
デモはここ  
http://vma.isocked.com/#/dashboard

## 現時点で実装してある機能
ログイン画面でメールアドレスとパスワードを入力してログインすることが可能です。  
ログイン画面でメールアドレスとパスワードを入力してRegisterボタンを押すとユーザー登録できます。  
DBに登録されるパスワードはハッシュ化されておらず平文で保存されます。

## どのように動いているか Vue.js→Flask→Vue.js
vue.jsで構築したフロントエンドを使ったユーザーが入力したデータをbackendのFlaskで構築したAPIを叩くことでデータを受け渡して処理をしています。  
例えば、トップページのログイン画面ですが、画面自体は  
frontend/src/views/auth/Login.vue  
https://github.com/geeorgey/vue_flask_template/blob/main/frontend/src/views/auth/Login.vue  
で構築されています。  
ログインボタンには　handleLogin　という関数が割り当てられており、同ファイルにある関数を呼び出しています。  
https://github.com/geeorgey/vue_flask_template/blob/cc05a7b367638c8aef55964620ed15ab6e4083f2/frontend/src/views/auth/Login.vue#L96  
dispatch('login', this.formModel)  
の部分でloginというメソッドを呼び出しています。loginがどこにあるかというとこちらです。  
https://github.com/geeorgey/vue_flask_template/blob/cc05a7b367638c8aef55964620ed15ab6e4083f2/frontend/src/store/modules/auth.js#L30  
    return request({    
      url: '/auth/login',    
      method: 'post'  
という部分がありますが、ここでFlaskを呼び出しています。  
該当するコードはこちらです。  
https://github.com/geeorgey/vue_flask_template/blob/cc05a7b367638c8aef55964620ed15ab6e4083f2/backend/auth.py#L15  
受け取ったusernameとpasswordをもとにユーザーテーブルを検索してマッチすれば200を返してログイン完了にするという形です。  
return jsonify 部分でfrontendにデータを返しています。  
Login.vueに戻りましょう。データを受け取るのはこの部分です。  
https://github.com/geeorgey/vue_flask_template/blob/cc05a7b367638c8aef55964620ed15ab6e4083f2/frontend/src/views/auth/Login.vue#L101  
200が返ってきた場合は、dashboardに移動します。  
400が返ってきた場合はログインに失敗した旨を返しています。  

フロントエンドからバックエンドにデータを投げて、処理したものを受け取る流れについて  
こちらに詳細を記していますので、興味がある場合は参照してみて下さい。  
https://qiita.com/geeorgey/items/ea60afe0c44a5f9db483

### 開発に必要な知識
Vue.jsについての知識が必要です。UI開発チームがこちらを担当します。  
pythonを書く人はbackend側を作ってデータの処理を担当してください。  
https://github.com/geeorgey/vue_flask_template/blob/cc05a7b367638c8aef55964620ed15ab6e4083f2/backend/auth.py#L15  
こちらに書いてあるようにrouteの設定をしてデータを受け取るためのエンドポイントを設定します。  
フロントエンドチームは、エンドポイントにデータを投げます。  
バックエンドチームは、受け取ったデータを使ってデータの処理をして、レスポンスを返します。  
フロントエンドチームは、返ってきたレスポンスを使って、UIに変化をもたらしましょう。

### frontendを開発するには
フロントエンドを更新する場合は  
/frontend/src  
以下のファイルを更新してから yarn build をしてビルドすることで更新が反映されます。  
注意：ビルド後にWebブラウザでアクセスしたときは、スーパーリロードしてブラウザキャッシュを消してください。  
そうしないとおそらくビルドしても更新が反映されません。


## 今後の予定
開発しやすいようにマニュアルを整備する予定。
