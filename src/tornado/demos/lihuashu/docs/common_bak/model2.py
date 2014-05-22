from kyototycoon import KyotoTycoon
import sys,time

# sample usage
kt = KyotoTycoon()
kt.open("localhost", 1978)
kt.set("japan:sexy", "tokyo00000ooo")
#build for masks form
cid =0
for i in range(0,100):
         cid +=1
         if not kt.set("mask:"+str(cid)+":maskid", str(cid)) or\
            not kt.set("mask:"+str(cid)+":userid", str(cid)) or\
            not kt.set("mask:"+str(cid)+":boardid", str(cid)) or\
            not kt.set("mask:"+str(cid)+":fileid", str(cid)) or\
            not kt.set("mask:"+str(cid)+":description", str("Mask的内容描述")) or\
            not kt.set("mask:"+str(cid)+":content", str("哇。。阳光暖暖的，好惬意的。")) or\
            not kt.set("mask:"+str(cid)+":ups",bytes(int("100"))) or\
            not kt.set("mask:"+str(cid)+":downs",bytes(int("10"))) or\
            not kt.set("mask:"+str(cid)+":hits",bytes(int("110"))) or\
            not kt.set("mask:"+str(cid)+":order", bytes(cid)) or\
            not kt.set("maks:"+str(cid)+":createdata",str(int(time.time()))) or\
            not kt.set("maks:"+str(cid)+":commentcount","8") or\
            not kt.set("mask:count", "3"):
                  print >>sys.stderr, "set error: " + str(kt.error())

k=kt.get("mask:100:content")
print(str(k,'UTF-8'))
#kt.remove("japan:sexy")
kt.close()