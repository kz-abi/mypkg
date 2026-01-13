# PID制御シミュレータ (mypkg)
![test](https://github.com/kz-abi/mypkg/actions/workflows/test.yml/badge.svg)

ROS 2を用いたPID制御パッケージです。
汎用的な**PIDコントローラ**と、動作確認用の**1次遅れ系プラントモデル**が含まれています。

本パッケージのコントローラは、トピックのリマッピングを行うことで、他パッケージのロボットやシミュレータの制御に使用することを想定しています。

## ノードと入出力
### `controller`
汎用のPID制御ノードです。外部のロボット（プラント）からのセンサ値を受け取り、操作量を計算して返します。

* **Subscriber**: `current_val` (`std_msgs/msg/Float32`)
  * 制御対象からのセンサ値（現在値）を受け取ります。
  * **他パッケージとの連携**: 制御したいロボットの状態量トピックにリマップして接続してください。
* **Publisher**: `control_input` (`std_msgs/msg/Float32`)
  * PID計算後の操作量を出力します。
  * **他パッケージとの連携**: ロボットの指令値トピックにリマップして接続してください。

### `plant`
動作確認用の、1次遅れ系物理モデルを模擬したノードです。
* **Subscriber**: `control_input` (`std_msgs/msg/Float32`)
  * コントローラからの操作量を受け取ります。
* **Publisher**: `current_val` (`std_msgs/msg/Float32`)
  * 物理モデル計算後の現在値を出力します。

## 使用方法

### 1. このパッケージ単体で動作確認する場合
同梱のLaunchファイルを使用し、コントローラと模擬プラントによる閉ループ制御を実行します。
```bash
$ ros2 launch mypkg mypkg.launch.py
```

### 2. 他のパッケージ（ロボット）を制御する場合
`controller` ノード単体を起動し、トピックを制御対象に合わせてリマップしてください。
以下は、`my_robot` という別パッケージのロボットを制御する場合の例です。

```bash
# 例: /sensor_data を受け取り、/motor_cmd に指令を出す場合
$ ros2 run mypkg controller --ros-args -r current_val:=/sensor_data -r control_input:=/motor_cmd
```

## テスト・検証
以下のスクリプトを実行することで、コントローラの収束性能を検証できます。

```bash
$ cd test
$ ./test.bash
```

### 検証結果の見方
スクリプト実行後、以下の条件を満たすと成功とみなされます。
* **成功判定**: 目標値（50.0）に対し、定常偏差が許容範囲（49.0〜50.0付近）に収束していること。
* **出力ログ**: 実行ディレクトリに生成されるログファイルを確認し、数値が安定していれば制御成功です。画面には `Test Passed` と表示されます。

## 実行環境
* ROS 2 Humble
* Python 3.10

## ライセンス
* このソフトウェアパッケージは、3条項BSDライセンスの下、再頒布および使用が許可されます。
* 2025 kz-abi
