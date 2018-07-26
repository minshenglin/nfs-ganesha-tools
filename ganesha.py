class Export():
    def __init__(self, export_id, path, clients, fsal):
        self.export_id = export_id
        self.path = path
        self.clients = clients
        self.fsal = fsal

    def __str__(self):
        s = "Export {\n\tExport_Id=%s;\n\tPath=%s;\n\tPseudo=%s;\n\tProtocols=4;\n\tTransports=TCP;\n" % \
            (self.export_id, self.path, self.path)

        for c in self.clients:
            s += "\tCLIENT { %s }\n" % c

        s += "\tFSAL { %s }\n" % self.fsal
        s += "}"
        return s

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

class CephfsFsal():
    def __str__(self):
        return "Name = CEPH;"

class RgwFsal():
    def __init__(self, user_id, access_key, secret_key):
        self.user_id = user_id
        self.access_key = access_key
        self.secret_key = secret_key

    def __str__(self):
        return "Name=RGW; User_Id=%s; Access_Key_Id=%s; Secret_Access_Key=%s;" % \
            (self.user_id, self.access_key, self.secret_key)

class Client():
    def __init__(self, cidrs, access_type=AccessType.NONE, squash=Squash.Root_Squash): 
        self.cidrs = cidrs
        self.access_type = access_type
        self.squash = squash

    def __str__(self):
        clients = ",".join(self.cidrs)
        return "Clients=%s; Squash=%s; Access_Type=%s;" % \
		(clients, self.squash, self.access_type)

if __name__ == '__main__':
    client = Client(["192.168.15.100"], access_type=AccessType.RW, squash=Squash.No_Root_Squash) 
    client2 = Client(["192.168.15.0/24"], access_type=AccessType.RO, squash=Squash.Root_Squash) 
    fsal = CephfsFsal()
    #fsal = RgwFsal("nfs", "30GAEOGMTRX0SKWBAD19", "DGMsovPHztquIllIKDJNVvf931xke97ABLsobpTI")
    export = Export(1234, "/test", [client, client2], fsal)
    print export
