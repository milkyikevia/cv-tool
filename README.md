# 📸 CV-Tool（画像・動画前処理CLIツール）

## 📝 概要

画像・動画の前処理を **YAMLで一括管理して自動実行できるCLIツール**です。    
データセット作成やCV学習用の前処理を効率化します。  

### ✨ 主な機能

* ✂️ Crop（切り抜き）
* 📐 Resize（解像度変更）
* 💡 Brightness（明るさ調整）
* 🎨 Saturation（彩度調整）
* 🔄 Rotate 90°（回転）
* ↔️ Flip（水平・垂直反転）

👉 すべての処理は `config.yaml` でON/OFF管理可能    

---

## 💻 動作環境

* Python 3.11.x
* Python 3.12.x
* Python 3.13.x
* Python 3.14.x

---

## 🚀 インストール

### 1. 📦 リポジトリ取得

```bash
git clone https://github.com/milkyikevia/cv-tool.git
cd cv-tool
git checkout 1.x
```

### 2. 🧪 仮想環境作成（Conda）

```bash
conda create -n cv-tool python=3.14
conda activate cv-tool
```

### 3. 📚 依存関係インストール

```bash
pip install -r requirements.txt
```

---

## 🛠️ 使用方法

本ツールは以下2つのモードをサポートしています：    

* CLIモード（コマンド実行）
* インタラクティブモード（対話式）

---

# 💻 CLIモード

```bash
python main.py [-t {image,i,video,v}] [-p PATH] [-c CONFIG] [-o OUTPUT]
```

### ⚙️ オプション

| オプション | 内容            | デフォルト         |
| ----- | ------------- | ------------- |
| `-t`  | image / video | image         |
| `-p`  | 入力パス          | ./assets      |
| `-c`  | configファイル    | ./config.yaml |
| `-o`  | 出力先           | ./result      |

---

### ▶️ 実行例

#### 画像（単体）

```bash
python main.py -t image -p ./assets/teddybear.jpeg -c config.yaml -o ./result
```

#### 画像（ディレクトリ）

```bash
python main.py -t image -p ./assets/ -c config.yaml -o ./result
```

#### 動画

```bash
python main.py -t video -p ./assets/asakusa.mp4 -c config.yaml -o ./result
```

---

# 🖥️ インタラクティブモード

```bash
python main.py --interactive
```

### ⚙️ コマンド一覧

| コマンド                | 説明       |          |
| ------------------- | -------- | -------- |
| `set type <image    | video>`  | データタイプ指定 |
| `set path <path>`   | 入力パス指定   |          |
| `set config <path>` | config指定 |          |
| `set output <path>` | 出力先指定    |          |
| `run`               | 前処理実行    |          |
| `show`              | 設定表示     |          |
| `help`              | ヘルプ      |          |
| `exit`              | 終了       |          |

---

### ▶️ 使用例

```bash
> set type image
> set path ./assets/teddybear.jpeg
> run
> exit
```

---

## ⚙️ config.yaml（設定例）

各処理は `enabled` でON/OFF制御できます。    

```yaml
resize:
  enabled: true
  width: 640
  height: 640

brightness:
  enabled: false
  value: 1.2

crop:
  enabled: true
  x: 0
  y: 0
  width: 512
  height: 512
```

👉 有効な処理のみ順番に実行されます    

---

## 🔁 処理フロー

基本の実行順：    

```
Crop → Resize → Brightness → Saturation → Rotate → Flip
```

---

## 📂 出力仕様

### 🖼️ 画像

```
photo.jpg → photo_processed.jpg
重複時 → photo_processed_001.jpg
```

### 🎞️ 動画

```
video.mp4 →
video_processed/
├── video_processed.mp4
└── frames/
```

---

## 🧪 テスト

```bash
PYTHONPATH=. python -m pytest test/ -v
```

---

## 🔍 品質チェック

```bash
make all
make security
```

（例：lint / format / security check）

---

## 📏 開発ルール

### 🌱 ブランチ命名

```
種別/Issue番号-内容
```

* feature/ : 機能追加
* fix/ : バグ修正
* hotfix/ : 緊急対応

---

## 🚀 まとめ

* YAMLで前処理を一括管理
* 画像・動画どちらも対応
* CLI / インタラクティブ両対応
* CVデータセット作成を効率化