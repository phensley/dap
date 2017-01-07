
import os, sys, time
from .util import info


class Entry(object):

    def __init__(self, modify, size, filetype, name):
        self.modify = modify
        self.size = size
        self.filetype = filetype
        self.name = name


class FTP(object):

    def __init__(self, host, initpath='.'):
        from ftplib import FTP as _FTP
        self.conn = _FTP(host)
        self.conn.login('anonymous', 'user@example.com')
        self.conn.cwd(initpath)

    def list(self):
        ls = []
        self.conn.retrlines('MLSD', ls.append)
        return parse_mlsd(ls)

    def chdir(self, path):
        self.conn.cwd(path)

    def walk(self, root, oper):
        info('%s %r' % (oper, root.name))
        dirs = []
        self.chdir(root.name)
        size = 0

        for entry in self.list():
            if entry.filetype == 'cdir':
                root.modify = entry.modify
            elif entry.filetype == 'dir':
                entry.name = os.path.join(root.name, entry.name)
                dirs.append(entry)
            elif entry.filetype == 'file':
                entry.name = os.path.join(root.name, entry.name)
                root.size += entry.size
                yield entry

        for d in dirs:
            for entry in self.walk(d, oper):
                yield entry
            root.size += d.size

        yield root

    def dirsize(self, rootdir):
        root = Entry('', 0, 'dir', rootdir)
        for entry in self.walk(root, 'sizing'):
            if entry.filetype == 'dir':
                yield entry

    def download(self, srcdir, dstdir, limiter=None):
        root = Entry('', 0, 'dir', srcdir)
        for entry in self.walk(root, 'scanning'):
            if entry.filetype == 'file':
                dstpath = os.path.join(dstdir, entry.name.lstrip('/'))
                parent = os.path.dirname(dstpath)
                if not os.path.exists(parent):
                    os.makedirs(parent)

                if os.path.exists(dstpath):
                    size = os.stat(dstpath).st_size
                    if size == entry.size:
                        info('skipping %r' % dstpath)
                        continue

                resume = None
                out = open(dstpath, 'ab')
                if os.path.exists(dstpath):
                    resume = os.stat(dstpath).st_size
                    out.seek(0, os.SEEK_END)

                name = entry.name[-52:]
                if name != entry.name:
                    name = '..' + name[2:]

                written = [0]
                def _cb(data):
                    out.write(data)
                    sz = len(data)
                    written[0] += sz
                    pct = written[0] / float(entry.size)

                    sys.stderr.write('\r{0:>52s}  [{1:20s}] {2:.1f}%'.format(name, '#'*int(pct*20), pct*100))
                    sys.stderr.flush()

                    if limiter is not None:
                        delay = limiter(sz)
                        if delay:
                            time.sleep(delay)

                self.conn.retrbinary('RETR ' + entry.name, _cb, rest=resume)
                info('')
                out.close()


def parse_mlsd(lines):
    r = []
    for line in lines:
        line, name = line.split(' ', 1)
        kvs = [e.split('=', 1) for e in line.strip(';').split(';')]
        kvs = {k: v for k, v in kvs}
        modify, size = int(kvs['modify']), int(kvs.get('size', 0))
        e = Entry(modify, size, kvs['type'], name)
        r.append(e)
    return r

