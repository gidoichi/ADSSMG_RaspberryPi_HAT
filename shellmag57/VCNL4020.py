# https://www.vishay.com/docs/83476/vcnl4020.pdf

import smbus
import time
from threading import BoundedSemaphore

class VCNL4020():

  _ALS_OD       = 0b00010000  # オンデマンド明るさ計測スタート
  _PROX_OD      = 0b00001000  # オンデマンド近接計測スタート
  _ALS_EN       = 0b00000100  # 明るさ繰り返し計測有効
  _PROX_EN      = 0b00000010  # 近接繰り返し計測有効
  _SELFTIMED_EN = 0b00000001  # 内蔵タイマー有効

  _CONT_CONV    = 0b10000000  # Continue Conversion有効
  _AMBIENT_RATE = 0b00010000  # 明るさの計測レート（default:2sample/s）
  _AUTO_OFFSET  = 0b00001000  # 自動オフセットモード有効
  _AVERAGING    = 0b00000101  # 平均化（default:32conv）

  _COMMAND_REG       = 0x80  # コマンドレジスタ
  _PID_REG           = 0x81  # プロダクトIDレジスタ
  _PROX_RATE_REG     = 0x82  # 近接測定レートジスタ
  _IR_CURRENT_REG    = 0x83  # 近接測定用赤外線LED電流設定レジスタ（default=20mA）
  _AMBIENT_PARAM_REG = 0x84  # 明るさセンサーパラメータレジスタ

  _AMBIENT_MSB       = 0x85  # 明るさ上位バイト
  _AMBIENT_LSB     = 0x86  # 明るさ下位バイト

  _PROX_MSB          = 0x87  # 近接上位バイト
  _PROX_LSB          = 0x88  # 近接下位バイト

  def __init__(self, i2c_addr = 0x13, busno = 1):
    self.addr = i2c_addr
    self.i2c = smbus.SMBus(busno)

    self._write_reg(self._COMMAND_REG, self._ALS_OD  |\
                       self._PROX_OD |\
                       self._ALS_EN  |\
                       self._PROX_EN |\
                       self._SELFTIMED_EN )

    self._write_reg(self._IR_CURRENT_REG, 2 )  # 20mA

    self._write_reg(self._AMBIENT_PARAM_REG, self._CONT_CONV    |\
                         self._AMBIENT_RATE |\
                         self._AUTO_OFFSET  |\
                         self._AVERAGING )
    self.semaphore = BoundedSemaphore()
    time.sleep(0.6)      # 初回測定まで待つ

  def _write_reg(self, reg, value):
    self.i2c.write_byte_data(self.addr, reg, value)

  @property
  def luminance(self):
    self.semaphore.acquire()
    d = self.i2c.read_i2c_block_data(self.addr, self._AMBIENT_MSB, 2)
    self.semaphore.release()
    return (d[0] * 256 + d[1])

  @property
  def proximity(self):
    self.semaphore.acquire()
    d = self.i2c.read_i2c_block_data(self.addr, self._PROX_MSB, 2)
    self.semaphore.release()
    return (d[0] * 256 + d[1])
