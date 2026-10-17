"""Metadata-only checkpoint finalization; filtered Git fetch, no full archive.

All gameplay blobs must remain identical to the independently restored base.
Only checkpoint helper and manifests/policy may change on the backup branch.
"""
import hashlib,json,os,subprocess,sys
from pathlib import Path
import map2l_isolated_checkpoint as old

ROOT=old.ROOT;GIT=old.GIT;ENV=old.ENV;BASE='0a66418cc3302704f14844d70608d9755d768dc1'
OUT=old.SESSION/'metadata_finish'
ALLOWED={'tools/map2l_isolated_checkpoint.py','docs/backups/CURRENT_CHECKPOINT_MANIFEST.json','docs/backups/BACKUP_POLICY.md','_checkpoint/MAP2L_RHINE_SWABIA_MANIFEST.json'}

def git(repo,*args,data=None):return subprocess.check_output([GIT,'--git-dir='+str(repo),*args],input=data,env=ENV)
def dump(name,value):OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def tree(repo,commit):
    return {name.decode():(mode.decode(),oid.decode()) for row in git(repo,'ls-tree','-rz',commit).split(b'\0') if row for meta,name in [row.split(b'\t',1)] for mode,kind,oid in [meta.split()]}
def init(repo):
    if not repo.exists():subprocess.check_call([GIT,'init','--bare',str(repo)],env=ENV)
    git(repo,'config','remote.origin.url',old.REMOTE);git(repo,'config','remote.origin.promisor','true');git(repo,'config','remote.origin.partialclonefilter','blob:none')
    git(repo,'fetch','--filter=blob:none','--depth=2','origin','refs/heads/'+old.BRANCH)

def restore_changed(repo,commit,label):
    entries=tree(repo,commit);expected=json.loads((OUT/'EXPECTED.json').read_text());target=OUT/('restore_'+label)
    for name,row in expected.items():
        assert entries[name][1]==row['oid'];raw=git(repo,'cat-file','blob',row['oid'])
        assert hashlib.sha256(raw).hexdigest()==row['sha256']
        path=target/name;assert path.resolve().is_relative_to(target.resolve());path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw);assert old.sha(path)==row['sha256']
    return len(expected)

def prepare():
    old.guard();assert json.loads((old.SESSION/'VERIFIED.json').read_text())['status']=='PASS_REMOTE_EXACT_RESTORATION'
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'PREPARED.json').exists()
    refs=old.remote_refs();assert refs['refs/heads/'+old.BRANCH]==BASE;dump('REMOTE_BEFORE.json',refs)
    repo=OUT/'metadata.git';init(repo);assert git(repo,'rev-parse','FETCH_HEAD').decode().strip()==BASE
    original=tree(repo,BASE);git(repo,'read-tree',BASE)
    helper='tools/map2l_isolated_checkpoint.py';raw=(ROOT/helper).read_bytes();oid=git(repo,'hash-object','-w','--stdin',data=raw).decode().strip()
    manifest=json.loads((old.SESSION/'MANIFEST.json').read_text());row=next(r for r in manifest['files'] if r['path']==helper);row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),git_blob=oid)
    manifest.update(parent=BASE,source_bytes=sum(r['bytes'] for r in manifest['files']),metadata_finalization='Only checkpoint helper, current manifest and policy updated; gameplay identical to independently restored 0a66418',base_complete_remote_verification='RESTORE_remote.json: 6726 blob SHA256 checks; 213 files materialized',delta_files=1,delta_bytes=len(raw))
    encoded=json.dumps(manifest,ensure_ascii=False,indent=2).encode();policy=git(repo,'show',BASE+':docs/backups/BACKUP_POLICY.md')+b'\n## MAP-2L Rhine-Westphalia and Swabia user-validated checkpoint\n\nCURRENT_CHECKPOINT_MANIFEST.json now contains the current full source manifest and matches _checkpoint/MAP2L_RHINE_SWABIA_MANIFEST.json. The backup metadata files do not hash themselves. Gameplay is identical to the independently restored 0a66418 snapshot. Only metadata and the checkpoint-helper safety checks changed afterward. The later Swabia continuation is deliberately not included. Restore sources using this manifest; never overwrite the development workspace.\n'
    updates={helper:raw,'docs/backups/CURRENT_CHECKPOINT_MANIFEST.json':encoded,'_checkpoint/MAP2L_RHINE_SWABIA_MANIFEST.json':encoded,'docs/backups/BACKUP_POLICY.md':policy};expected={}
    for name,content in updates.items():
        oid=git(repo,'hash-object','-w','--stdin',data=content).decode().strip();git(repo,'update-index','--cacheinfo','100644,'+oid+','+name)
        expected[name]=dict(oid=oid,sha256=hashlib.sha256(content).hexdigest(),bytes=len(content))
    newtree=git(repo,'write-tree','--missing-ok').decode().strip();commit=git(repo,'-c','user.name=MAP-2L Checkpoint','-c','user.email=checkpoint@local.invalid','commit-tree',newtree,'-p',BASE,data=b'MAP-2L checkpoint: current manifests and exact-commit restoration guard\n').decode().strip()
    latest=tree(repo,commit);assert set(latest)==set(original) and {n for n in latest if latest[n]!=original[n]}==ALLOWED
    assert all(latest[n]==original[n] for n in original if n not in ALLOWED),'Gameplay or research changed'
    dump('EXPECTED.json',expected);checked=restore_changed(repo,commit,'local');git(repo,'update-ref','refs/heads/'+old.BRANCH,commit)
    dump('PREPARED.json',dict(commit=commit,parent=BASE,changed_files=sorted(ALLOWED),all_other_blob_ids_unchanged=True,local_delta_restoration=checked,main_unchanged=True));old.guard();print('PREPARED_METADATA_ONLY',commit,checked,flush=True)

def publish():
    old.guard();p=json.loads((OUT/'PREPARED.json').read_text());assert p['local_delta_restoration']==4
    assert old.remote_refs()==json.loads((OUT/'REMOTE_BEFORE.json').read_text())
    git(OUT/'metadata.git','push',old.REMOTE,'refs/heads/'+old.BRANCH+':refs/heads/'+old.BRANCH)
    refs=old.remote_refs();assert refs['refs/heads/'+old.BRANCH]==p['commit'];assert refs['refs/heads/main']==json.loads((OUT/'REMOTE_BEFORE.json').read_text())['refs/heads/main'];dump('REMOTE_AFTER.json',refs);old.guard();print('PUBLISHED_METADATA_ONLY',p['commit'],flush=True)

def verify():
    old.guard();p=json.loads((OUT/'PREPARED.json').read_text());repo=OUT/'remote.git';init(repo);assert git(repo,'rev-parse','FETCH_HEAD').decode().strip()==p['commit']
    entries=tree(repo,p['commit']);original=tree(repo,BASE);assert set(entries)==set(original) and {n for n in entries if entries[n]!=original[n]}==ALLOWED
    restored=restore_changed(repo,p['commit'],'remote')
    refs=old.remote_refs();assert refs['refs/heads/'+old.BRANCH]==p['commit'] and refs['refs/heads/main']==json.loads((OUT/'REMOTE_BEFORE.json').read_text())['refs/heads/main']
    result=dict(status='PASS_REMOTE_INCREMENTAL_RESTORATION',commit=p['commit'],parent=BASE,branch=old.BRANCH,remote_tree_files=len(entries),changed_files=sorted(ALLOWED),changed_blob_sha256_verified=restored,changed_files_materialized=restored,all_other_blob_ids_unchanged=True,base_complete_sha256_verification_files=6726,workspace_head_index_unchanged=True,main_unchanged=True,swabia_continuation_included=False,no_full_archive_created=True)
    dump('VERIFIED.json',result);old.guard();print(json.dumps(result),flush=True)

if __name__=='__main__':{'prepare':prepare,'publish':publish,'verify':verify}[sys.argv[1]]()
