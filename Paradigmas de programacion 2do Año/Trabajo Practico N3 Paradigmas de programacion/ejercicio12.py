# Nombre alumno: Franco Genaro Reyes
class TarjetaCredito:
    def __init__(self, numero, banco, limite):
        self.numero = numero
        self.banco = banco
        self.limite = limite
        self.saldo_utilizado = 0

    def consumir(self, monto):
        if self.saldo_utilizado + monto <= self.limite:
            self.saldo_utilizado += monto
            print(f'Se consumieron ${monto} en la tarjeta {self.numero}.')
        else:
            print('No se puede consumir ese monto: excede el límite de la tarjeta.')

    def pagar(self, monto):
        self.saldo_utilizado -= monto
        if self.saldo_utilizado < 0:
            self.saldo_utilizado = 0
        print(f'Se pagó ${monto}. Saldo utilizado actual: ${self.saldo_utilizado}')

    def mostrar_estado(self):
        disponible = self.limite - self.saldo_utilizado
        print(f'Tarjeta {self.numero} - Banco: {self.banco}')
        print(f'Límite: ${self.limite} | Usado: ${self.saldo_utilizado} | Disponible: ${disponible}')

class Cliente:
    def __init__(self, nombre, dni):
        self.nombre = nombre
        self.dni = dni
        self.tarjetas = []

    def agregar_tarjeta(self, tarjeta):
        self.tarjetas.append(tarjeta)

    def gastar_en_tarjeta(self, numero_tarjeta, monto):
        for tarjeta in self.tarjetas:
            if tarjeta.numero == numero_tarjeta:
                tarjeta.consumir(monto)
                return
        print('No se encontró una tarjeta con ese número.')

    def mostrar_tarjetas(self):
        print(f'Cliente: {self.nombre} - DNI: {self.dni}')
        print('Tarjetas asociadas:')
        for tarjeta in self.tarjetas:
            tarjeta.mostrar_estado()

cliente = Cliente('Franco Genaro Reyes', '44123456')

t1 = TarjetaCredito('1234-5678-9012', 'Banco Nación', 50000)
t2 = TarjetaCredito('9876-5432-1098', 'Banco Galicia', 30000)

cliente.agregar_tarjeta(t1)
cliente.agregar_tarjeta(t2)

cliente.gastar_en_tarjeta('1234-5678-9012', 10000)
cliente.gastar_en_tarjeta('9876-5432-1098', 35000)

cliente.mostrar_tarjetas()