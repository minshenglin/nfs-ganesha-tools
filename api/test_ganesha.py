import pytest
import ganesha

# test CephfsFsal

def __get_cephfs_fsal_str():
    return "Name=CEPH;"

def __get_cephfs_fsal_dict():
    return {"name": "ceph"}

def __get_cephfs_fsal_obj():
    return ganesha.CephfsFsal()

def test_cephfs_fsal_cast_from_string():
    s = __get_cephfs_fsal_str()
    fsal = ganesha.Fsal.parser(s)
    assert isinstance(fsal, ganesha.CephfsFsal)

def test_cephfs_fsal_cast_from_dict():
    d = __get_cephfs_fsal_dict()
    fsal = ganesha.Fsal.parser(d)
    assert isinstance(fsal, ganesha.CephfsFsal)

def test_cephfs_fsal_cast_from_string_to_dict():
    s = __get_cephfs_fsal_str()
    fsal = ganesha.Fsal.parser(s)
    d = __get_cephfs_fsal_dict()
    assert fsal.dict() == d

def test_cephfs_fsal_cast_from_dict_to_string():
    d = __get_cephfs_fsal_dict()
    fsal = ganesha.Fsal.parser(d)
    s = __get_cephfs_fsal_str()
    assert str(fsal) == s

# test RgwFsal

def __get_rgw_fsal_str():
    return "Name=RGW;User_Id=nfs;Access_Key_Id=30GAEOGMTRX0SKWBAD19;Secret_Access_Key=DGMsovPHztquIllIKDJNVvf931xke97ABLsobpTI;"

def __get_rgw_fsal_dict():
    return {"name": "rgw", "user_id": "nfs", "access_key_id": "30GAEOGMTRX0SKWBAD19", "secret_access_key": "DGMsovPHztquIllIKDJNVvf931xke97ABLsobpTI"}

def __get_rgw_fsal_obj():
    return ganesha.RgwFsal("nfs", "30GAEOGMTRX0SKWBAD19", "DGMsovPHztquIllIKDJNVvf931xke97ABLsobpTI")

def test_rgw_fsal_cast_from_string():
    s = __get_rgw_fsal_str()
    fsal = ganesha.Fsal.parser(s)
    assert fsal == __get_rgw_fsal_obj()

def test_rgw_fsal_cast_from_dict():
    d = __get_rgw_fsal_dict()
    fsal = ganesha.Fsal.parser(d)
    assert fsal == __get_rgw_fsal_obj()

def test_rgw_fsal_cast_from_string_to_dict():
    s = __get_rgw_fsal_str()
    fsal = ganesha.Fsal.parser(s)
    d = __get_rgw_fsal_dict()
    assert d == fsal.dict()

def test_rgw_fsal_cast_from_dict_to_string():
    d = __get_rgw_fsal_dict()
    fsal = ganesha.Fsal.parser(d)
    s = __get_rgw_fsal_str()
    assert str(fsal) == s

# test Clinet

def __get_client_str():
    return "Clients=192.168.15.11,192.168.16.0/24;Squash=No_Root_Squash;Access_Type=RW;" 

def __get_client_dict():
    return {"clients": ["192.168.15.11","192.168.16.0/24"], "access_type": "RW", "squash": "No_Root_Squash"}

def __get_client_obj():
    return ganesha.Client(["192.168.15.11", "192.168.16.0/24"], 
           access_type=ganesha.AccessType.RW, 
           squash=ganesha.Squash.No_Root_Squash)

def test_client_cast_from_string():
    s = __get_client_str()
    client = ganesha.Client.parser(s)
    assert client == __get_client_obj()
    
def test_client_cast_from_dict():
    d = __get_client_dict()
    client = ganesha.Client.parser(d)
    assert client == __get_client_obj()

def test_client_cast_from_string_to_dict():
    s = __get_client_str()
    client = ganesha.Client.parser(s)
    d = __get_client_dict()
    assert d == client.dict()

def test_client_cast_from_dict_to_string():
    d = __get_client_dict()
    client = ganesha.Client.parser(d)
    s = __get_client_str()
    assert s == str(client)

# test Export

def __get_export_str():
    client_str = __get_client_str()
    fsal_str = __get_rgw_fsal_str()
    return "Export{Export_Id=1234;Path=/test;Pseudo=/nfs/test;Protocols=4;Transports=TCP;" + \
           "CLIENT{%s}FSAL{%s}}" % (client_str, fsal_str)

def __get_export_dict():
    client_dict = __get_client_dict()
    fsal_dict = __get_rgw_fsal_dict()
    return {"export_id": "1234", "path": "/test", "pseudo": "/nfs/test", "protocols": "4",
            "transports": "TCP", "client": [client_dict], "fsal": fsal_dict}

def __get_export_obj():
    clients = [__get_client_obj()]
    fsal = __get_rgw_fsal_obj()
    return ganesha.Export("1234", "/test", clients, fsal, pseudo="/nfs/test", protocols="4", transports="TCP")

def test_export_cast_from_str(): 
    s = __get_export_str()
    export = ganesha.Export.parser(s)
    assert export == __get_export_obj()

def test_export_cast_from_dict(): 
    d = __get_export_dict()
    export = ganesha.Export.parser(d)
    assert export == __get_export_obj()

def test_export_cast_from_string_to_dict():
    s = __get_export_str()
    export = ganesha.Export.parser(s)
    d = __get_export_dict()
    assert d == export.dict()

def test_export_cast_from_dict_to_string():
    d = __get_export_dict()
    export = ganesha.Export.parser(d)
    s = __get_export_str()
    assert s == str(export)

# test GaneshaConfig

def __get_export_str_2():
    client_str = __get_client_str()
    fsal_str = __get_cephfs_fsal_str()
    return "Export{Export_Id=5678;Path=/test2;Pseudo=/nfs/test2;Protocols=4;Transports=TCP;" + \
           "CLIENT{%s}FSAL{%s}}" % (client_str, fsal_str)

def __get_export_obj_2():
    clients = [__get_client_obj()]
    fsal = __get_cephfs_fsal_obj()
    return ganesha.Export("5678", "/test2", clients, fsal, pseudo="/nfs/test2", protocols="4", transports="TCP")

def __get_export_dict_2():
    client_dict = __get_client_dict()
    fsal_dict = __get_cephfs_fsal_dict()
    return {"export_id": "5678", "path": "/test2", "pseudo": "/nfs/test2", "protocols": "4",
            "transports": "TCP", "client": [client_dict], "fsal": fsal_dict}

def __get_ganesha_config_str():
    export1 = __get_export_str()
    export2 = __get_export_str_2()
    return export1 + '\n' + export2

def __get_ganesha_config_obj():
    export1 = __get_export_obj()
    export2 = __get_export_obj_2()
    return ganesha.GaneshaConfig([export1, export2])

def __get_ganesha_config_dict():
    export1 = __get_export_dict()
    export2 = __get_export_dict_2()
    return {"export": [export1, export2]}

def test_ganesha_config_cast_from_str():
    s = __get_ganesha_config_str()
    config = ganesha.GaneshaConfig.parser(s)
    assert config == __get_ganesha_config_obj()

def test_ganesha_config_cast_from_dict():
    d = __get_ganesha_config_dict()
    config = ganesha.GaneshaConfig.parser(d)
    assert config == __get_ganesha_config_obj()

def test_export_cast_from_string_to_dict():
    s = __get_ganesha_config_str()
    config = ganesha.GaneshaConfig.parser(s)
    assert config.dict() == __get_ganesha_config_dict()

def test_export_cast_from_string_to_dict():
    d = __get_ganesha_config_dict()
    config = ganesha.GaneshaConfig.parser(d)
    assert str(config) == __get_ganesha_config_str()

