# knowledge

本から学んだ内容を本ごとにdumpしていく個人ナレッジベース。

## 設計方針

1. **1冊 = 1ディレクトリ**（`books/<書名>/`）。本の情報・読書メモ・引用がそこに閉じる。
2. **dump先は1ファイルに集約**（`notes.md`）。読みながら追記するだけでよく、書く場所に迷わない。
3. **本を横断する概念は `topics/` に切り出す**。ここが蓄積の本体。読んだ冊数が増えるほど、「本ごとのメモ」より「概念ごとのノート」に価値が集まる。
4. **プレーンなMarkdown + Git**。ツールに依存せず、差分が読め、grepできる。
5. **索引は自動生成**（`scripts/build-index.py`）。手でメンテすると必ず腐る。

## ディレクトリ

```
books/                本ごとのメモ
  README.md           全書籍の索引（自動生成）
  <書名>/             ディレクトリ名は日本語の書名（副題は落とす）
    index.md          メタデータ・全体まとめ・読書ログ
    notes.md          章ごとの読書メモ（dumpのメイン）
    quotes.md         そのまま残したい引用
topics/               本を横断する概念ノート
templates/            新規作成用テンプレート
scripts/              索引生成などの補助スクリプト
```

## 分担

| | 担当 |
| --- | --- |
| 書誌情報の調査（著者・発売日・ISBN・ページ数） | Claude |
| 目次の取得と章立ての作成 | Claude |
| テンプレート配置・索引更新・表記整理 | Claude |
| **各章で何が重要だったか** | 自分 |
| 引用の抜き書き、解釈、疑問 | 自分 |
| `topics/` への切り出し | 提案はClaude、判断と執筆は自分 |

Claudeは**空の器を正確に作るところまで**。章の中身を推測で埋めさせない（`CLAUDE.md` に明記済み）。

## 使い方

### 新しい本を追加する

Claude Codeに本のURL・書名・ISBNのどれかを渡して「追加して」と頼む。ディレクトリ作成・メタデータ調査・目次の検索・全章分の見出し作成・索引更新まで済んだ状態が返ってくる。

手動でやる場合:

```bash
book=書名
mkdir -p "books/$book"
cp templates/book-index.md "books/$book/index.md"
cp templates/book-notes.md "books/$book/notes.md"
cp templates/book-quotes.md "books/$book/quotes.md"
# index.md のfrontmatterを埋める
python3 scripts/build-index.py   # books/README.md を更新
```

### 読みながらdumpする

`books/<書名>/notes.md` に章単位で追記する。記法は最小限:

| 記法 | 意味 |
| --- | --- |
| `p.123` | 該当ページ。あとで原典に戻れるように、できるだけ付ける |
| `> …` | 本文の引用（自分の言葉と混ぜない） |
| `→ …` | 自分の解釈・連想・仕事への当てはめ |
| `? …` | 疑問・未消化・要検証 |
| `[[topics/xxx]]` | 概念ノートへのリンク |

引用と自分の考えを記法で分けておくのが唯一の重要なルール。数年後に読み返したとき、「本が言ったこと」と「自分が考えたこと」を区別できなくなるのが一番もったいない。

### 読み終わったら

1. `index.md` の「全体まとめ」「効いた3点」を書く（ここだけは必ず自分の言葉で）。
2. 繰り返し出てきた概念を `topics/` に切り出し、`notes.md` からリンクする。
3. `status: done` / `finished` / `rating` を埋めて `python3 scripts/build-index.py`。

## 索引

- [書籍一覧](books/README.md)
- [概念ノート一覧](topics/README.md)
