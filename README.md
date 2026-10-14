# 動物のつながり — 公開研究デモ

チンパンジー・アザラシ・鯉・ハト・豚を同じ入口の「動物種」で切り替える非商用研究デモです。AIライブ推論ではありません。ユーザー指定により展示用のつながりは架空設定とし、アザラシ・鯉・ハト・豚にはID固定の「友達・ライバル・遊び仲間」を表示します。実際の社会関係ではありません。全種でBBox枠を非表示にし、位置データは名前と矢印の追従にだけ利用します。下記の過去milestoneは実装経緯であり、現在の表示仕様はこの段落を優先します。

公開入口: https://takuto-ando.github.io/chimp-no-tsunagari/ 。`?species=seal` などで選択動物を指定できます。`seal.html` / `animals.html` は互換入口です。
アザラシ3・鯉9・ハト17・豚26の全55件の追跡／注釈IDに展示用の仮名を付けています（例: しお・なぎ・みなと）。一覧は `data/displayNames.json`。各種の配列はID番号の1始まり順です。実在の名前、性別、性格、社会関係を示しません。動画間の同一性を意味せず、元のID・BBox・共起計算は変更していません。チンパンジーの既存名は保持しています。
相関図のカードは動画のBBox中心の変化に追従し、画面内の2個体を結ぶ辺をアニメーション表示します。図の配置は読みやすさを保つ模式配置で、物理座標・社会関係の推定ではありません。シークに追従し、画面外のカードは最後の位置を保持します。動きを減らす端末設定ではtransitionと辺アニメーションを抑えます。

## Attribution / Media license

Xiaoxuan Ma, Stephan P. Kaufhold, Jiajun Su, Wentao Zhu, Jack Terwilliger, Andres Meza, Yixin Zhu, Federico Rossano, Yizhou Wang. ChimpACT: A Longitudinal Dataset for Understanding Chimpanzee Behaviors. NeurIPS 2023, vol.36, pp.27501–27531.

Source: https://shirleymaxx.github.io/ChimpACT/

ChimpACT videos, cropped reference images, derived annotation/prediction data and data modifications: CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/ . Noncommercial use and attribution required. Changes: videos recompressed/no audio; reference images cropped; prediction boxes and fictional relationship overlays added. No endorsement by dataset authors or Leipzig Zoo is implied. This is a research demonstration of chimpanzee co-occurrence visualization, not a commercial exhibit or a verified account of their social relationships. Full dataset/request-form files are not included.

Model weights, private research repository, backend, databases, credentials, and original dataset ZIP are not published.

## Downloadable mapped videos

downloads/ contains three silent 16:9 MP4 demo videos. Original images are letterboxed without stretching or cropping. AI-estimated names and fictional sex/character/social overlays are burned in. These are not live inference or verified social relationships. Redistribute only for noncommercial use with downloads/LICENSE.txt.

## アザラシ版

`seal.html` は同じUI・プレイヤー・BBox・個体カード・観測関係図を再利用します。
`python3 seal/serve.py` をこのディレクトリで実行し、http://127.0.0.1:5189/seal.html を開きます（動画シーク用のRange対応、Python標準ライブラリのみ）。
実映像5本（19秒・4秒・4秒・6秒・2秒）に手動BBoxを付けています。追加動画は目視keyframe間を線形補間しています。Seal 01/02/03は各短区間だけの一時追跡IDで、実在個体名ではありません。別動画の同じラベル同士が同一個体かは未確認です。
既存JSONの `individual_id=seal_track_01/02/03` はUI互換用の一時キーで、確認済み個体識別を意味しません。
初期表示は19秒版です。観測した3本の追跡区間を注釈し、画面外・不確かな区間は補間しません。網羅的な全個体注釈ではなく、未注釈の個体が映る場合があります。
単頭の3本と2頭の短区間も保持しています。既存 `pipeline.pair_history` から共起・画像上の近接の辺を生成しています。社会関係ではありません。画面奥の岩などの形は個体として登録していません。
SealIDとの照合・画像使用・再配布・学習、新規モデル、LLM APIはありません。

動画01–03の出典: Ian Durbach, *Video classification using deep learning* (2020), https://zenodo.org/records/3842040 （DOI: 10.5281/zenodo.3842040）。
レコードのライセンスはCC BY 4.0: https://creativecommons.org/licenses/by/4.0/ 。転載・改変時は出典、ライセンス、変更を明記してください。
変更: `030615ch3_210225.avi` と `260515ch1_083456.avi` の短区間を無音H.264 MP4に変換、手動BBoxと追跡ラベルを重ねています。著者の推奨を意味しません。
画面内時計は順に2015-06-03 21:05:39–21:05:43、21:05:44–21:05:48、2015-05-26 08:34:59–08:35:05です。
コンテナ時刻と画面内時計に差があるため、画面内時計と抽出フレームの目視で区間を選択しました。
再抽出は元AVIをデコードし、`select=between(n\,2145\,2188),setpts=N/(11*TB)`、`select=between(n\,2200\,2243),setpts=N/(11*TB)`、別日AVIで `select=between(n\,40\,111),setpts=N/(12*TB)` を使用します（`-an -fps_mode passthrough -c:v libx264 -crf 23 -pix_fmt yuv420p -movflags +faststart`）。
元AVIはローカルの部分取得のみでGit登録していません。

動画04: The Lamb Family, *Harbor seals (Phoca vitulina)*, Point Defiance Zoo & Aquarium, Tacoma, Washington, USA (2016-01-04)。
出典: https://commons.wikimedia.org/wiki/File:Harbor_seals_(Phoca_vitulina).webm 。CC BY-SA 2.0: https://creativecommons.org/licenses/by-sa/2.0/ 。著者表示とShareAlike条件を維持してください。
既存の `seal_reid/data/public_detection_video/harbor_seals_6s.mp4` から3–5秒（10 fpsでフレーム30–49）を抽出し、960×540へ縮小・無音H.264に再圧縮、手動BBox・一時追跡ラベルを追加しました。作者の推奨・監修を意味しません。
動画04の派生MP4、手動BBox・追跡・共起JSONをCC BY-SA 2.0で提供します。SealID素材は含みません。カメラは動いており、定点撮影・物理距離の計測ではありません。
元動画のSHA256: `15e3ea8dd0543a95155de6cb247f3ad84b123052c91352c2f372338ccdf814ac`。既存6秒clipのSHA256: `ec5ae97bafc641ee78bc5f5fbdcb11897faf71ab60f5852b6f410a0d634f50a0`。
2秒版のMP4は約141 KiBです。動画ごとに追跡カード・出典・ライセンスを切り替えます。

19秒版も同じCommons出典・CC BY-SA 2.0です。元WebMの先頭19秒を960×540・10 fps・無音H.264へ変換し、190フレームの部分的手動追跡注釈を追加しています。派生MP4と対応JSONもCC BY-SA 2.0です。
生成: `ffmpeg -i harbor_seals.webm -t 19 -an -vf 'fps=10,scale=960:540' -c:v libx264 -crf 23 -pix_fmt yuv420p -movflags +faststart seal_harbor_19s.mp4` 。約1.2 MiB。再識別モデルの学習はありません。

既存の研究ソース `animal_video_reid/web` は公開repoに含まれないため、全面コピーを避け、変更したソースの差分を `seal/ui.patch` に保存しています。ほかの動物には既存 `DatasetViewer.tsx` を再利用しています。
`patch -d /path/to/web-copy -p1 < seal/ui.patch` を同ソースのコピーへ適用して `npm run build:pages` を実行し、生成されたhash付きJS/CSSを `assets/` へコピーし、3つのHTMLの参照名を更新します。
データ再生成は研究環境のPythonで `seal/generate.py --research-source /path/to/animal_video_reid` を実行します。既存 `pair_history` と `prepare_pages.sanitized` を使用します。
チンパンジーのJS・CSS・JSON・映像は既存ファイルを保持し、入口リンクだけ追加しています。

作業: `codex/20261014-seal-demo`、元commit `1648ddd`、専用worktreeで既存の未コミット変更を隔離。push・公開は未実施。
検証pass: TypeScript・Vite build、既存Vitest 42件、Ruff、MP4の全フレームdecode、`git diff --check`。
ブラウザ検証pass（初版）: アザラシ全44フレームのBBox座標・有無、再生・シーク、一時追跡カード、架空の関係がないこと、JS/HTTPエラーなし。
既存 `smoke_pages.py` もpass: チンパンジー3動画の再生、AI/GT切替、プロフィール・参照画像、関係選択、全画面、3画面幅、reload。
最後の安全地点: 元commitを保持した未コミット差分。元のチンパンジー資産は保持。次の操作は必要時の差分レビューで、push・公開には別途明示要求が必要です。

追加milestone（2026-10-14）: 2本を追加し計3本・160フレーム。変更は映像2本、対応JSON2本、catalog、生成処理、説明表示・初期シーク、source patch、READMEに限定。
検証pass: 3本の全160フレームのBBox座標・有無、動画切替・シーク・再生、架空の辺なし、チンパンジー入口、JS/HTTPエラーなし。TypeScript/Vite、42テスト、Ruff、3本のMP4全decodeもpass。個体対応は動画内に限定し、各動画間の同一性は未確認。

複数頭milestone（2026-10-14）: Commons由来の2頭同時遊泳を1本追加し計4本。手動追跡2件と既存の画像上の共起・近接計算を使用。UI変更は追跡カードの動画別絞り込み、初期動画、出典・ライセンス表示に限定。
検証pass: 全4動画・180フレームのBBox座標と有無、2追跡カード・共起辺、動画ごとのノード切替、再生・シーク、チンパンジー入口、JS/HTTPエラーなし。TypeScript/Vite、既存42テスト、Ruff、追加MP4 decode、出典SHA256一致もpass。社会関係・動画間の個体対応は未確認。未コミット差分を保持し、push・公開は未実施。

## 鯉・ハト・豚（同じ観測画面の形式）

http://127.0.0.1:5189/animals.html で動物種・動画カードを切り替えます。既存の動画再生・BBox・個体プロフィール・Graph・共起表示を再利用し、チンパンジーの元資産は保持しています。
`animal_video_reid/convert_animal_videos.py` で変換済みの `web/public/datasets` を再利用しました。新規モデル・学習・推論はありません。AI切替は無効です。
鯉9個体・536フレーム、ハト17個体・600フレーム、豚26個体・500フレーム。IDは動画内の人手注釈であり、実在の名前・性格・社会関係を付けていません。
出典: Ludmila I. Kuncheva, José Luis Garrido-Labrador, Ismael Ramos-Pérez, Samuel L. Hennessey, Juan J. Rodriguez, *Animal Re-Identification from Video*, https://zenodo.org/records/7322821 。注釈はCC BY 4.0、元映像は寄託者記載のPixabay Licenseです。
動画の単体再配布用ダウンロードは提供しません。公開素材は観測UI・注釈・個体画像と一体で利用します。追加の加工は実動画プレビューの切り出しです。詳細: `datasets/LICENSE.txt` 。元ZIP・モデル重み・SealID画像は含みません。
現在の安全地点: 専用codex branchで既存公開branchの履歴を保持して統合。ユーザーの明示要求により公開branchへpushする。元データZIP、重み、SealID画像は公開対象に含めない。
検証pass（今回）: アザラシ5動画・370フレームのBBox同期、19秒再生と3本の一時追跡区間、動画カード5枚、鯉・ハト・豚の動画カード3枚・GT ID選択・参照画像・共起図・再生・シーク・390px表示、チンパンジーへ戻る操作。JS/HTTPエラーなし。TypeScript/Vite、既存42テスト、Ruff、19秒MP4 decodeもpass。
差分は19秒MP4・対応JSON・追跡定義、変換済み3種のデータと既存viewer、共通UIの動画カード・入口・アイコン・出典表示、READMEとsource patchです。BBox精度や再識別精度のベンチマークではありません。

統合・公開milestone: 5種をページ再読み込みなしで切替、選択状態をURLへ保持。相関図の動きを動画時刻・BBoxへ接続。既存公開commit `69ca7ba` をmergeして履歴を保全し、Pages対象の `codex/20261013-pages` へfast-forward pushする。force push・新規学習・LLM APIは使用しない。
検証pass: TypeScript/Vite、45テスト、5種の再読み込みなしの切替、動く相関図・シーク復帰・一時停止・再生、動物種のURL保存、19秒動画、スマホ表示、JS/HTTPエラーなし。既存チンパンジー3動画のAI/GT・プロフィール・全画面・3画面幅も既存smokeでpass。画像上の運動に連動する模式図であり、社会関係やBBox精度の評価ではありません。
仮名表示milestone: アザラシ3・鯉9・ハト17・豚26の計55追跡／注釈IDに展示用の仮名を設定。元IDとチンパンジーの名前は保持。検証pass: 45テスト、TypeScript/Vite、全55仮名のBBox・個体カード・相関図表示、仮名の注意書き、チンパンジー表示、JS/HTTPエラーなし。

アザラシ動画保存: 選択中の動画をMP4で保存できるリンクを追加。5本の短区間動画は `seal/media/` に保存済み。保存ファイルは映像のみで、BBox・仮名・相関図はUI上で同期表示する。相関図は観測した同時出現・近接であり、社会関係ではない。再利用時は画面の出典・ライセンスを参照。

保存リンク検証pass: 5本すべてのダウンロードSHA256が保存済みMP4と一致、出典への移動、全動画decode、45テスト、TypeScript/Vite。5種の相関図移動・シーク復帰・停止・再生とスマホ表示もpass。

## アザラシのマッピング済み動画

`seal/downloads/seal_harbor_19s-mapped.mp4` はBBox・仮名と動画同期の観測相関図を焼き込んだ19秒・1280×720・10fpsの無音MP4です。手動BBox（補間あり）であり、AI検出結果ではありません。表示名は仮名、辺は注釈共起で社会関係ではありません。加工動画もCC BY-SA 2.0で提供し、作者・出典・変更内容を `seal/downloads/LICENSE.txt` と動画内へ記載しています。
既存 `animal_video_reid/export_demo_videos.py` のPlaywrightフレーム描画→FFmpeg方式を再利用。再生成: `python3 seal/export_mapped.py --output /path/to/new-directory` （ローカル観測UIを5189で起動、Playwright/ChromiumとFFmpegが必要）。元MP4は `seal/media/` に保持。変更はエクスポート処理、加工動画と利用条件、保存リンクに限定。

加工動画検証pass: 190フレーム・19秒・1280×720・10fps、全decode、4秒時点のBBox2件以上と相関辺、焼き込み画像の目視確認、ダウンロードSHA256一致。45テスト、TypeScript/Vite、Ruff、全仮名表示と5種の相関図・シーク・再生回帰もpass。

映像内矢印への修正: `seal/downloads/seal_harbor_19s-arrows.mp4` はチンパンジーと同じ `RelationshipOverlay` を再利用し、映像内の2頭間に共起矢印と「共起」を焼き込む。別枠の相関図は動画に含めない。UIでも「映像にも関係線」で表示／非表示を切り替え可能。矢印は社会関係・行動方向を示さない。

映像内矢印検証pass: 再生時刻に応じた矢印位置の変化、関係線チェックによる表示切替、焼き込みプレビューの目視、19秒・190フレーム・1280×720。TypeScript/Vite・45テスト・Ruff・仮名と既存5種の動作回帰もpass。

設定つながりmilestone: 共起表示をやめ、全55件の仮名と元IDを保持したまま、アザラシ・鯉・ハト・豚の関係種類をID順で固定。表示時刻・選択・入力順で同じペアの種類は変わらない。Unknownには設定しない。全種のUIと保存アザラシ動画でBBox枠を隠す。新規学習・推論・依存追加なし。

設定つながり検証pass: 48テスト（順序に依存しないID固定・自己関係／重複なしを追加）、TypeScript/Vite、Prettier、Ruff。全5種で枠非表示、共起ラベルなし、仮関係のシーク時固定、矢印表示切替を確認。55仮名、既存動画切替・相関図の動き・スマホ表示も回帰pass。アザラシ19秒MP4の全decodeと枠なし・友達矢印の焼き込みを目視確認。

スマホ文字サイズ調整（2026-10-15）: 映像幅480px未満では名前と矢印ラベルを映像幅に比例して縮小。600px以下の画面では相関図カード名12px、関係文字9px。390px幅で全5種の名前15px以下・矢印ラベル13px以下・横溢れなしを確認し、PCのアザラシ名20pxは維持。48テスト・TypeScript/Vite・Prettierと仮関係／枠なし回帰もpass。保存MP4は変更せず、レスポンシブUIだけを変更。

## Additional GT animal demos

datasets/ contains koi, pigeons and pigs from Animal Re-Identification from Video, https://zenodo.org/records/7322821 . Dataset annotations: CC BY 4.0; original stock videos: Pixabay License. These media are integrated into the interactive GT viewer, not offered as standalone downloads. Individual IDs are video-local ground truth, not AI predictions. Display names and ID-fixed relationship labels are fictional exhibition settings, not observed social facts. Original annotation data is unchanged. Full authors, provenance and modifications: datasets/LICENSE.txt. The original ChimpACT files keep their separate CC BY-NC 4.0 license.
