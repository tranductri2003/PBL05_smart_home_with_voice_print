class Permission:
    def __init__(self, id, member_id, appliance_id, member_name=None, appliance_name=None):
        self.id = id
        self.member_id = member_id
        self.appliance_id = appliance_id
        self.member_name = member_name
        self.appliance_name = appliance_name

    def __str__(self):
        return f"Permission(ID: {self.id}, Member: {self.member_name}, Appliance: {self.appliance_name})"