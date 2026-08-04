# Practica OCP (Open/Closed):
class ClienteNormal:
    def precio_final(self, precio):
        return precio
    
class ClientePremium:
    def precio_final(self, precio):
        return precio * 0.90
    
class ClienteVIP:
    def precio_final(self, precio):
        return precio * 0.80

def calcular_descuento(precio, cliente):
    return cliente.precio_final(precio)

# Practica LSP (sustitucion de Liskov):
class Empleado:
    def calcular_sueldo(self, horas):
        return horas * 10

class Gerente(Empleado):
    def calcular_sueldo(self, horas):
        return horas * 25

class Voluntario(Empleado):
    def calcular_sueldo(self, horas):
        # AQUI se encuentra el error, cuando llamamos a Voluntario (que hereda
        # de empleado), el metodo heredado calcular_sueldo traiciona dando un ValueError
        # en vez de un numero. Como lo dice el contrato.
        # Viola LSP porque la clase padre tiene un contrato en el metodo calcular_sueldo,
        # el cual es violado en Voluntario.
        raise ValueError("Los voluntarios no cobran")

def pagar_nomina(empleados, horas):
    total = 0
    for e in empleados:
        total += e.calcular_sueldo(horas)
    return total

# Practica ISP (Segregación de interfaces):
class Cajero:
    def cobrar(self, monto):
        return f'Cobrando {monto}'
class Mesero:
    def atender_mesa(self, mesa):
        return f'Atendiendo {mesa}'
class Cocinero:
    def cocinar(self, plato):
        return f"Preparando {plato}"

# Practica DIP (Inversion de dependencias):
# (tambien contiene SRP, OCP)
pedido_prueba = {"cliente": "franco@test.com",
                 "items": [{"precio": 100}, {"precio": 50}]}

class ServicioPedidos:
    # DIP aplicado porque la clase ya no depende de un notificador en especial, tiene
    # un contrato de que mientras sea notificador no le importa cual sea.
    def __init__(self, notificador):
        self.notificador = notificador

    def procesar(self, pedido):
        total = sum(item["precio"] for item in pedido["items"])
        self.notificador.enviar(pedido["cliente"], f"Tu pedido: ${total}")

class NotificadorWhatsapp:
    def enviar(self, cliente, mensaje):
        print(f"[WhatsApp] para {cliente}: {mensaje}")

class NotificadorEmail:
    def enviar(self, cliente, mensaje):
        print(f"[Email] para {cliente}: {mensaje}")

class NotificadorFalso:
    def __init__(self):
        self.enviados = []
    def enviar(self, cliente, mensaje):
        self.enviados.append([cliente, mensaje])

whatsapp = NotificadorWhatsapp()
servicio = ServicioPedidos(whatsapp)
servicio.procesar(pedido_prueba)

print(whatsapp.enviar)