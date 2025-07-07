from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

plt.figure()
plt.close()

car_stats = {
    "Toyota Fortuner": 10,
    "Chevrolet Optra": 12,
    "Toyota Corolla": 14,
    "JAC Arena": 11,
    "Toyota Hilux": 9,
    "Hyundai Grand i10": 18,
    "Kia K3": 15,
    "Ford Ranger": 8,
    "Chevrolet Aveo": 13,
    "Hyundai Getz": 14
}

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    error = None

    if request.method == "POST":
        try:
            carro = request.form["carro"]
            km_dia = float(request.form["km_dia"])
            precio = float(request.form["precio"])

            if carro not in car_stats:
                error = "The selected car is not on the list."
                return render_template("index.html", error=error, car_stats=car_stats)
            rendimiento = car_stats[carro]

            if rendimiento == 0:
                error = "Efficiency cannot be 0."
                return render_template("index.html", error=error, car_stats=car_stats)

            litros_dia = km_dia / rendimiento
            gasto_dia = litros_dia * precio
            gasto_semana = gasto_dia * 7
            gasto_mes = gasto_dia * 30

            dias = list(range(1, 31))
            gasto_acumulado = [gasto_dia * d for d in dias]
            plt.figure(figsize=(14, 7))
            plt.plot(dias, gasto_acumulado, marker='o', color='#f76b1c', linewidth=3, markersize=8)
            plt.title(f"Accumulated Expense for {carro}", fontsize=22, color='#232526', weight='bold')
            plt.xlabel("Day of the month", fontsize=16)
            plt.ylabel("Expense ($)", fontsize=16)
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.xticks(fontsize=13)
            plt.yticks(fontsize=13)
            plt.tight_layout(pad=2.0)
            plt.gca().set_facecolor('#f7f7f7')

            ruta_imagen = os.path.join(app.root_path, "static", "gasto.png")
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
            plt.savefig(ruta_imagen)
            plt.close()

            resultado = {
                "carro": carro,
                "gasto_dia": round(gasto_dia, 2),
                "gasto_semana": round(gasto_semana, 2),
                "gasto_mes": round(gasto_mes, 2)
            }

        except ValueError:
            error = "Please enter valid numerical values."
        except KeyError:
            error = "Please complete all fields in the form."

    return render_template("index.html", resultado=resultado, error=error, car_stats=car_stats)

if __name__ == "__main__":
    app.run(debug=True)