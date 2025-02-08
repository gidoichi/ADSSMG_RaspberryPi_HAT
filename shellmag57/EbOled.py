import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class EbOled(Adafruit_SSD1306.SSD1306_128_64):

  WIDTH = 128
  HEIGHT = 64

  __RST = 24
  __DC = 23
  SPI_PORT = 0
  SPI_DEVICE = 0

  DEFAULT_FONT = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
  FONT_SIZE = 14
  _LINE_HEIGHT = 16

  def __init__(self):
    self.__spi = SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE, max_speed_hz=8000000)
    super().__init__(rst=self.__RST, dc=self.__DC, spi=self.__spi)
    self._image = Image.new('1', (self.WIDTH, self.HEIGHT) ,0)
    self._draw = ImageDraw.Draw(self._image)
    self._font = ImageFont.truetype(self.DEFAULT_FONT, self.FONT_SIZE, encoding='unic')

  def image(self, image):
    self._image = image
    super().image(self._image)

  def drawString(self, str, line=0):
    self._draw.rectangle((0, line*self._LINE_HEIGHT, self.WIDTH,line*self._LINE_HEIGHT+self._LINE_HEIGHT), fill=(0))
    self._draw.text((0, line*self._LINE_HEIGHT), str, font=self._font, fill=1)
    self.image(self._image)
