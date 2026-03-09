# Cosense RAG System

Cosense (Scrapbox) のプロジェクトデータをインデックスし、AI（Ollama / Gemma3）を使用して質問に回答する RAG (Retrieval-Augmented Generation) システムです。

## 特徴

- **スパースベクトル検索**: SPLADE モデルを使用してテキストをベクトル化し、Elasticsearch で高速かつ高精度な検索を行います。
- **自動同期**: Cosense API からページデータを自動的に取得・更新します。
- **AI 回答生成**: オフラインで動作する Ollama (Gemma3) を統合し、プライバシーに配慮した回答生成が可能です。
- **モダンな UI**: React + Vite による、高速でレスポンシブなダークモード UI を提供します。

## アーキテクチャ

システムは以下の 6 つのサービスで構成されています：

- **ui**: React フロントエンド (Port: 3000)
- **search-api**: バックエンド・オーケストレーター (Port: 8000)
- **splade-api**: SPLADE ベクトル化サービス (Port: 8001)
- **llm-api**: Ollama 連携サービス (Port: 8002)
- **batch**: データ取り込み（インジェクション）サービス
- **elasticsearch**: 検索エンジン / ベクトルデータベース (Port: 9200)

## セットアップ

### 1. 前提条件

- Docker & Docker Compose
- [Ollama](https://ollama.ai/) がホストマシンで動作していること
- Ollama で `gemma3:latest` モデルがプルされていること:
  ```bash
  ollama pull gemma3:latest
  ```

### 2. 起動

プロジェクトのルートディレクトリで以下のコマンドを実行します：

```bash
make up
```

### 3. テストデータのインポート (Cosense 同期)

デフォルトでは `help` プロジェクトのデータを同期するように設定されています：

```bash
make sync
```

## 使い方

1. ブラウザで `http://localhost:3000` にアクセスします。
2. 検索バーに Cosense の内容に関する質問を入力します。
3. AI が生成した回答と、その根拠となったソース（Cosense へのリンク）が表示されます。

## 開発用コマンド

`Makefile` に便利なショートカットを用意しています：

- `make up`: 全サービスをバックグラウンドで起動
- `make down`: サービスの停止と削除
- `make build`: コンテナの再ビルド
- `make logs`: ログの表示
- `make health`: 各サービスのヘルスチェック
- `make sync`: Cosense データの同期実行
- `make clean`: データ量（Elasticsearch）を含む完全なクリーンアップ