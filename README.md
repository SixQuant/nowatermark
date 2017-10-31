# nowatermark
remove watermark. 去除图片中的水印

## Install

```
pip3 install nowatermark
```

## Usage

```
from nowatermark import WatermarkRemover

path = './data/'

watermark_template_filename = path + 'anjuke-watermark-template.jpg'
remover = WatermarkRemover()
remover.load_watermark_template(watermark_template_filename)

remover.remove_watermark(path + 'anjuke3.jpg', path + 'anjuke3-result.jpg')
remover.remove_watermark(path + 'anjuke4.jpg', path + 'anjuke4-result.jpg')

```

### Original
![Original](https://github.com/SixQuant/nowatermark/blob/master/data/anjuke2.jpg)

### Removed watermark
![Removed watermark](https://github.com/SixQuant/nowatermark/blob/master/data/anjuke2-result.jpg)
