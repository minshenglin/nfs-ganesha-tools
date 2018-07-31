# nfs-ganesha-tools
Create cephfs subdirectory and setup quota without ceph-fuse

## Setup

- Install Package

```pip install -r requirements.txt1```

- Create NFS-Ganesha Pool

```
sudo ceph osd pool create nfs-ganesha 4 4
```
