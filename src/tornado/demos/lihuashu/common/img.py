#coding:utf8

# Python bind ImageMagick by Insion
# Email:insion@live.com
import os
import subprocess

class Img:
        def open(self,img_path= "/opt/im/bin"):
                self.img_path=img_path

        def convert_thumbnail(self,input_file=None,output_file=None,output_size='100x100'):
                #整张图片缩小成一定比例,然后填充空白的地方.
                #convert -thumbnail 200x200 -background white -gravity center -extent 200x200 input_file.jpg output_file.jpg
                img_bin=os.path.join(self.img_path,'convert')
                s=subprocess.Popen([img_bin,'-thumbnail',output_size,'-background','white','-gravity','center','-extent',output_size,input_file,output_file], stdout=subprocess.PIPE)
                sr=s.stdout.read()
                if sr:
                        print(sr)
                        return False
                else:
                        return True

        def convert_resize(self,input_file=None,output_file=None,output_size='100x100'):
                #按比例缩放,宽度和高度哪个比较大,按照大的比例缩放
                #convert -resize 100x200 input_file.jpg output_file.jpg
                img_bin=os.path.join(self.img_path,'convert')
                s=subprocess.Popen([img_bin,'-resize',output_size,input_file,output_file], stdout=subprocess.PIPE)
                sr=s.stdout.read()
                if sr:
                        print(sr)
                        return False
                else:
                        return True
                
        def convert_watermark(self,watermark_file=None,input_file=None,output_file=None):
                #convert -gravity southeast -geometry +20%+10% -composite input_file.jpg lhs_logo.png output_file.jpg               
                img_bin=os.path.join(self.img_path,'convert')
                s=subprocess.Popen([img_bin,'-gravity','southeast','-geometry','+20%+10%','-composite',input_file,watermark_file,output_file], stdout=subprocess.PIPE)
                sr=s.stdout.read()
                if sr:
                        print(sr)
                        return False
                else:
                        return True
                
        def composite_watermark(self,watermark_file=None,input_file=None,output_file=None):
                #composite -gravity southeast -dissolve 30 -geometry +15%+15%  lhslogo.png input_file.jpg output_file.jpg
                img_bin=os.path.join(self.img_path,'composite')
                s=subprocess.Popen([img_bin,'-gravity','southeast','-dissolve','100','-geometry','+20%+10%',watermark_file,input_file,output_file], stdout=subprocess.PIPE)
                sr=s.stdout.read()
                if sr:
                        print(sr)
                        return False
                else:
                        return True
                
        