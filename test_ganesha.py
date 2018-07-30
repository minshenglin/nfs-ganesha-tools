import pytest
import ganesha

def test_cephfs_fsal_cast_from_string():
    fsal = ganesha.Fsal.parser("Name=CEPH;")
    assert isinstance(fsal, ganesha.CephfsFsal)

def test_cephfs_fsal_cast_from_dict():
    fsal = ganesha.Fsal.parserJson({"name": "ceph"})
    assert isinstance(fsal, ganesha.CephfsFsal)

def test_cephfs_fsal_cast_from_string_to_dict():
    fsal = ganesha.Fsal.parser("NAME=Ceph;")
    assert {"name": "ceph"} == fsal.dict()

def __get_rgw_fsal_str():
    return "Name=RGW;User_Id=nfs;Access_Key_Id=30GAEOGMTRX0SKWBAD19;Secret_Access_Key=DGMsovPHztquIllIKDJNVvf931xke97ABLsobpTI;"

def __get_rgw_fsal_dict():
    return {"name": "rgw", "user_id": "nfs", "access_key_id": "30GAEOGMTRX0SKWBAD19", "secret_access_key": "DGMsovPHztquIllIKDJNVvf931xke97ABLsobpTI"}

def test_cephfs_fsal_cast_from_dict_to_string():
    fsal = ganesha.Fsal.parserJson({"name": "ceph"})
    assert str(fsal) == "Name=CEPH;"

def test_rgw_fsal_cast_from_string():
    s = __get_rgw_fsal_str()
    fsal = ganesha.Fsal.parser(s)
    assert isinstance(fsal, ganesha.RgwFsal)
    assert fsal.user_id == "nfs"
    assert fsal.access_key == "30GAEOGMTRX0SKWBAD19"
    assert fsal.secret_key == "DGMsovPHztquIllIKDJNVvf931xke97ABLsobpTI"

def test_rgw_fsal_cast_from_dict():
    d = __get_rgw_fsal_dict()
    fsal = ganesha.Fsal.parserJson(d)
    assert isinstance(fsal, ganesha.RgwFsal)
    assert fsal.user_id == "nfs"
    assert fsal.access_key == "30GAEOGMTRX0SKWBAD19"
    assert fsal.secret_key == "DGMsovPHztquIllIKDJNVvf931xke97ABLsobpTI"

def test_rgw_fsal_cast_from_string_to_dict():
    s = __get_rgw_fsal_str()
    fsal = ganesha.Fsal.parser(s)
    d = __get_rgw_fsal_dict()
    assert d == fsal.dict()

def test_rgw_fsal_cast_from_dict_to_string():
    d = __get_rgw_fsal_dict()
    fsal = ganesha.Fsal.parserJson(d)
    s = __get_rgw_fsal_str()
    assert str(fsal) == s
