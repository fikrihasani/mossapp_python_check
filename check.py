class Bagan:
    name = ""
    age = 0
    def __init__(self,name,age):
        self.name = name
        self.age = age
    
    def check(self):
        print(self.name)
        print(self.age)



bagan = Bagan("aaa",10)
bagan.check()