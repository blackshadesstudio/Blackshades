#!/usr/bin/env python3
"""Build the complete static site using only Python's standard library."""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'dist'
PAGES = ('index.html', '404.html', 'privacy.html', 'thank-you.html', 'robots.txt', 'sitemap.xml')
ARCHIVES = ('assets-01.zip', 'assets-02.zip')

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = []
        self.anchors = []
    def handle_starttag(self, tag, attributes):
        data = dict(attributes)
        if data.get('id'):
            self.ids.append(data['id'])
        for key in ('src', 'href'):
            if data.get(key):
                self.refs.append(data[key])
        for key in ('srcset', 'imagesrcset'):
            for part in data.get(key, '').split(','):
                if part.strip():
                    self.refs.append(part.strip().split()[0])

def main():
    required = list(PAGES) + list(ARCHIVES) + ['asset-manifest.json']
    missing = [name for name in required if not (ROOT / name).is_file()]
    if missing:
        raise RuntimeError('Upload all package files to the repository root. Missing: ' + ', '.join(missing))
    manifest = json.loads((ROOT / 'asset-manifest.json').read_text(encoding='utf-8'))
    if OUTPUT.is_symlink():
        raise RuntimeError('The dist output must be a regular directory, not a symlink.')
    with tempfile.TemporaryDirectory(prefix='.build-', dir=ROOT) as temp:
        destination = Path(temp) / 'dist'
        destination.mkdir()
        for name in PAGES:
            shutil.copyfile(ROOT / name, destination / name)
        written = set()
        for name in ARCHIVES:
            with zipfile.ZipFile(ROOT / name) as archive:
                for member in archive.infolist():
                    if member.is_dir():
                        continue
                    relative = PurePosixPath(member.filename)
                    if relative.is_absolute() or '..' in relative.parts or not relative.parts or relative.parts[0] != 'assets':
                        raise RuntimeError('Unexpected asset path in ' + name + ': ' + member.filename)
                    if member.filename in written:
                        raise RuntimeError('Duplicate asset: ' + member.filename)
                    target = destination.joinpath(*relative.parts)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.read(member))
                    written.add(member.filename)
        expected = manifest['files']
        if written != set(expected):
            raise RuntimeError('The asset archives are incomplete or mismatched. Re-upload both assets ZIP files.')
        for name, digest in expected.items():
            actual = hashlib.sha256((destination / name).read_bytes()).hexdigest()
            if actual != digest:
                raise RuntimeError('Asset integrity check failed: ' + name)
        for name in PAGES:
            if not name.endswith('.html'):
                continue
            document = Document()
            document.feed((destination / name).read_text(encoding='utf-8'))
            if len(document.ids) != len(set(document.ids)):
                raise RuntimeError('Duplicate element ID in ' + name)
            for reference in document.refs:
                parsed = urlsplit(reference)
                if parsed.scheme or parsed.netloc:
                    continue
                if parsed.path:
                    local = destination / unquote(parsed.path.lstrip('/'))
                    if local.is_dir():
                        local = local / 'index.html'
                    if not local.is_file():
                        raise RuntimeError('Missing page resource in ' + name + ': ' + reference)
                elif parsed.fragment and parsed.fragment not in document.ids:
                    raise RuntimeError('Missing page anchor in ' + name + ': ' + reference)
        for stylesheet in (destination / 'assets').glob('*.css'):
            for reference in re.findall(r'url\([\'"]?([^\)\'\"]+)', stylesheet.read_text(encoding='utf-8')):
                if not urlsplit(reference).scheme and not (stylesheet.parent / reference).is_file():
                    raise RuntimeError('Missing stylesheet resource: ' + reference)
        index = (destination / 'index.html').read_text(encoding='utf-8')
        if index.count('class="gallery-card"') != manifest['gallery_frames']:
            raise RuntimeError('Unexpected gallery photo count.')
        if OUTPUT.exists():
            shutil.rmtree(OUTPUT)
        os.replace(destination, OUTPUT)
    print('Build passed: all {} portfolio photographs and {} asset files verified.'.format(manifest['gallery_frames'], len(expected)))
    print('Publish directory: dist')
    print('The complete website is at dist/index.html')

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('BUILD ERROR: ' + str(error), file=sys.stderr)
        sys.exit(1)
