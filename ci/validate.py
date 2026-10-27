from pathlib import Path
import json,base64,subprocess,tempfile
r=Path(__file__).resolve().parents[1]
allow={'.gitignore','README.md','DISTRIBUTION.md','distribution-policy.json','update.json','update-certificate.der','ci',' .github'.strip()}
for x in r.iterdir():
 if x.name=='.git':continue
 assert x.name in allow, 'Unexpected public root: '+x.name
for x in r.rglob('*'):
 if not x.is_file() or '.git' in x.parts:continue
 assert not x.name.endswith(('.java','.kt','.cpp','.h','.jks','.keystore','.apk','.jar','.ttf','.otf')), 'Unexpected implementation/secret/binary: '+str(x)
e=json.loads((r/'update.json').read_text());data=base64.b64decode(e['payload'],validate=True);signature=base64.b64decode(e['signature'],validate=True);assert len(data)<16384
with tempfile.TemporaryDirectory() as d:
 d=Path(d);(d/'payload').write_bytes(data);(d/'sig').write_bytes(signature)
 public=subprocess.check_output(['openssl','x509','-inform','DER','-in',str(r/'update-certificate.der'),'-pubkey','-noout']);(d/'key.pem').write_bytes(public)
 subprocess.run(['openssl','dgst','-sha256','-verify',str(d/'key.pem'),'-signature',str(d/'sig'),str(d/'payload')],check=True)
p=json.loads(data);assert p['schema']==1
policy=json.loads((r/'distribution-policy.json').read_text())
if policy['mode']=='hold':assert p['available'] is False,'A held distribution must not advertise an APK'
workflow=(r/'.github/workflows/build.yml').read_text();assert 'workflow_call:' in workflow and 'secrets.' not in workflow and 'private-source' in workflow
print('Public boundary, signed channel and secret-free reusable workflow verified; this check is not an Android compilation.')
