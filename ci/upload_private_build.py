from pathlib import Path
import os,sys,json,zipfile,hashlib,subprocess
repo=os.environ['GITHUB_REPOSITORY'];assert repo=='canxin121/am-enhancer','Delivery must remain in caller-private repository'
metadata=json.loads(subprocess.check_output(['gh','api','repos/'+repo],text=True));assert metadata['private'] is True,'Refusing to expose build artifacts'
folder=Path(sys.argv[1]);build=json.loads((folder/'BUILD.json').read_text());assert build['signed'] is False and build['sourceIncluded'] is False
assert build['runId']==os.environ['GITHUB_RUN_ID']
expected={build['apkFile'],'BUILD.json','SHA256SUMS','README.txt'};assert {p.name for p in folder.iterdir()}==expected,'Only verified deliverables may be uploaded'
apk=folder/build['apkFile'];assert hashlib.sha256(apk.read_bytes()).hexdigest()==build['sha256']
run=os.environ['GITHUB_RUN_ID'];attempt=os.environ.get('GITHUB_RUN_ATTEMPT','1');name='AM-Enhancer-0.1.0-'+build['sourceCommit'][:12]+'-run'+run+'-attempt'+attempt+'-unsigned.zip'
archive=folder.parent/name
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(folder.iterdir()):z.write(p,p.name)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None and set(z.namelist())==expected
subprocess.run(['gh','release','view','v0.1.0','--repo',repo],check=True,stdout=subprocess.DEVNULL)
# A unique run/attempt name avoids touching the previous installable APK or moving a tag.
subprocess.run(['gh','release','upload','v0.1.0','--repo',repo,str(archive)],check=True)
sha=hashlib.sha256(archive.read_bytes()).hexdigest();url='https://github.com/'+repo+'/releases/download/v0.1.0/'+name
record={'archive':name,'archiveSha256':sha,'privateRelease':'v0.1.0','url':url,'noExistingAssetReplaced':True,'applicationVersionUnchanged':True}
print(json.dumps(record,indent=2))
with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as f:f.write('\n## Download\n\n[Verified private build package]('+url+')\n\nZIP SHA-256: `'+sha+'`\n\nStored on the existing private v0.1.0 Release; no old artifacts deleted. APK is unsigned and must use the original local signing key.\n')
