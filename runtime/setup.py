# -*- coding: utf-8 -*-
"""
@author: tambre /Modifications by Anarchon
@version: v0.2
"""

import os
import re
import sys
import getopt
import shutil
import zipfile
import subprocess



def dlProgress(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize)
      sys.stdout.write("\rDownload: " + xxxname + "       %d%%" % percent)
      sys.stdout.flush()

def startProcess(command):
        import shlex
        args = shlex.split(command)
        p = subprocess.Popen(args)
        p.communicate()[0]

def getArgument(line):
	cfg = open(os.path.join(os.getcwd(), "conf", "smcp.cfg"), "r")
	lines = cfg.readlines()
	line = lines[line].strip()
	ver = line.split('=', 1)[1]
	return ver

def getStarMadeBuild(file, web, workingDir, smbuild, smbuildsize, invalid):
        #TO-DO: Fix progress display
        if invalid:
                print ('*   Found invalid StarMade build zip, downloading new one')
        print ('*   Getting new StarMade... (' + str(os.path.getsize(os.path.join(workingDir, 'install','starmade-build_' + smbuild + '.zip')) / 1024) + 'KB/' + smbuildsize + 'KB)')
        print ('')
       
    

def main(argv):
        global rem_file
        global xxxname
        ignoreupdates = False
        hasfailed = False
        try:
                opts, args = getopt.getopt(argv, "iu", ["ignoreupdates"])
        except getopt.GetoptError:
                print ("Failed to parse arguments")
                print ("Arguments:")
                print ("ignoreupdates/iu - Disables updating")
                sys.exit()
        for opt, arg in opts:
                if opt in ("-iu", "-ignoreupdates"):
                        ignoreupdates = True
        print ('-----------------------------------------')
        print ('--------- Welcome to SMCP v%s ---------' % getArgument(0))
        print ('-----------------------------------------\n')
        workingDir = os.getcwd()
        smver = getArgument(1)
        smbuild = getArgument(2)
        smbuildsize = getArgument(4)
        if ignoreupdates == False:
                foundUpdates = False
                print ('Checking for updates...')
                if os.path.isfile(os.path.join(workingDir, 'install', 'starmade-build_' + smbuild + '.zip')):
                        if not zipfile.is_zipfile(os.path.join(workingDir, 'install', 'starmade-build_' + smbuild + '.zip')):
                                import urllib.request
                                import urllib.error
                                
                                os.remove(os.path.join(workingDir, 'install', 'starmade-build_' + smbuild + '.zip'))
                                rem_file = r'http://files.star-made.org/build/starmade-build_' + smbuild + '.zip'
                                xxxname='starmade-build_' + smbuild + '.zip'         
                                spath=os.path.join(workingDir, 'install', 'starmade-build_' + smbuild + '.zip')
                                urllib.request.urlretrieve(rem_file,spath, reporthook=dlProgress)
                else:
                      
                        import urllib.request
                        import urllib.error
                       
                        rem_file = r'http://files.star-made.org/build/starmade-build_' + smbuild + '.zip'                   
                        spath=os.path.join(workingDir, 'install', 'starmade-build_' + smbuild + '.zip')
                        xxxname='starmade-build_' + smbuild + '.zip'
                        urllib.request.urlretrieve(rem_file,spath, reporthook=dlProgress)


                      
                if foundUpdates == False:
                        print ('')
        elif not zipfile.is_zipfile(os.path.join(workingDir, 'install', 'starmade-build_' + smbuild + '.zip')):
                print ("Invalid zip file!")
        print ('Extracting StarMade v' + smver + '\n')
        if not os.path.exists('instance') and not os.path.isdir('instance'):
                os.makedirs('instance')
        if not os.path.exists('tmp') and not os.path.isdir('tmp'):
                os.makedirs('tmp')
        if not os.path.exists('conf') and not os.path.isdir('conf'):
                os.makedirs('conf')
        unzip(os.path.join(workingDir, 'install', 'starmade-build_' + smbuild + '.zip'), os.path.join(workingDir, 'instance'))
        print ('Decompiling StarMade is not working now')
        #print ('*   Deobfuscating... (Stage #1) (DISABLED)')
        #print ('*       Not here yet, skipping')
        #startProcess("java -Xmx1G -jar runtime/N3Remapper.jar conf/remapper.cfg pre instance/StarMade.jar tmp/deobf.zip")
        print ('*   Decompiling...   (Stage #2) (DISABLED)\n')
        print ('*   -(This can take several hours..)')
        if not os.path.exists('src') and not os.path.isdir('src'):
                os.makedirs('src')
        #tmp/deobf.zip when we have implemented SpecialSource
        #startProcess('java -Xmx1G -jar runtime/fernflower.jar' + workingDir + 'install/StarMade.zip sources')
        startProcess("java -Xmx1G -jar runtime/bin/fernflower.jar instance/StarMade.jar src")
        print ('Setting up Eclipse workspace\n')
        unzip(os.path.join(workingDir, "install", "EclipseWorkspace.zip"), workingDir)
        if os.path.exists(workingDir + 'tmp'):
                print ('Deleting temporary files\n')
                shutil.rmtree(workingDir + 'tmp')
        endMessage(hasfailed)

def endMessage(failed):
        if failed:
                print ('-----------------------------------------')
                print ('----------- SMCP setup failed -----------')
                print ('-----------------------------------------')
        else:
                print ('-----------------------------------------')
                print ('- SMCP Is now ready for mod development -')
                print ('-----------------------------------------')
	
def unzip(zipFilePath, destDir):
        zfile = zipfile.ZipFile(zipFilePath)
        for name in zfile.namelist():
                (dirName, fileName) = os.path.split(name)
                if fileName == '':
                        newDir = os.path.join(destDir, dirName)
                        if not os.path.exists(newDir):
                                os.mkdir(newDir)
                else:
                        fd = open(os.path.join(destDir, name), 'wb')
                        fd.write(zfile.read(name))
                        fd.close()
        zfile.close()
	
if __name__ == "__main__":
	main(sys.argv[1:])
