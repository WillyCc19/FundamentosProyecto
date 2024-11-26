from flask import Flask, render_template, request, jsonify

app = Flask(__name__)






@app.route('/')
def form():
    return render_template('pagina1.html')

# Lista donde se almacenan  los cursos y tareas en la Página 2
cursos = [{'nombre_curso': 'Física', 'descripcion_tarea': 'Aprobar el curso'}]
#***********
@app.route('/pagina2', methods=['GET', 'POST'])
# POST: Enviar datos al servidor, GET: Solicitar información del servidor.
def formulario2():
    # Si la solicitud fue realizada con el método POST.
    if request.method == 'POST':
        # Manejo del formulario para agregar tareas en la pagina2
        nombre_curso = request.form.get('nombre_curso')  # llave dentro del diccionario cursos
        descripcion_tarea = request.form.get('descripcion_tarea')  # valor de la llave dentro del diccionario cursos

        if nombre_curso and descripcion_tarea:  # Si no están vacíos
            if descripcion_tarea.lower() == 'aprobar':  # Si el curso es "aprobar"
                descripcion_tarea = 'Curso no aprobado'  # Cambiar el nombre
            cursos.append({'nombre_curso': nombre_curso, 'descripcion_tarea': descripcion_tarea})

    # Renderizar la página con la lista de cursos
    return render_template('pagina2.html', cursos=cursos)


@app.route('/obtener_tareas', methods=['GET'])
# La función obtener_tareas solo responderá a solicitudes GET
def obtener_tareas():
    # Ruta para obtener todas las descripciones de tareas como JSON
    descripciones_tareas = [curso['descripcion_tarea'] for curso in cursos]
    # Flask envía la lista de descripciones de las tareas a la página en formato JSON
    return jsonify(descripciones_tareas)


@app.route('/eliminar_tarea', methods=['POST'])
# La función eliminar_tarea solo responderá a solicitudes POST
def eliminar_tarea():
    # Ruta para eliminar una tarea específica
    descripcion_tarea_a_eliminar = request.form.get('descripcion_tarea_a_eliminar')

    # Se refiere al diccionario cursos para que no se genere una variable local
    global cursos
    # Se examina que descripcion_tarea coincida con la descripción de tarea que el usuario quiere borrar.
    cursos = [curso for curso in cursos if curso['descripcion_tarea'] != descripcion_tarea_a_eliminar]
    # Solo se agregan a la nueva lista los cursos que no coinciden con la descripción de tarea a eliminar.
    # Redirigir de nuevo a la página de tareas
    return render_template('pagina2.html', cursos=cursos)





# Variables para almacenar las notas y sus porcentajes
notas = []  # Lista de tuplas (id, nota, porcentaje)
contador_id = 1  # Contador para asignar IDs únicos a las notas


@app.route('/calculadora_notas', methods=['GET', 'POST'])
def calculadora_notas():
    if request.method == 'POST':
        # Obtener nota y porcentaje del formulario
        nota = float(request.form.get('nota'))
        porcentaje = float(request.form.get('porcentaje'))

        # Validar si la nota y el porcentaje son correctos
        if 0 <= nota <= 20 and 0 <= porcentaje <= 100:
            global contador_id
            notas.append((contador_id, nota, porcentaje))  # Guardar nota y porcentaje
            contador_id += 1  # Incrementar el contador de IDs

    # Calcular el promedio ponderado
    peso_total = sum(porcentaje for _, _, porcentaje in notas)
    if peso_total == 0:
        promedio_ponderado = 0
    else:
        suma_ponderada = sum((nota * (porcentaje / 100)) for _, nota, porcentaje in notas)
        promedio_ponderado = round(suma_ponderada, 2)

    # Mostrar la página con las notas y el promedio
    return render_template('calculadora_notas.html', notas=notas, promedio_ponderado=promedio_ponderado)


@app.route('/eliminar_nota', methods=['POST'])
def eliminar_nota():
    # Obtener ID de la nota a eliminar
    nota_id = int(request.form.get('nota_id'))

    # Eliminar la nota con el ID proporcionado
    global notas
    notas = [nota for nota in notas if nota[0] != nota_id]

    # Calcular el nuevo promedio ponderado
    peso_total = sum(porcentaje for _, _, porcentaje in notas)
    if peso_total == 0:
        promedio_ponderado = 0
    else:
        suma_ponderada = sum((nota * (porcentaje / 100)) for _, nota, porcentaje in notas)
        promedio_ponderado = round(suma_ponderada, 2)

    # Redirigir a la página con las notas restantes y el nuevo promedio
    return render_template('calculadora_notas.html', notas=notas, promedio_ponderado=promedio_ponderado)


@app.route('/obtener_notas', methods=['GET'])
def obtener_notas():
    # Devolver todas las notas como JSON
    descripcion_notas = [{'id': nota[0], 'nota': nota[1], 'porcentaje': nota[2]} for nota in notas]
    return jsonify(descripcion_notas)





if __name__ == '__main__':
    app.run(debug=True)
