class Member:
    def __init__(self, id, name, about):
        self.id = id
        self.name = name
        self.about = about

    def __str__(self):
        return f"Member(ID: {self.id}, Name: {self.name}, About: {self.about})"