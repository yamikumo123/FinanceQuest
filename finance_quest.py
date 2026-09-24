# Proyecto: FinanceQuest - Gamificación de Finanzas Personales
# Asignatura: Construcción de Software

import json
import os
from datetime import datetime

class Player:
    def __init__(self, name="Héroe Financiero", level=1, xp=0, hp=100):
        self.name = name
        self.level = level
        self.xp = xp
        self.hp = hp

    def add_xp(self, amount):
        self.xp += amount
        print(f"\n✨ ¡Ganaste +{amount} XP!")
        xp_needed = self.level * 100
        if self.xp >= xp_needed:
            self.level += 1
            self.xp -= xp_needed
            self.hp = min(100, self.hp + 20)
            print(f"🎉 ¡SUBISTE AL NIVEL {self.level}! Salud recuperada.")

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        print(f"\n💔 ¡Cuidado! Perdiste {amount} HP por gastos de alto riesgo.")
        if self.hp == 0:
            print("☠️ ¡Tu salud financiera llegó a 0! Necesitas recuperarte urgente registrando ahorros.")

class FinanceQuest:
    def __init__(self, data_file="game_data.json"):
        self.data_file = data_file
        self.player = Player()
        self.transactions = []
        self.load_data()

    def register_transaction(self):
        print("\n--- REGISTRAR MOVIMIENTO ---")
        print("1. Registrar Ingreso / Ahorro (Ganas XP)")
        print("2. Registrar Gasto (Peligro de daño en HP)")
        option = input("Selecciona una opción (1 o 2): ")

        if option not in ["1", "2"]:
            print("❌ Opción inválida.")
            return

        try:
            amount = float(input("Monto en $: "))
            category = input("Categoría (ej. Ocio, Comida, Sueldo, Ahorro): ").strip()
        except ValueError:
            print("❌ Por favor ingresa un número válido.")
            return

        is_income = (option == "1")
        transaction = {
            "amount": amount,
            "category": category,
            "is_income": is_income,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(transaction)

        if is_income:
            # 10% del monto ingresado se otorga como XP
            xp_gained = max(10, int(amount * 0.10))
            self.player.add_xp(xp_gained)
        else:
            # Si el gasto es mayor a $200 en categorías de ocio/caprichos, causa daño
            if category.lower() in ["ocio", "capricho", "juegos", "fiesta"] and amount > 200:
                self.player.take_damage(25)
            else:
                self.player.add_xp(5) # Un pequeño XP por llevar control de los gastos obligatorios

        self.save_data()

    def show_status(self):
        print("\n==================================")
        print(f"👤 JUGADOR: {self.player.name}")
        print(f"⭐ NIVEL:   {self.player.level}")
        print(f"✨ XP:      {self.player.xp} / {self.player.level * 100}")
        print(f"❤️ VIDA:    {self.player.hp} / 100")
        print(f"📊 HISTORIAL: {len(self.transactions)} movimientos registrados")
        print("==================================")

    def show_history(self):
        print("\n--- HISTORIAL DE TRANSACCIONES ---")
        if not self.transactions:
            print("No hay movimientos registrados aún.")
            return
        
        for t in self.transactions[-5:]: # Muestra las últimas 5
            tipo = "➕ Ingreso" if t["is_income"] else "➖ Gasto"
            print(f"[{t['date']}] {tipo}: ${t['amount']} | Cat: {t['category']}")

    def save_data(self):
        data = {
            "player": self.player.__dict__,
            "transactions": self.transactions
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.player = Player(**data["player"])
                self.transactions = data["transactions"]

# --- BUCLE INTERACTIVO DEL JUEGO ---
def main():
    game = FinanceQuest()
    
    while True:
        print("\n🎮 *** FINANCE QUEST *** 🎮")
        print("1. Ver Estado del Personaje")
        print("2. Registrar Ingreso o Gasto")
        print("3. Ver Historial")
        print("4. Salir")
        
        choice = input("\nEscoge una opción (1-4): ")

        if choice == "1":
            game.show_status()
        elif choice == "2":
            game.register_transaction()
        elif choice == "3":
            game.show_history()
        elif choice == "4":
            print("\n¡Gracias por jugar a FinanceQuest! Guardando progreso...")
            break
        else:
            print("❌ Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()