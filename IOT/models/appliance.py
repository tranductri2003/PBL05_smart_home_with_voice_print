class Appliance:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return f"Appliance(ID: {self.id}, Name: {self.name}, Description: {self.description})"