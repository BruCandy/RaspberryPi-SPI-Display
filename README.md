# RaspberryPi-SPI-Display

このプロジェクトは、 **Raspberry Pi Pico** を使用して、**MSP2807** とSPI通信を行うものです。

## ファイル構成
このプロジェクトの主要なディレクトリとファイルの構成について説明します。

### draw_square/
- **概要**: 正方形を描画するための実装が含まれています。
- **主なファイル**
  - main.py : 
  - ili9341_init.py : 
  - ili9341_clear.py : 
  - square.py : 

### draw_petersen_graph/
- **概要**: ペテルセングラフを描画するための実装が含まれています。
- **主なファイル**
  - main.py : 
  - ili9341_init.py : 
  - ili9341_clear.py : 
  - petersen_graph.py : 

### draw_picture/
- **概要**: 画像を描画するための実装が含まれています。
- **主なファイル**
  -- data/ : 表示する画像を格納
  - main.py : 
  - ili9341.py :


## 参考
このプロジェクトでは、コマンドおよびデータ送信のタイミングの参考として、
MITライセンスで公開されている [rdagger/micropython-ili9341](https://github.com/rdagger/micropython-ili9341) の ili9341.py を参照しました。