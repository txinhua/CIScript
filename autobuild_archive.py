import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from optparse import OptionParser
import subprocess


CONFIGURATION = "Release"

def cleanBuildDir(buildDir):
	cleanCmd = "rm -r %s" %(buildDir)
	process = subprocess.Popen(cleanCmd, shell = True)
	process.wait()
	print "cleaned buildDir: %s" %(buildDir)

def buildProject(project, scheme, output, plistPath):
	process = subprocess.Popen("pwd", stdout=subprocess.PIPE)
	(stdoutdata, stderrdata) = process.communicate()

	archiveDir = stdoutdata.strip() + '/Archive/%s.xcarchive' %(scheme)
	print "archiveDir: " + archiveDir
	archiveCmd = 'xcodebuild archive -project %s -scheme %s -configuration %s -archivePath %s' %(project, scheme, CONFIGURATION, archiveDir)
	process = subprocess.Popen(archiveCmd, shell = True)
	process.wait()

	exportArchiveCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s' %(archiveDir, output, plistPath)
	process = subprocess.Popen(exportArchiveCmd, shell=True)
	(stdoutdata, stderrdata) = process.communicate()

	#cleanBuildDir("./build")

def buildWorkspace(workspace, scheme, output, plistPath):
	process = subprocess.Popen("pwd", stdout=subprocess.PIPE)
	(stdoutdata, stderrdata) = process.communicate()

	archiveDir = stdoutdata.strip() + '/Archive/%s.xcarchive' %(scheme)
	print "archiveDir: " + archiveDir
	archiveCmd = 'xcodebuild archive -workspace %s -scheme %s -configuration %s -archivePath %s' %(workspace, scheme, CONFIGURATION, archiveDir)
	process = subprocess.Popen(archiveCmd, shell = True)
	process.wait()

	exportArchiveCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s' %(archiveDir, output, plistPath)
	process = subprocess.Popen(exportArchiveCmd, shell=True)
	(stdoutdata, stderrdata) = process.communicate()

	# cleanBuildDir(buildDir)

def xcbuild(options):
	project = options.project
	workspace = options.workspace
	scheme = options.scheme
	output = options.output
	plistPath = options.plist

	if project is None and workspace is None:
		pass
	elif project is not None:
		buildProject(project, scheme, output, plistPath)
	elif workspace is not None:
		buildWorkspace(workspace, scheme, output, plistPath)

def main():
	
	parser = OptionParser()
	parser.add_option("-w", "--workspace", help="Build the workspace name.xcworkspace.", metavar="name.xcworkspace")
	parser.add_option("-p", "--project", help="Build the project name.xcodeproj.", metavar="name.xcodeproj")
	parser.add_option("-s", "--scheme", help="Build the scheme specified by schemename. Required if building a workspace.", metavar="schemename")
	parser.add_option("-o", "--output", help="specify output filePath+filename", metavar="output_filePath+filename")
	parser.add_option("-l", "--plist", help="specify plist filePath+filename", metavar="plist_filePath+filename")

	(options, args) = parser.parse_args()

	print "options: %s, args: %s" % (options, args)

	xcbuild(options)

if __name__ == '__main__':
	main()
