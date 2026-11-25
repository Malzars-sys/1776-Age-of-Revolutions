"""Preserve native benchmark lines as Windows rotates the debug log."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import re
import time

from simperf56_native_categories_20261123 import LAB, read


def archive(trial):
    (run,) = (LAB/'runs').glob(trial+'_*')
    launch = read(run/'LAUNCH.json')
    logs = Path(launch['profile'])/'logs'
    assert logs.resolve().is_relative_to((LAB/'profiles').resolve())
    output = LAB/'evidence'/(trial+'_NATIVE_LOG_ARCHIVE.log')
    seen, versions = set(), {}
    stop_deadline = time.monotonic()+launch['max_wall_seconds']+30
    print(f'{trial} native log archive ready at {datetime.now(timezone.utc).isoformat()}', flush=True)
    with output.open('xb', buffering=0) as stream:
        while time.monotonic() < stop_deadline:
            ended = (run/'EXIT.json').exists()
            log_dir = run/'logs' if ended and (run/'logs/debug.log').exists() else logs
            def generation(path):
                match = re.fullmatch(r'debug\.(\d+)\.log', path.name)
                return int(match[1]) if match else 0
            paths = sorted(log_dir.glob('debug*.log'), key=generation, reverse=True)
            for path in paths:
                try:
                    metadata = path.stat()
                    version = (metadata.st_size, metadata.st_mtime_ns)
                    if versions.get(path) == version:
                        continue
                    content = path.read_bytes()
                except OSError:
                    continue
                versions[path] = version
                for match in re.finditer(rb'(?m)^\[\d\d:\d\d:\d\d\][^\r\n]*SIM56\|(?:DAY\||WINDOW\||INIT\|)[^\r\n]+\r?\n', content):
                    line = match[0]
                    if line not in seen:
                        seen.add(line)
                        stream.write(line)
            if ended:
                break
            time.sleep(2)
    print(f'{trial} preserved {len(seen)} native log lines', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('trial')
    args = parser.parse_args()
    assert re.fullmatch(r'[A-Z0-9_]{2,40}', args.trial)
    archive(args.trial)
