
'''
>>> import PythonMagick
>>> dir(PythonMagick.Image())

['__class__', '__delattr__', '__dict__', '__doc__',
'__eq__', '__format__', '__ge__', '__getattribute__',
'__gt__', '__hash__', '__init__', '__instance_size__', 
'__le__', '__lt__', '__module__', '__ne__', '__new__',
'__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
'__sizeof__', '__str__', '__subclasshook__', 
'__weakref__', 'adaptiveThreshold', 'addNoise', 
'adjoin', 'affineTransform', 'animationDelay', 
'animationIterations', 
'annotate',
'antiAlias', 
'attribute',
'backgroundColor', 'backgroundTexture', 
'baseColumns', 'baseFilename', 'baseRows', 
'blur', 
'border',
'borderColor', 'boundingBox', 'boxColor',
'cacheThreshold', 'channel', 'channelDepth', 'charcoal', 
'chop', 'chromaBluePrimary', 'chromaGreenPrimary', 
'chromaRedPrimary', 'chromaWhitePoint', 'classType', 
'clipMask', 'colorFuzz', 'colorMap', 'colorMapSize', 
'colorSpace', 'colorize', 'columns', 'comment', 'compare', 
'compose', 'composite', 'compressType', 'contrast', 
'convolve', 'crop', 'cycleColormap', 'debug', 'defineSet', 
'defineValue', 'density', 'depth', 'despeckle', 
'directory', 'display', 'draw', 'edge', 'emboss', 'endian', 
'enhance', 'equalize', 'erase', 'fileName', 
'fileSize', 'fillColor', 'fillPattern', 'fillRule', 'filterType', 
'flip', 'floodFillColor', 'floodFillOpacity', 
'floodFillTexture', 'flop', 
'font', 'fontPointsize', 'fontTypeMetrics', 'format',
'frame', 'gamma', 
'gaussianBlur',
'geometry',
'gifDisposeMethod',
'iccColorProfile', 
'implode',
'interlaceType', 
'iptcProfile',
'isValid', 
'label', 
'lineWidth',
'magick', 
'magnify',
'map', 'matte', 'matteColor', 'matteFloodfill', 
'meanErrorPerPixel', 'medianFilter', 'minify', 
'modifyImage',
'modulate', 'modulusDepth', 'monochrome', 
'montageGeometry', 'negate', 'normalize', 
'normalizedMaxError', 
'normalizedMeanError', 'oilPaint', 'opacity', 
'opaque', 'page', 'penColor', 'penTexture', 'ping', 
'pixelColor', 
'process', 'profile', 'quality', 'quantize',
'quantizeColorSpace', 'quantizeColors', 'quantizeDither', 
'quantizeTreeDepth', 'raise', 'read', 'readPixels', 
'reduceNoise', 'registerId', 'renderingIntent',
'resize',
'resolutionUnits', 
'roll',
'rotate', 
'rows', 
'sample',
'scale', 'scene', 'segment', 
'shade', 'sharpen', 'shave', 
'shear', 'signature', 'size', 
'solarize', 'spread', 
'statistics', 'stegano', 
'stereo', 'strokeAntiAlias', 
'strokeColor', 'strokeDashOffset', 
'strokeLineCap', 
'strokeLineJoin', 'strokeMiterLimit', 
'strokePattern',
'strokeWidth', 'subImage', 'subRange', 
'swirl',
'syncPixels', 'textEncoding', 'texture', 'threshold', 
'throwImageException', 'tileName', 'totalColors', 
'transform', 'transformOrigin', 'transformReset', 
'transformRotation', 'transformScale', 'transformSkewX',
'transformSkewY', 'transparent', 'trim', 'type', 
'unregisterId', 'unsharpmask', 'verbose', 'view', 'wave', 
'write',
'writePixels',
'x11Display',
'xResolution',
'yResolution', 
'zoom']
'''

from PythonMagick import Image,Blob
#img = PythonMagick.Image("/home/insion/Pictures/k.jpg")

data=file('/home/insion/Pictures/o.jpg','rb').read()
img=Image(Blob(data))
img.resize('490')
img.write('k2k.jpg')
print("ok")

#k=fs.upload("/home/insion/Pictures/k.jpg")
#print(k)
#fs.delete("groupserver1/M00/00/00/wKhqTk_GwtDUaSWdAARGywFLfVc321.jpg")

