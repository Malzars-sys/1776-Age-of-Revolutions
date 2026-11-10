"""Prepare a file-by-file integration review without writing Git or live files.

Rebuilds PR text blobs from a preserved diff and local common-ancestor objects.
Every reconstructed blob is checked against the Git object ID in the diff.
git show and git merge-file --stdout are read-only; output goes to evidence only.
"""
from pathlib import Path, PurePosixPath
import argparse
import collections
import hashlib
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, env=ENV, capture_output=True)


def blob_id(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def normalize(raw):
    return None if raw is None else raw.replace(b'\r\n', b'\n')


def commit_file(commit, path):
    result = git('show', f'{commit}:{path}')
    if result.returncode == 0:
        return result.stdout
    if b'does not exist' in result.stderr or b'exists on disk, but not in' in result.stderr:
        return None
    raise RuntimeError(result.stderr.decode(errors='replace'))


def reconstruct(base, patch):
    index = re.search(r'^index ([0-9a-f]+)\.\.([0-9a-f]+)', patch, re.M)
    if not index:
        raise ValueError('Missing object IDs in text diff')
    old_id, new_id = index.groups()
    if base is not None and not blob_id(base).startswith(old_id):
        raise ValueError('Common-ancestor blob does not match the PR index')
    deleted = '\n+++ /dev/null\n' in patch
    lines = normalize(base or b'').splitlines(keepends=True)
    parts = patch.splitlines(keepends=True)
    position, output = 0, []
    number = 0
    while number < len(parts):
        header = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', parts[number])
        if not header:
            number += 1
            continue
        old_start = int(header[1]) - 1 if int(header[1]) else 0
        if old_start < position:
            raise ValueError('Overlapping hunks')
        output.extend(lines[position:old_start])
        position = old_start
        number += 1
        hunk = []
        while number < len(parts) and not parts[number].startswith('@@ '):
            line = parts[number]
            if line.startswith('\\ No newline at end of file'):
                if hunk:
                    sign, value = hunk[-1]
                    hunk[-1] = (sign, value.rstrip(b'\n'))
            elif line[:1] in (' ', '+', '-'):
                hunk.append((line[0], line[1:].encode('utf-8')))
            else:
                break
            number += 1
        old_count, new_count = 0, 0
        for sign, value in hunk:
            if sign in (' ', '-'):
                if position >= len(lines) or lines[position] != value:
                    raise ValueError(f'Hunk context mismatch at old line {position + 1}')
                position += 1
                old_count += 1
            if sign in (' ', '+'):
                output.append(value)
                new_count += 1
        if old_count != int(header[2] or 1) or new_count != int(header[4] or 1):
            raise ValueError('Hunk line counts differ')
    output.extend(lines[position:])
    remote = None if deleted else b''.join(output)
    if remote is not None and not blob_id(remote).startswith(new_id):
        raise ValueError(f'Reconstructed head blob mismatch: {blob_id(remote)} vs {new_id}')
    return remote


def write_version(evidence, kind, path, raw):
    if raw is None:
        return
    target = evidence / 'versions' / kind / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        prior = target.read_bytes()
        if prior == raw:
            return
        archive = evidence / 'history' / hashlib.sha256(prior).hexdigest()
        archive.parent.mkdir(exist_ok=True)
        if not archive.exists():
            archive.write_bytes(prior)
    target.write_bytes(raw)


def save_result(evidence, name, value):
    target = evidence / name
    raw = (json.dumps(value, indent=2) + '\n').encode('utf-8')
    if target.exists() and target.read_bytes() != raw:
        prior = target.read_bytes()
        archive = evidence / 'history' / hashlib.sha256(prior).hexdigest()
        archive.parent.mkdir(exist_ok=True)
        if not archive.exists():
            archive.write_bytes(prior)
    target.write_bytes(raw)


def reconcile(evidence, side, path, current, base, remote, main_file, resolutions):
    """Resolve only proven cases; an explicit resolution is tied to exact bytes."""
    if normalize(current) == normalize(remote):
        return 'ALREADY_PRESENT', current
    if normalize(main_file) == normalize(remote):
        return 'REMOTE_ALREADY_IN_MAIN_KEEP_' + side.upper(), current
    if normalize(remote) == normalize(base):
        return 'REMOTE_UNCHANGED_KEEP_' + side.upper(), current
    if path in resolutions:
        resolution = resolutions[path]
        expected = resolution['expected_' + side + '_sha256']
        actual = hashlib.sha256(current).hexdigest() if current is not None else None
        if actual != expected:
            raise ValueError('Explicit resolution is stale for ' + side + ': ' + path)
        if resolution['action'] != 'keep_current':
            raise ValueError('Unsupported resolution action')
        return 'EXPLICIT_REVIEW_KEEP_' + side.upper(), current
    if normalize(current) == normalize(base):
        return 'ADOPT_REMOTE_ONLY_CHANGE', remote
    if path.startswith('docs/'):
        return 'KEEP_' + side.upper() + '_EVIDENCE_REMOTE_ARCHIVED', current
    if current is None or remote is None:
        return 'MODIFY_DELETE_REVIEW_REQUIRED', None
    temp = evidence / 'merge_inputs_v2' / side
    temp.mkdir(parents=True, exist_ok=True)
    for name, raw in [('current', current), ('base', base or b''), ('hotfix', remote)]:
        (temp / name).write_bytes(normalize(raw))
    merged = git('merge-file', '--stdout', '--diff3', '-L', side.upper(), '-L', 'COMMON_BASE', '-L', 'HOTFIX',
                 str(temp / 'current'), str(temp / 'base'), str(temp / 'hotfix'))
    if merged.returncode == 0:
        # Preserve original EOLs when the content has not changed.
        return 'CLEAN_THREE_WAY_MERGE', current if normalize(merged.stdout) == normalize(current) else merged.stdout
    if merged.returncode < 0 or merged.returncode > 127:
        raise RuntimeError('git merge-file failed: ' + merged.stderr.decode(errors='replace'))
    conflict = evidence / 'conflicts' / side / path
    conflict.parent.mkdir(parents=True, exist_ok=True)
    conflict.write_bytes(merged.stdout)
    return 'CONFLICT_REVIEW_REQUIRED', None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    if not evidence.is_relative_to(ROOT / 'docs/reports/compatibility'):
        parser.error('Output must stay inside repository compatibility reports.')
    source = json.loads((evidence / 'INPUT_METADATA.json').read_text(encoding='utf-8'))
    blob_file = evidence / 'REMOTE_BLOBS.json'
    supplied_blobs = json.loads(blob_file.read_text(encoding='utf-8')) if blob_file.exists() else {}
    resolution_file = evidence / 'RESOLUTIONS.json'
    resolutions = json.loads(resolution_file.read_text(encoding='utf-8'))['files'] if resolution_file.exists() else {}
    diff = (evidence / 'PR34_REMOTE.diff').read_bytes().decode('utf-8')
    blocks = {}
    for block in re.split(r'(?=^diff --git )', diff, flags=re.M):
        match = re.match(r'diff --git a/(.+) b/(.+)\n', block)
        if match:
            assert match[1] == match[2], 'Renames require explicit review'
            blocks[match[2]] = block
    assert set(blocks) == set(source['paths']), 'Diff and validated PR path list differ'
    index_path = ROOT / '.git/index'
    index_before = hashlib.sha256(index_path.read_bytes()).hexdigest()
    rows, failures, source_hashes = [], [], {}
    for count, path in enumerate(source['paths'], 1):
        clean = PurePosixPath(path)
        assert not clean.is_absolute() and '..' not in clean.parts and '.git' not in clean.parts
        base = commit_file(source['base_sha'], path)
        main_file = commit_file(source['main_sha'], path)
        active = ROOT / path
        current = active.read_bytes() if active.is_file() else None
        source_hashes[path] = hashlib.sha256(current).hexdigest() if current is not None else None
        try:
            remote = reconstruct(base, blocks[path])
        except ValueError as error:
            if path not in supplied_blobs:
                failures.append({'path': path, 'error': str(error)})
                continue
            expected = re.search(r'^index [0-9a-f]+\.\.([0-9a-f]+)', blocks[path], re.M)[1]
            raw = supplied_blobs[path]['text'].encode('utf-8')
            matches = [data for data in [raw, b'\xef\xbb\xbf' + raw] if blob_id(data).startswith(expected)]
            if len(matches) != 1:
                failures.append({'path': path, 'error': 'Supplied blob does not match the pinned PR object'})
                continue
            remote = matches[0]
        for kind, raw in [('base', base), ('main', main_file), ('workspace', current), ('hotfix', remote)]:
            write_version(evidence, kind, path, raw)
        row = {'path': path, 'functional': path.startswith(('common/', 'events/', 'localization/', 'map_data/')),
               'remote_blob': blob_id(remote) if remote is not None else None,
               'main_equals_hotfix': normalize(main_file) == normalize(remote),
               'workspace_equals_hotfix': normalize(current) == normalize(remote),
               'workspace_equals_main': normalize(current) == normalize(main_file),
               'source_sha256': source_hashes[path]}
        for side, data, kind, prefix in [('workspace', current, 'proposed', 'proposed'),
                                         ('main', main_file, 'branch_candidate', 'branch_candidate')]:
            try:
                status, proposed = reconcile(evidence, side, path, data, base, remote, main_file, resolutions)
            except ValueError as error:
                status, proposed = 'RESOLUTION_REVIEW_REQUIRED', None
                failures.append({'path': path, 'side': side, 'error': str(error)})
            row['status' if side == 'workspace' else 'branch_status'] = status
            if not status.endswith('REVIEW_REQUIRED'):
                write_version(evidence, kind, path, proposed)
                row[prefix + '_deleted'] = proposed is None
                row[prefix + '_equals_' + side] = proposed == data
                row[prefix + '_sha256'] = hashlib.sha256(proposed).hexdigest() if proposed is not None else None
        rows.append(row)
        if count % 20 == 0:
            print(json.dumps({'reviewed': count, 'total': len(source['paths'])}), flush=True)
    source_changes = []
    for path, digest in source_hashes.items():
        p = ROOT / path
        current = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        if current != digest:
            source_changes.append(path)
    result = {'status': 'INTEGRATION_REVIEW_PREPARED', 'source': source, 'files': rows,
              'counts': dict(collections.Counter(row['status'] for row in rows)),
              'branch_counts': dict(collections.Counter(row['branch_status'] for row in rows)),
              'reconstruction_failures': failures, 'active_files_changed_during_snapshot': source_changes,
              'git_index_unchanged': hashlib.sha256(index_path.read_bytes()).hexdigest() == index_before,
              'git_writes': False, 'live_files_written': False, 'engine_tested': False}
    save_result(evidence, 'FILE_INTEGRATION_REVIEW.json', result)
    print(json.dumps({key: result[key] for key in ['status', 'counts', 'reconstruction_failures',
                                                'active_files_changed_during_snapshot', 'git_index_unchanged']}))


if __name__ == '__main__':
    main()
