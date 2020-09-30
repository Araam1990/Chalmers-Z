import sys
import wordfreq
import urllib.request

if len(sys.argv) < 4:
    print("topmost.py {stopfile} {wordfile} {count}")
    sys.exit(0)

def main(stopfilepath, wordfilepath, count):
    if wordfilepath.startswith("http://") or wordfilepath.startswith("https://"):
        response = urllib.request.urlopen(sys.argv[2])
        wordfile = response.read().decode("utf8").split("\n")

        wordfiletokens = wordfreq.tokenize(wordfile)
    
        stopfile = wordfreq.fileOpener(stopfilepath)
        counted = wordfreq.countWords(wordfiletokens, stopfile)
        wordfreq.printTopMost(counted, count)
        
    else:        
        stopfile = wordfreq.fileOpener(stopfilepath)
        wordfile = wordfreq.fileOpener(wordfilepath)
        counted = wordfreq.countWords(wordfile, stopfile)
        wordfreq.printTopMost(counted, count)


(_, stopfile, wordfile, count) = sys.argv


main(stopfile,wordfile, int(count))