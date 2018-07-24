import rados
import cephfs
import xattr
import errno
import os
import sys

def check_root():
    if os.geteuid() == 0:
        return
    
    print "Only Root can execute this script."
    exit(errno.EACCES)

def check_action(var):
    if var.lower() != 'create':
        print "Action is not specific."
        exit(errno.EINVAL)

    return var

def check_path(var):
    if var[0] != '/':   # cephfs path should start from root (/)
        print 'Path is not illegal:', var
        exit(errno.EINVAL)

    return var

def to_value(var):
    try: 
        int(var)
        return var
    except ValueError:
        print "Quota Value is illegal:", var
        exit(errno.EINVAL)

def check_vars():
    if len(sys.argv) != 4:
        print_help() 
        exit(errno.EINVAL)

class CephHandler():
    def __init__(self):
        self.cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
        self.cluster.connect()
        self.fs = CephfsHandler(self.cluster)

    def createPool(self, name):
        pools = self.cluster.list_pools()
        if name in pools:
            return

        self.cluster.create_pool(name)

    def read(self, pool, name):
        ioctx = self.cluster.open_ioctx(pool)
        content = ioctx.read(name)
        ioctx.close()
        return content

    def write(self, pool, name, content):
        ioctx = self.cluster.open_ioctx(pool)
        ioctx.write_full(name, content)
        ioctx.close()

class CephfsHandler():
    def __init__(self, cluster):
        self.fs = cephfs.LibCephFS()
        self.fs.create_with_rados(cluster)
        self.fs.init()
        self.fs.mount()

    def mkdir(self, path, mode=0o755):
        try:
            self.fs.mkdir(path, mode)
            return True
        except cephfs.ObjectExists:
            return True
        except Exception:
            return False

    def setQuotaBytes(self, path, value):
        return self.__setQuota(path, "bytes", value)

    def __setQuota(self, path, kind, value): 
        if kind not in ["bytes", "files"]:
            return False

        name = "ceph.quota.max_"  + kind
        self.fs.setxattr(path=path, name=name, value=value, flags=xattr.XATTR_CREATE)
        return True

    def sync(self):
        self.fs.sync_fs()

def print_help():
    print "Tool for create cephfs folder and set max bytes quota"
    print "Usage:", sys.argv[0], "create", "<cephfs path (ex: /test)>", "<quota value (bytes)>" 

if __name__ == '__main__':

    check_root()
    check_vars()

    action = check_action(sys.argv[1])
    path = check_path(sys.argv[2])
    value = to_value(sys.argv[3])

    ceph = CephHandler()
    ceph.fs.mkdir(path)
    ceph.fs.setQuotaBytes(path, value)
    ceph.fs.sync()

    ceph.createPool("nfs-ganesha")
