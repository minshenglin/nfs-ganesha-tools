class Export():
    def __init__(self, export_id, path, clients, fsal):
        self.export_id = export_id
        self.path = path
        self.clients = clients
        self.fsal = fsal

    def __str__(self):
        s = "Export {\n\t Export_Id=%s;\n\t Path=%s;\n\t Pseudo=%s;\n\t Protocols=4;\n\t Transports=TCP;\n" % (self.export_id, self.path, self.path)
        for c in self.clients:
            s += "\t CLIENT { %s }\n" % c
        s += "\t FSAL { %s }\n }" % self.fsal
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

class Fsal():
    def __str__(self):
        return "Name = CEPH;"

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
    fsal = Fsal()
    export = Export(1234, "/test", [client, client2], fsal)
    print export
