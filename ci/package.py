from pathlib import Path
import sys,os,subprocess,json,hashlib,zipfile
source=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
apk=source/'dist/applemusic-usb-hifi-0.1.0.apk';sdk=Path(os.environ['ANDROID_SDK_ROOT'])/'build-tools/34.0.0'
cert=subprocess.check_output([str(sdk/'apksigner'),'verify','--print-certs',str(apk)],text=True)
expected='e2cacbdede8e2c75899f132ca7232f1d38e86258cdc1a4121f0e7a5a399743c5'
assert 'certificate SHA-256 digest: '+expected in cert,'Original signing identity is required'
with zipfile.ZipFile(apk) as z:build=json.loads(z.read('assets/build-info.json'))
assert build['versionName']=='0.1.0' and build['versionCode']==4008
name='AMHiFi-0.1.0-'+build['buildId'][:12]+'.apk';data=apk.read_bytes();(out/name).write_bytes(data)
manifest={'schema':1,'available':True,'package':'org.research.amhifi','versionName':'0.1.0','versionCode':4008,'buildId':build['buildId'],'buildEpoch':build['buildEpoch'],'sha256':hashlib.sha256(data).hexdigest(),'size':len(data),'minApi':30,'abis':['arm64-v8a','armeabi-v7a','x86_64'],'url':'https://github.com/canxin121/amhifi-releases/releases/download/v0.1.0/'+name,'notes':'稳定性与体验修复。安装后重启手机生效。'}
(out/'payload.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':')))
subprocess.run(['java',str(source/'tools/SignUpdate.java'),str(source/'signing/lab-development.jks'),'hifi-lab',str(out/'payload.json'),str(out/'update.json')],check=True,stdout=subprocess.DEVNULL)
(out/'SHA256SUMS').write_text(manifest['sha256']+'  '+name+'\n')
(out/'build.json').write_text(json.dumps({'sourceCommit':os.environ['SOURCE_COMMIT'],'buildId':build['buildId'],'version':'0.1.0','apkSha256':manifest['sha256']},indent=2)+'\n')
(out/'payload.json').unlink()
print('Verified APK and signed metadata prepared. No source artifact was generated.')
