from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')  # Usar un backend no interactivo
import matplotlib.pyplot as plt
import os

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
            rendimiento = float(request.form["rendimiento"])
            precio = float(request.form["precio"])

            # Validar que el rendimiento no sea 0
            if rendimiento == 0:
                error = "El rendimiento no puede ser 0."
                return render_template("index.html", error=error)

            # Calcular gastos
            litros_dia = km_dia / rendimiento
            gasto_dia = litros_dia * precio
            gasto_semana = gasto_dia * 7
            gasto_mes = gasto_dia * 30

            # Generar gráfica
            dias = list(range(1, 31))
            gasto_acumulado = [gasto_dia * d for d in dias]
            plt.figure(figsize=(8, 4))
            plt.plot(dias, gasto_acumulado, marker='o', color='blue')
            plt.title(f"Gasto Acumulado para {carro}")
            plt.xlabel("Día del mes")
            plt.ylabel("Gasto ($)")
            plt.grid(True)
            plt.tight_layout()

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

    return render_template("index.html", resultado=resultado, error=error)

if __name__ == "__main__":
    app.run(debug=True)