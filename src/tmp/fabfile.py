from fabric.api import run,put,cd,env,local
import shutil,os
import py_compile

__author__ = 'Joseph'

UpxEXE = os.path.join(os.getcwd(),"usr/bin/upx.exe")
SevenZipEXE = os.path.join(os.getcwd(),"usr/bin/7z.exe")
dist_dir = os.path.join(os.getcwd(),"dist")
pro_dir = os.getcwd()

def unzip(zip_file,out_dir):
    local(SevenZipEXE+' -aoa x "'+zip_file+'" -o "'+out_dir+'"')


def upx(dir,files = "*.*"):
    print "upx ... "+dir
    os.chdir(dir)
    local(UpxEXE+" --best "+files)

def copydir(dir):
    from_dir = os.path.join(pro_dir,dir)
    to_dir = os.path.join(dist_dir,dir)
    print "copy dir from :"+ from_dir + " to :" +to_dir
    shutil.copytree(from_dir,to_dir)

def copyfile(file):
    from_dir = os.path.join(pro_dir,file)
    to_dir = os.path.join(dist_dir,file)
    print "copy file from :"+ from_dir + " to :" +to_dir
    shutil.copy(from_dir,to_dir)

def build_pyc():
    py_compile.compile('library/AppCore.py')
    py_compile.compile('library/__init__.py')
    py_compile.compile('App.py')

def pre_build():
    if os.path.isdir(os.path.join(pro_dir,"build")):
        print "delete ./build"
        shutil.rmtree(os.path.join(pro_dir,"build"))
    if os.path.isdir(os.path.join(pro_dir,"dist")):
        print "delete ./dist"
        shutil.rmtree(os.path.join(pro_dir,"dist"))


def compress():
    os.chdir(dist_dir)
    output_zip = os.path.join(pro_dir,"Output/setup.zip")
    if os.path.isfile(output_zip):
        os.remove(output_zip)
    if os.path.isdir(os.path.dirname(output_zip)) == False:
        os.mkdir(os.path.dirname(output_zip))
    print "compress " +dist_dir+" to " + output_zip
    local(SevenZipEXE + ' a -tzip -mx9 "'+output_zip+'" -r')

def package_to_setup():
    #http://www.jrsoftware.org/ishelp/index.php?topic=compilercmdline
    os.chdir(pro_dir)
    local("iscc setup_script.iss")

def build():
    pre_build()
    print "build ptserver"
    local("python build_run.py py2exe")
    upx(dist_dir,"*.exe")
    os.chdir(pro_dir)
    copyfile("config.cfg")
    dirs = [
        'imageformats',
        'Microsoft.VC90.CRT',
        'var/res',
        'usr/bin',
        'usr/local/php/53',
        'usr/local/mysql',
        'usr/local/openssl',
        'usr/local/memcached',
        'usr/local/mongodb',
        'usr/local/ssdb-bin',
    ]
    for dir in dirs:
        copydir(dir)

    os.remove(os.path.join(dist_dir,"usr/bin/winscp.ini"))




