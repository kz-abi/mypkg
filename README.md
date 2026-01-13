# PID制御パッケージ (mypkg)
![test](https://github.com/kz-abi/mypkg/actions/workflows/test.yml/badge.svg)

ROS 2を用いたPID制御パッケージです。
汎用的な**PIDコントローラ**と、動作確認用の**1次遅れ系プラントモデル**が含まれています。

本パッケージの `controller` ノードは、トピックのリマッピングを行うことで、他パッケージのロボットやシミュレータの制御に使用することを想定しています。

## ノードと入出力
### `controller`
汎用のPID制御ノードです。外部のロボット（プラント）からのセンサ値を受け取り、目標値（固定）に近づけるための操作量を計算して出力します。

* **Subscriber**: `current_val` (`std_msgs/msg/Float32`)
  * 制御対象からのセンサ値（現在値）を受け取ります。
  * **接続方法**: 制御したいロボットの状態量トピック（例: `/motor_speed`, `/distance`）にリマップして接続してください。
* **Publisher**: `control_input` (`std_msgs/msg/Float32`)
  * PID計算後の操作量を出力します。
  * **接続方法**: ロボットの指令値トピック（例: `/motor_cmd`, `/cmd_vel`）にリマップして接続してください。

### `plant`
動作確認用の、1次遅れ系物理モデルを模擬したノードです。
* **Subscriber**: `control_input` (`std_msgs/msg/Float32`)
  * コントローラからの操作量を受け取ります。
* **Publisher**: `current_val` (`std_msgs/msg/Float32`)
  * 物理モデル計算後の現在値を出力します。
  * 動作確認用に `[INFO] ... Data: <数値>` という形式でログ出力も行います。

## 使用方法

### 1. このパッケージ単体で動作確認する場合
同梱のLaunchファイルを使用し、コントローラと模擬プラントによる閉ループ制御を実行します。
```bash
$ ros2 launch mypkg mypkg.launch.py
```

### 2. 他のパッケージ（ロボット）を制御する場合
`controller` ノード単体を起動し、トピックを制御対象に合わせてリマップしてください。

**実行例：`/sensor_data` を受け取り、`/motor_cmd` に指令を出す場合**
```bash
$ ros2 run mypkg controller --ros-args -r current_val:=/sensor_data -r control_input:=/motor_cmd
```
※ 相手側のトピックの型は `std_msgs/msg/Float32` である必要があります。

## テスト・検証
以下のスクリプトを実行することで、コントローラの収束性能を自動検証できます。

```bash
$ cd test
$ ./test.bash
```

### 検証結果の見方
スクリプトが自動的にログを監視し、**目標値 50.0** への収束を確認します。

* **成功時**: 制御が安定し、画面に以下のようなログが表示されれば成功です。
  ```text
  [INFO] [plant]: Data: 49.0...
  ```
  （目標値 **50.0** 付近の数値を含むログ行が表示されます）

* **失敗時**:
  何も表示されずに終了します（終了ステータスが1になります）。

## 実行環境
* ROS 2 Humble
* Python 3.10

## ライセンス
* このソフトウェアパッケージは、3条項BSDライセンスの下、再頒布および使用が許可されます。
* © 2025 kz-abi
