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

def connect_cephfs():
    cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
    libcephfs = cephfs.LibCephFS()
    libcephfs.create_with_rados(cluster)

    libcephfs.init()
    libcephfs.mount()

    return libcephfs

def to_xattr_name(var):

    var = var.lower()

    if var == "bytes":
        return 'ceph.quota.max_bytes'
    elif var == "files":
        return 'ceph.quota.max_files'
    else:
        print "Quota type is illegal:", var
        exit(errno.EINVAL)

def to_xattr_value(var):

    try: 
        int(var)
        return var
    except ValueError:
        print "Quota Value is illegal:", var
        exit(errno.EINVAL)

def check_vars():
    if len(sys.argv) != 5:
        print_help() 
        exit(errno.EINVAL)

    return

def print_help():
    print "Tool for create cephfs folder and set quota"
    print "Usage:", sys.argv[0], "create", "<cephfs path (ex: /test)>", "<quota type (bytes/files)>", "<quota value>" 

if __name__ == '__main__':

    check_root()
    check_vars()
    libcephfs = connect_cephfs()
    action = check_action(sys.argv[1])
    path = check_path(sys.argv[2])
    xattr_name = to_xattr_name(sys.argv[3])
    xattr_value = to_xattr_value(sys.argv[4])

    libcephfs.mkdir(path, 0o755)
    libcephfs.setxattr(path=path, name=xattr_name, value=xattr_value, flags=xattr.XATTR_CREATE)
    libcephfs.sync_fs()
