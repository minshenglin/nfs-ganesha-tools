import re

class Export():
    def __init__(self, export_id, path, clients, fsal, pseudo=None, protocols="4", transports="TCP"):
        self.export_id = export_id
        self.path = path
        self.pseudo = pseudo if pseudo is not None else path
        self.protocols = protocols
        self.transports = transports
        self.clients = clients
        self.fsal = fsal

    def __eq__(self, other):
        return type(self) == type(other) and \
               self.export_id == other.export_id and \
               self.path == other.path and \
               self.pseudo == other.pseudo and \
               self.protocols == other.protocols and \
               self.transports == other.transports and \
               self.clients == other.clients and \
               self.fsal == other.fsal

    def __str__(self):
        s = "Export{Export_Id=%s;Path=%s;Pseudo=%s;Protocols=%s;Transports=%s;" % \
            (self.export_id, self.path, self.pseudo, self.protocols, self.transports)

        for c in self.clients:
            s += "CLIENT{%s}" % c

        s += "FSAL{%s}" % self.fsal
        s += "}"
        return s

    def dict(self):
        client_dict = [c.dict() for c in self.clients]
        return {"export_id": self.export_id, "path": self.path, "pseudo": self.pseudo, "protocols": self.protocols, 
                "transports": self.transports, "client": client_dict, "fsal": self.fsal.dict()}

    @staticmethod
    def parser(content):
        # simple attribute
        if isinstance(content, str):
            result = re.search("Export_Id=(.+?);Path=(.+?);Pseudo=(.+?);Protocols=(.+?);Transports=(.+?);", content)
            export_id = result.group(1)
            path = result.group(2)
            pseudo = result.group(3)
            protocols = result.group(4)
            transports = result.group(5)
        if isinstance(content, dict):
            export_id = content['export_id']
            path = content['path']
            pseudo = content['pseudo']
            protocols = content['protocols']
            transports = content['transports']
       
        # fsal attribute
        if isinstance(content, str):
            match = re.findall("FSAL{(?P<v>.+?)}", content)[0]
            fsal = Fsal.parser(match) 
        if isinstance(content, dict):
            fsal = Fsal.parser(content["fsal"])

        # client attribute
        if isinstance(content, str):
            clients = [Client.parser(c) for c in re.findall("CLIENT{(?P<v>.+?)}", content)]
        if isinstance(content, dict):
            clients = [Client.parser(c) for c in content['client']]

        return Export(export_id, path, clients, fsal, pseudo=pseudo, protocols=protocols, transports=transports)

class AccessType():
    RW = "RW"
    RO = "RO"
    MDONLY = "MDONLY"
    MDONLY_RO = "MDONLY_RO"
    NONE = "NONE" 

class Squash():
    No_Root_Squash = "No_Root_Squash"
    Root_Squash = "Root_Squash"
    All_Squash = "All_Squash"

class Fsal():
    @staticmethod 
    def parser(content):
        if isinstance(content, str):
            is_ceph_fsal = "name=ceph" in content.lower()
        elif isinstance(content, dict):
            is_ceph_fsal = content['name'] == 'ceph'

        if is_ceph_fsal:
            return CephfsFsal()

        return RgwFsal.parser(content)

class CephfsFsal():
    def __str__(self):
        return "Name=CEPH;"

    def __eq__(self, other):
        return type(self) == type(other)

    def dict(self):
        return {"name": "ceph"}

class RgwFsal():
    def __init__(self, user_id, access_key, secret_key):
        self.user_id = user_id
        self.access_key = access_key
        self.secret_key = secret_key

    def __eq__(self, other):
        return type(self) == type(other) and \
               self.user_id == other.user_id and \
               self.access_key == other.access_key and \
               self.secret_key == other.secret_key

    def __str__(self):
        return "Name=RGW;User_Id=%s;Access_Key_Id=%s;Secret_Access_Key=%s;" % \
            (self.user_id, self.access_key, self.secret_key)

    def dict(self):
        return {"name": "rgw", "user_id": self.user_id, "access_key_id": self.access_key, 
            "secret_access_key": self.secret_key}

    @staticmethod
    def parser(content):
        if isinstance(content, str):
            result = re.search("User_Id=(.+?);Access_Key_Id=(.+?);Secret_Access_Key=(.+?);", content)
            user_id = result.group(1)
            access_key = result.group(2)
            secret_key = result.group(3)
        elif isinstance(content, dict):
            user_id = content['user_id']
            access_key = content['access_key_id']
            secret_key = content['secret_access_key']

        return RgwFsal(user_id, access_key, secret_key)

class Client():
    def __init__(self, cidrs, access_type=AccessType.NONE, squash=Squash.Root_Squash): 
        self.cidrs = cidrs
        self.access_type = access_type
        self.squash = squash

    def __eq__(self, other):
        return type(self) == type(other) and self.cidrs == other.cidrs and \
               self.access_type == other.access_type and \
               self.squash == other.squash

    def __str__(self):
        clients = ",".join(self.cidrs)
        return "Clients=%s;Squash=%s;Access_Type=%s;" % \
		(clients, self.squash, self.access_type)

    def dict(self):
        return {"clients": self.cidrs, "access_type": self.access_type, "squash": self.squash}

    @staticmethod
    def parser(content):
        if isinstance(content, str):
            result = re.search("Clients=(.+?);Squash=(.+?);Access_Type=(.+?);", content)
            cidrs = result.group(1).split(',')
            squash = result.group(2)
            access_type = result.group(3)
        elif isinstance(content, dict):
            cidrs = content['clients']
            squash = content['squash']
            access_type = content['access_type']

        return Client(cidrs, access_type=access_type, squash=squash)

class GaneshaConfig():
    def __init__(self, exports):
        self.exports = exports

    def __str__(self):
        return "\n".join(map(str, self.exports))

    def dict(self):
        return {"export": [e.dict() for e in self.exports]}

    @staticmethod
    def parser(content):
        if content is None or content == "":
           return GaneshaConfig([])

        exports = []
        for line in content.split('\n'):
           exports.append(Export.parser(line))

        return GaneshaConfig(exports)

    @staticmethod
    def parserJson(content):
        exports = []
        for j in content['export']:
            exports.append(Export.parserJson(j))

        return GaneshaConfig(exports)

if __name__ == '__main__':
    client = Client(["192.168.15.100"], access_type=AccessType.RW, squash=Squash.No_Root_Squash) 
    client2 = Client(["192.168.15.0/24"], access_type=AccessType.RO, squash=Squash.Root_Squash) 
    ceph_fsal = CephfsFsal()
    rgw_fsal = RgwFsal("nfs", "30GAEOGMTRX0SKWBAD19", "DGMsovPHztquIllIKDJNVvf931xke97ABLsobpTI")
    export = Export(1234, "/test", [client, client2], ceph_fsal, pseudo="/cephfs/test")
    export2 = Export(6789, "/test2", [client, client2], rgw_fsal, pseudo="/rgw/test2")

    config = GaneshaConfig.parser(str(export) + "\n" + str(export2))
    print config

    #import json
    #content = config.dict()
    #print content
    #print GaneshaConfig.parserJson(content)
