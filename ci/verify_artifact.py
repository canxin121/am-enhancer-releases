from pathlib import Path
import os,sys,re,json,hashlib,zipfile,struct,subprocess,shutil
source=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();log=Path(sys.argv[3]).read_text();out.mkdir(parents=True,exist_ok=True)
apk=source/'dist/applemusic-usb-hifi-0.1.0-unsigned.apk';bt=Path(os.environ['ANDROID_SDK_ROOT'])/'build-tools/34.0.0'
def run(*args):return subprocess.check_output([str(x) for x in args],text=True,stderr=subprocess.STDOUT)
badging=run(bt/'aapt','dump','badging',apk)
assert "package: name='org.research.amhifi'" in badging and "versionCode='4008'" in badging and "versionName='0.1.0'" in badging
assert 'launchable-activity:' not in badging,'Standalone launcher unexpectedly restored'
run(bt/'zipalign','-c','16384',apk)
info={'versionName':'0.1.0','versionCode':4008,'sourceCommit':os.environ['SOURCE_COMMIT'],'pipelineCommit':os.environ['PIPELINE_COMMIT'],'runId':os.environ['GITHUB_RUN_ID'],'runUrl':'https://github.com/'+os.environ['GITHUB_REPOSITORY']+'/actions/runs/'+os.environ['GITHUB_RUN_ID'],'signed':False,'requiresLocalOriginalSignature':True,'sourceIncluded':False,'native':{},'tests':{}}
with apk.open('rb') as raw,zipfile.ZipFile(apk) as z:
 assert z.testzip() is None
 assert z.read('assets/xposed_init').strip()==b'org.research.amhifi.HookEntry'
 assert not any('pcm_probe' in name or 'classes.jar' in name or name.endswith(('.jks','.keystore','.java','.cpp')) for name in z.namelist())
 build=json.loads(z.read('assets/build-info.json'));assert build['versionName']=='0.1.0' and build['versionCode']==4008 and build['sourceCommit']==info['sourceCommit']
 info['buildId']=build['buildId'];info['buildEpoch']=build['buildEpoch']
 for abi,machine in [('arm64-v8a',183),('armeabi-v7a',40),('x86_64',62)]:
  entry=z.getinfo('lib/'+abi+'/libamhifi_usb.so');data=z.read(entry);assert entry.compress_type==zipfile.ZIP_STORED
  raw.seek(entry.header_offset);h=raw.read(30);a,b=struct.unpack_from('<HH',h,26);assert (entry.header_offset+30+a+b)%16384==0
  assert struct.unpack_from('<H',data,18)[0]==machine
  is64=data[4]==2;offset=struct.unpack_from('<Q' if is64 else '<I',data,32 if is64 else 28)[0];size,count=struct.unpack_from('<HH',data,54 if is64 else 42)
  for n in range(count):
   at=offset+n*size
   if struct.unpack_from('<I',data,at)[0]==1:assert struct.unpack_from('<Q' if is64 else '<I',data,at+(48 if is64 else 28))[0]>=16384
  info['native'][abi]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'alignment16k':True}
 assert len([n for n in z.namelist() if n.startswith('lib/') and n.endswith('.so')])==3
for name,pattern in [('javaPlayback',r'AMHiFi core: (\d+) assertions passed'),('gainClockFlush',r'Playback gain/clock/flush: (\d+) assertions passed'),('usbVolume',r'USB user volume: (\d+) assertions passed'),('logPrivacy',r'Log privacy: (\d+) assertions passed'),('versionPolicy',r'Compatibility policy: (\d+) assertions passed'),('faultLatch',r'First-fault latch: (\d+) assertions passed')]:
 m=re.search(pattern,log);assert m,'Missing test result '+name;info['tests'][name]=int(m.group(1))
assert '100% tests passed, 0 tests failed out of 2' in log;info['tests']['nativeTargets']=2
name='AMHiFi-0.1.0-'+info['sourceCommit'][:12]+'-unsigned.apk';target=out/name;shutil.copyfile(apk,target);info['apkFile']=name;info['sha256']=hashlib.sha256(target.read_bytes()).hexdigest();info['bytes']=target.stat().st_size
(out/'BUILD.json').write_text(json.dumps(info,indent=2)+'\n');(out/'SHA256SUMS').write_text(info['sha256']+'  '+name+'\n')
(out/'README.txt').write_text('GitHub Actions compiled artifact. Unsigned; do not install as an update. Sign locally using the original module key. No source or credentials included. Version stays 0.1.0 / 4008.\n')
print(json.dumps(info,indent=2))
summary=os.environ.get('GITHUB_STEP_SUMMARY')
if summary:
 with open(summary,'a') as f:f.write('## AM HiFi build verified\n\nVersion: **0.1.0 / 4008**\n\nABIs: arm64-v8a, armeabi-v7a, x86_64. Java/native tests passed.\n\nUnsigned APK SHA-256: `'+info['sha256']+'`\n\nArtifact contains APK, verification receipt and checksums only. Signing key stays off GitHub. No source archive uploaded.\n')
