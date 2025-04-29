# Nombre alumno: Franco Genaro Reyes
class ConversorMetros:
    def __init__(self, metros):
        self.metros = metros
        
    def a_km(self):
        return self.metros/1000
    
    def a_cm(self):
        return self.metros*100

conversor_metros1 = ConversorMetros(100)
print(f'Los metros ingresados en km son {conversor_metros1.a_km()} y en cm son {conversor_metros1.a_cm()}')