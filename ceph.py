import rados
import cephfs
import xattr
import errno
import os
import sys
import ganesha 

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

if __name__ == '__main__':

    ceph = CephHandler()
    client = ganesha.Client(["192.168.15.100"], 
        access_type=ganesha.AccessType.RW, 
        squash=ganesha.Squash.No_Root_Squash)

    client2 = ganesha.Client(["192.168.15.0/24"], 
        access_type=ganesha.AccessType.RO, 
        squash=ganesha.Squash.Root_Squash)

    fsal = ganesha.CephfsFsal()
    #fsal = RgwFsal("nfs", "30GAEOGMTRX0SKWBAD19", "DGMsovPHztquIllIKDJNVvf931xke97ABLsobpTI")
    export = ganesha.Export(1234, "/test", [client, client2], fsal)

    ceph.write("nfs-ganesha", "export", str(export))
    print ceph.read("nfs-ganesha", "export")
