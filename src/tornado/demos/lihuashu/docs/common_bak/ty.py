#coding:utf8
from img import Img
i=Img()
i.open()
k=i.convert_thumbnail(input_file="/home/insion/Pictures/l.jpg",output_file="/home/insion/Pictures/toutput.jpg")
print(k)
k=i.convert_resize(input_file="/home/insion/Pictures/l.jpg",output_file="/home/insion/Pictures/loutput2.jpg",output_size="500x")
print(k)

ki=i.composite_watermark(watermark_file="/home/insion/Pictures/lhs_logo.png",input_file="/home/insion/Pictures/loutput2.jpg",output_file="/home/insion/Pictures/loutput.jpg")
print(ki)
ki=i.convert_watermark(watermark_file="/home/insion/Pictures/lhs_logo.png",input_file="/home/insion/Pictures/m.jpg",output_file="/home/insion/Pictures/moutput.jpg")
print(ki)