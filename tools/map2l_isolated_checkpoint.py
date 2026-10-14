"""Incremental backup branch snapshot; never writes the principal Git index/HEAD.

Raw blobs bypass filters. Restoration hashes every blob and materializes only
the changed/new files, avoiding a second full working-tree/archive on disk.
"""
import hashlib,json,os,re,subprocess,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GIT='C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
SESSION=Path('C:/Users/simeo/.codex/visualizations/2026/09/08/01a080b1-616e-71b2-85c3-0d7759724725/checkpoint_map2l_rhine_swabia_incremental')
OLD_PLAN=SESSION.parent/'checkpoint_map2l_user_validated_2026_10_14/SOURCE_PLAN.json'
REMOTE='https://github.com/Malzars-sys/1776-Age-of-Revolutions.git'
BRANCH='backup/1776-checkpoints'
EXPECTED_PARENT='d7f05ce71ef40df96e3a53e1ccf4ebaf65b9b941'
ENV={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'}

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def git(*args,repo=None,data=None):
    prefix=[GIT]+(['--git-dir='+str(repo)] if repo else ['-C',str(ROOT)])
    return subprocess.check_output(prefix+list(args),input=data,env=ENV)

def dump(name,value):
    SESSION.mkdir(parents=True,exist_ok=True)
    (SESSION/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def guard():
    state=json.loads((SESSION/'WORKSPACE_GUARD.json').read_text())
    assert git('rev-parse','HEAD').decode().strip()==state['head'],'Workspace HEAD changed'
    assert sha(ROOT/'.git/index')==state['index_sha256'],'Workspace index changed'
    return state

def remote_refs():
    return dict((line.split()[1],line.split()[0]) for line in git('ls-remote',REMOTE,'refs/heads/main','refs/heads/'+BRANCH).decode().splitlines())

def prepare():
    assert not (SESSION/'PREPARED.json').exists(),'Do not overwrite a prepared snapshot'
    SESSION.mkdir(parents=True,exist_ok=True)
    before=dict(head=git('rev-parse','HEAD').decode().strip(),index_sha256=sha(ROOT/'.git/index'))
    dump('WORKSPACE_GUARD.json',before)
    old=json.loads(OLD_PLAN.read_text(encoding='utf-8'))
    forbidden={r['path']:r.get('reason','prior exclusion') for r in old['excluded']}
    names={r['path'] for r in old['files']}
    names.update(git('ls-files','-z','--cached','--others','--exclude-standard').decode().split('\0'))
    names.discard('')
    blocked_dirs={'.git','.asset-cache','.colgrep','.venv','node_modules','__pycache__','.codex','.agents'}
    files=[];excluded=[]
    secret=re.compile(rb'(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|sk-proj-[A-Za-z0-9_-]{40,})')
    for name in sorted(names):
        path=ROOT/name;parts=Path(name).parts
        if name in forbidden or any(p in blocked_dirs for p in parts) or path.suffix.lower() in {'.pyc','.log','.tmp','.v3'} or path.name.lower() in {'.env','credentials','id_rsa','id_ed25519'}:
            excluded.append(dict(path=name,reason=forbidden.get(name,'cache/save/secret filename')));continue
        if not path.is_file():
            excluded.append(dict(path=name,reason='Absent from current source; retained remote historical snapshot'));continue
        assert not path.is_symlink(),name
        size=path.stat().st_size
        assert size<100_000_000,('Oversized blob',name,size)
        if path.suffix.lower() in {'.txt','.json','.md','.py','.js','.yml','.toml','.ps1'} and size<12_000_000:
            assert not secret.search(path.read_bytes()),('Potential secret; publication blocked',name)
        files.append(dict(path=name,bytes=size,sha256=sha(path)))
    refs=remote_refs();assert refs['refs/heads/'+BRANCH]==EXPECTED_PARENT,refs
    dump('REMOTE_BEFORE.json',refs)
    repo=SESSION/'snapshot.git'
    if not repo.exists():git('init','--bare',str(repo))
    git('fetch','--depth=1',REMOTE,'refs/heads/'+BRANCH,repo=repo)
    assert git('rev-parse','FETCH_HEAD',repo=repo).decode().strip()==EXPECTED_PARENT
    oldtree={}
    for item in git('ls-tree','-rz',EXPECTED_PARENT,repo=repo).split(b'\0'):
        if not item:continue
        meta,name=item.split(b'\t',1);mode,kind,oid=meta.decode().split();assert kind=='blob'
        oldtree[name.decode()]=(mode,oid)
    git('read-tree',EXPECTED_PARENT,repo=repo)
    previous={r['path']:r for r in old['files']};delta=[];updates=[]
    for row in files:
        name=row['path'];path=ROOT/name
        if name in oldtree and previous.get(name,{}).get('sha256')==row['sha256']:
            mode,oid=oldtree[name]
        else:
            oid=git('hash-object','--no-filters','-w',str(path),repo=repo).decode().strip();mode=oldtree.get(name,('100644',''))[0]
            delta.append(row)
        row['git_blob']=oid;updates.append(f'{mode} {oid}\t{name}\0'.encode())
    manifest=dict(branch=BRANCH,parent=EXPECTED_PARENT,files=files,excluded=excluded,source_bytes=sum(r['bytes'] for r in files),delta_files=len(delta),delta_bytes=sum(r['bytes'] for r in delta),workspace_guard=before,hash_policy='Raw SHA256 bytes; no Git filters',restore_policy='All snapshot blobs streamed and SHA256 checked; delta restored to disk',historical_boundary_certification=False,automated_engine_testing=False)
    dump('MANIFEST.json',manifest)
    oid=git('hash-object','--no-filters','-w',str(SESSION/'MANIFEST.json'),repo=repo).decode().strip()
    updates.append(f'100644 {oid}\t_checkpoint/MAP2L_RHINE_SWABIA_MANIFEST.json\0'.encode())
    git('update-index','-z','--index-info',repo=repo,data=b''.join(updates))
    tree=git('write-tree',repo=repo).decode().strip()
    commit=git('-c','user.name=MAP-2L Checkpoint','-c','user.email=checkpoint@local.invalid','commit-tree',tree,'-p',EXPECTED_PARENT,repo=repo,data=b'MAP-2L: user-validated Rhine-Westphalia and Swabia, localization repairs\n').decode().strip()
    git('update-ref','refs/heads/'+BRANCH,commit,repo=repo)
    dump('PREPARED.json',dict(commit=commit,tree=tree,parent=EXPECTED_PARENT,delta=delta,files=len(files),bytes=manifest['source_bytes']))
    guard()
    print(json.dumps(dict(stage='PREPARED',commit=commit,files=len(files),delta_files=len(delta),delta_bytes=manifest['delta_bytes'])),flush=True)

def refresh_self():
    """Fix checkpoint-helper bytes in the unpublished snapshot, without refetch."""
    guard();assert not (SESSION/'REMOTE_AFTER.json').exists()
    repo=SESSION/'snapshot.git';manifest=json.loads((SESSION/'MANIFEST.json').read_text());prepared=json.loads((SESSION/'PREPARED.json').read_text())
    name=Path(__file__).relative_to(ROOT).as_posix()
    for row in manifest['files']:
        if row['path']!=name:assert sha(ROOT/row['path'])==row['sha256']
        else:
            row.update(bytes=(ROOT/name).stat().st_size,sha256=sha(ROOT/name),git_blob=git('hash-object','--no-filters','-w',str(ROOT/name),repo=repo).decode().strip())
            prepared['delta']=[r for r in prepared['delta'] if r['path']!=name]+[row]
            git('update-index','--cacheinfo','100644,'+row['git_blob']+','+name,repo=repo)
    manifest.update(source_bytes=sum(r['bytes'] for r in manifest['files']),delta_bytes=sum(r['bytes'] for r in prepared['delta']),delta_files=len(prepared['delta']))
    dump('MANIFEST.json',manifest)
    oid=git('hash-object','--no-filters','-w',str(SESSION/'MANIFEST.json'),repo=repo).decode().strip()
    git('update-index','--cacheinfo','100644,'+oid+',_checkpoint/MAP2L_RHINE_SWABIA_MANIFEST.json',repo=repo)
    tree=git('write-tree',repo=repo).decode().strip();commit=git('-c','user.name=MAP-2L Checkpoint','-c','user.email=checkpoint@local.invalid','commit-tree',tree,'-p',EXPECTED_PARENT,repo=repo,data=b'MAP-2L: user-validated Rhine-Westphalia and Swabia, localization repairs\n').decode().strip()
    git('update-ref','refs/heads/'+BRANCH,commit,prepared['commit'],repo=repo)
    prepared.update(commit=commit,tree=tree,bytes=manifest['source_bytes']);dump('PREPARED.json',prepared)
    print('Unpublished helper corrected:',commit,flush=True)

def restore(repo,label,materialize=True):
    prepared=json.loads((SESSION/'PREPARED.json').read_text());manifest=json.loads((SESSION/'MANIFEST.json').read_text())
    expected={r['path']:r for r in manifest['files']};delta={r['path'] for r in prepared['delta']}
    entries=[]
    for item in git('ls-tree','-rz',prepared['commit'],repo=repo).split(b'\0'):
        if item:
            meta,name=item.split(b'\t',1);mode,kind,oid=meta.decode().split();assert kind=='blob';entries.append((name.decode(),oid))
    proc=subprocess.Popen([GIT,'--git-dir='+str(repo),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,env=ENV)
    assert {name for name,_ in entries}==set(expected)|{'_checkpoint/MAP2L_RHINE_SWABIA_MANIFEST.json'},'Unexpected or missing snapshot files'
    checked=0;written=0;total=0
    for name,oid in entries:
        if name not in expected:continue
        row=expected[name];assert oid==row['git_blob']
        proc.stdin.write((oid+'\n').encode());proc.stdin.flush()
        header=proc.stdout.readline().decode().split();assert header[1]=='blob';remaining=int(header[2]);assert remaining==row['bytes']
        h=hashlib.sha256();stream=None
        if materialize and name in delta:
            target=SESSION/('restore_'+label)/name
            assert target.resolve().is_relative_to((SESSION/('restore_'+label)).resolve())
            target.parent.mkdir(parents=True,exist_ok=True);stream=target.open('wb')
        try:
            while remaining:
                chunk=proc.stdout.read(min(remaining,1024*1024));assert chunk
                h.update(chunk);remaining-=len(chunk);total+=len(chunk)
                if stream:stream.write(chunk)
        finally:
            if stream:stream.close()
        assert proc.stdout.read(1)==b'\n'
        assert h.hexdigest()==row['sha256'],('Restore SHA256 mismatch',name)
        if stream:assert sha(target)==row['sha256'];written+=1
        checked+=1
        if checked%1000==0:print(label,'verified',checked,flush=True)
    proc.stdin.close();assert proc.wait()==0
    assert checked==len(expected)
    git('fsck','--full','--no-reflogs',repo=repo)
    result=dict(status='PASS_ALL_BLOB_SHA256_AND_DELTA_RESTORATION',checked=checked,bytes=total,materialized_delta_files=written,commit=prepared['commit'])
    dump('RESTORE_'+label+'.json',result);guard();print(json.dumps(result),flush=True)

def publish():
    guard();prepared=json.loads((SESSION/'PREPARED.json').read_text())
    assert json.loads((SESSION/'RESTORE_local.json').read_text())['status'].startswith('PASS')
    refs=remote_refs();old=json.loads((SESSION/'REMOTE_BEFORE.json').read_text());assert refs==old,'Remote changed; do not overwrite'
    for r in json.loads((SESSION/'MANIFEST.json').read_text())['files']:assert sha(ROOT/r['path'])==r['sha256'],('Source changed since snapshot',r['path'])
    git('push',REMOTE,'refs/heads/'+BRANCH+':refs/heads/'+BRANCH,repo=SESSION/'snapshot.git')
    refs=remote_refs();assert refs['refs/heads/'+BRANCH]==prepared['commit'];assert refs['refs/heads/main']==old['refs/heads/main']
    dump('REMOTE_AFTER.json',refs);guard();print('PUBLISHED',prepared['commit'],flush=True)

def verify_remote():
    guard();prepared=json.loads((SESSION/'PREPARED.json').read_text())
    repo=SESSION/'remote_verify.git'
    if not repo.exists():git('init','--bare',str(repo))
    git('fetch','--depth=1',REMOTE,'refs/heads/'+BRANCH,repo=repo)
    assert git('rev-parse','FETCH_HEAD',repo=repo).decode().strip()==prepared['commit']
    restore(repo,'remote',True)
    refs=remote_refs();old=json.loads((SESSION/'REMOTE_BEFORE.json').read_text());assert refs['refs/heads/main']==old['refs/heads/main'];assert refs['refs/heads/'+BRANCH]==prepared['commit']
    dump('VERIFIED.json',dict(status='PASS_REMOTE_EXACT_RESTORATION',commit=prepared['commit'],branch=BRANCH,main_unchanged=True,workspace_head_index_unchanged=True,delta_only_disk_restoration=True,no_full_archive_created=True))

if __name__=='__main__':
    {'prepare':prepare,'refresh-self':refresh_self,'restore':lambda:restore(SESSION/'snapshot.git','local'), 'publish':publish,'verify-remote':verify_remote}[sys.argv[1]]()
