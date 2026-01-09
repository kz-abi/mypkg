# PID制御シミュレータ
![test](https://github.com/kz-abi/mypkg/actions/workflows/test.yml/badge.svg)

ROS 2を用いた1次遅れ系プラントのPID制御シミュレータです。

## ノードと入出力
### `plant`
1次遅れ系の物理モデルをシミュレートするノードです。
* **Sub**: `/count_up` (`std_msgs/msg/Int16`)
  * コントローラからの操作量を受け取ります。
* **Pub**: `/current_val` (`std_msgs/msg/Int16`)
  * 現在の状態量（出力値）を計算して送信します。

### `controller`
PID制御を行うコントローラのノードです。
* **Sub**: `/current_val` (`std_msgs/msg/Int16`)
  * プラントの出力値を受け取ります。
* **Pub**: `/count_up` (`std_msgs/msg/Int16`)
  * 目標値（50.0）に近づけるための操作量を送信します。

## 実行方法
Launchファイルを使用して、制御対象とコントローラを同時に起動します。
```bash
$ ros2 launch mypkg mypkg.launch.py
```

## 動作確認
以下のコマンドで、ノード間の通信とPID制御の収束を自動で検証できます。
```bash
$ cd test
$ bash ./test.bash
```

## 実行環境
* ROS 2 Humble
* Python 3.10

## ライセンス
* このソフトウェアパッケージは、3条項BSDライセンスの下、再頒布および使用が許可されます。
* © 2025 kz-abi
