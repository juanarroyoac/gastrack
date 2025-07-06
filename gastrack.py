from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')  # Usar un backend no interactivo
import matplotlib.pyplot as plt
import os


# Diccionario de autos y su rendimiento (km/L)
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
            # Obtener datos del formulario
            carro = request.form["carro"]
            km_dia = float(request.form["km_dia"])
            precio = float(request.form["precio"])

            # Buscar el rendimiento del carro seleccionado
            if carro not in car_stats:
                error = "El carro seleccionado no está en la lista."
                return render_template("index.html", error=error, car_stats=car_stats)
            rendimiento = car_stats[carro]

            # Validar que el rendimiento no sea 0
            if rendimiento == 0:
                error = "El rendimiento no puede ser 0."
                return render_template("index.html", error=error, car_stats=car_stats)

            # Calcular gastos
            litros_dia = km_dia / rendimiento
            gasto_dia = litros_dia * precio
            gasto_semana = gasto_dia * 7
            gasto_mes = gasto_dia * 30

            # Generar gráfica
            dias = list(range(1, 31))
            gasto_acumulado = [gasto_dia * d for d in dias]
            plt.figure(figsize=(14, 7))  # Mucho más grande para la web
            plt.plot(dias, gasto_acumulado, marker='o', color='#f76b1c', linewidth=3, markersize=8)
            plt.title(f"Gasto Acumulado para {carro}", fontsize=22, color='#232526', weight='bold')
            plt.xlabel("Día del mes", fontsize=16)
            plt.ylabel("Gasto ($)", fontsize=16)
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.xticks(fontsize=13)
            plt.yticks(fontsize=13)
            plt.tight_layout(pad=2.0)
            plt.gca().set_facecolor('#f7f7f7')

            # Guardar imagen en la carpeta static
            ruta_imagen = os.path.join(app.root_path, "static", "gasto.png")
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
            plt.savefig(ruta_imagen)
            plt.close()

            # Preparar resultados para mostrar en la página
            resultado = {
                "carro": carro,
                "gasto_dia": round(gasto_dia, 2),
                "gasto_semana": round(gasto_semana, 2),
                "gasto_mes": round(gasto_mes, 2)
            }

        except ValueError:
            error = "Por favor, ingresa valores numéricos válidos."
        except KeyError:
            error = "Por favor, completa todos los campos del formulario."

    return render_template("index.html", resultado=resultado, error=error, car_stats=car_stats)
if __name__ == "__main__":
    app.run(debug=True)