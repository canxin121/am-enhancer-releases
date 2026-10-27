from pathlib import Path
import os,sys,json,subprocess,base64,urllib.request
folder=Path(sys.argv[1]);channel=Path(__file__).resolve().parents[1];policy=json.loads((channel/'distribution-policy.json').read_text());publish=os.environ.get('PUBLISH_REQUESTED')=='true'
if publish:
 assert policy['mode']=='approved','Public release is held pending distribution rights'
 if policy['basis']=='corresponding-source':
  url=policy.get('correspondingSourceUrl','');assert url.startswith('https://')
  with urllib.request.urlopen(url,timeout=20) as response:assert response.status==200
 elif policy['basis']=='separate-license':assert policy.get('separateLicenseConfirmed') is True
 else:raise AssertionError('No verified distribution basis')
repo='canxin121/amhifi-releases';tag='v0.1.0';assets=[str(x) for x in folder.iterdir() if x.suffix in ('.apk','.json') or x.name=='SHA256SUMS']
probe=subprocess.run(['gh','release','view',tag,'--repo',repo,'--json','isDraft'],text=True,capture_output=True)
if probe.returncode:
 subprocess.run(['gh','release','create',tag,'--repo',repo,'--title','AM HiFi 0.1.0','--draft','--notes','Version pinned at 0.1.0. APK and metadata only; publication requires distribution approval.'],check=True)
else:
 assert json.loads(probe.stdout)['isDraft'] or publish,'Refusing to replace an already-public release during a draft-only build'
subprocess.run(['gh','release','upload',tag,'--repo',repo,'--clobber',*assets],check=True)
if publish:
 subprocess.run(['gh','release','edit',tag,'--repo',repo,'--draft=false'],check=True)
 existing=json.loads(subprocess.check_output(['gh','api','repos/'+repo+'/contents/update.json'],text=True))
 body={'message':'Update signed APK feed (version remains 0.1.0)','sha':existing['sha'],'content':base64.b64encode((folder/'update.json').read_bytes()).decode()}
 subprocess.run(['gh','api','repos/'+repo+'/contents/update.json','--method','PUT','--input','-'],input=json.dumps(body),text=True,check=True,stdout=subprocess.DEVNULL)
 print('Public APK and signed feed updated.')
else:print('Build attached to a maintainer-only draft. Public feed was not changed.')
