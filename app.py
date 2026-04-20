from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Arrays en memoria
alumnos = []
profesores = []

# ------------------- ALUMNOS -------------------
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    return jsonify(alumnos), 200

@app.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    alumno = next((a for a in alumnos if a['id'] == id), None)
    if alumno:
        return jsonify(alumno), 200
    return jsonify({'error': 'Alumno no encontrado'}), 404

@app.route('/alumnos', methods=['POST'])
def create_alumno():
    data = request.get_json()
    
    # Validar campos requeridos
    campos_requeridos = ['nombres', 'apellidos', 'matricula', 'promedio']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None:
            return jsonify({'error': f'Campo {campo} es requerido'}), 400
    
    # Validar strings no vacios
    for campo in ['nombres', 'apellidos']:
        valor = data.get(campo, '')
        if not isinstance(valor, str) or valor.strip() == '':
            return jsonify({'error': f'Campo {campo} debe ser string no vacio'}), 400
    
    # matricula puede ser string o numero, lo convertimos a string
    matricula = data.get('matricula')
    if not isinstance(matricula, str):
        matricula = str(matricula)
    if matricula.strip() == '':
        return jsonify({'error': 'Campo matricula no puede estar vacio'}), 400
    
    # promedio debe ser numero
    try:
        promedio = float(data.get('promedio'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Campo promedio debe ser un numero valido'}), 400
    
    # Usar el id enviado si existe, sino generar uno nuevo
    nuevo_id = data.get('id')
    if nuevo_id is None:
        nuevo_id = max([a['id'] for a in alumnos], default=0) + 1
    else:
        try:
            nuevo_id = int(nuevo_id)
        except (ValueError, TypeError):
            nuevo_id = max([a['id'] for a in alumnos], default=0) + 1
    
    nuevo_alumno = {
        'id': nuevo_id,
        'nombres': data['nombres'].strip(),
        'apellidos': data['apellidos'].strip(),
        'matricula': matricula.strip(),
        'promedio': promedio
    }
    alumnos.append(nuevo_alumno)
    return jsonify(nuevo_alumno), 201

@app.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    alumno = next((a for a in alumnos if a['id'] == id), None)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404
    
    data = request.get_json()
    
    if 'nombres' in data:
        if data['nombres'] is None or (isinstance(data['nombres'], str) and data['nombres'].strip() == ''):
            return jsonify({'error': 'nombres no puede ser vacio'}), 400
        if isinstance(data['nombres'], str):
            alumno['nombres'] = data['nombres'].strip()
    
    if 'apellidos' in data:
        if data['apellidos'] is None or (isinstance(data['apellidos'], str) and data['apellidos'].strip() == ''):
            return jsonify({'error': 'apellidos no puede ser vacio'}), 400
        if isinstance(data['apellidos'], str):
            alumno['apellidos'] = data['apellidos'].strip()
    
    if 'matricula' in data:
        matricula = data['matricula']
        if matricula is None:
            return jsonify({'error': 'matricula no puede ser nula'}), 400
        if not isinstance(matricula, str):
            matricula = str(matricula)
        if matricula.strip() == '':
            return jsonify({'error': 'matricula no puede estar vacia'}), 400
        alumno['matricula'] = matricula.strip()
    
    if 'promedio' in data:
        try:
            alumno['promedio'] = float(data['promedio'])
        except (ValueError, TypeError):
            return jsonify({'error': 'promedio debe ser un numero valido'}), 400
    
    return jsonify(alumno), 200

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    global alumnos
    alumno = next((a for a in alumnos if a['id'] == id), None)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404
    alumnos = [a for a in alumnos if a['id'] != id]
    return jsonify({'mensaje': 'Alumno eliminado'}), 200

# ------------------- PROFESORES -------------------
@app.route('/profesores', methods=['GET'])
def get_profesores():
    return jsonify(profesores), 200

@app.route('/profesores/<int:id>', methods=['GET'])
def get_profesor(id):
    profesor = next((p for p in profesores if p['id'] == id), None)
    if profesor:
        return jsonify(profesor), 200
    return jsonify({'error': 'Profesor no encontrado'}), 404

@app.route('/profesores', methods=['POST'])
def create_profesor():
    data = request.get_json()
    
    campos_requeridos = ['numeroEmpleado', 'nombres', 'apellidos', 'horasClase']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None:
            return jsonify({'error': f'Campo {campo} es requerido'}), 400
    
    for campo in ['nombres', 'apellidos']:
        valor = data.get(campo, '')
        if not isinstance(valor, str) or valor.strip() == '':
            return jsonify({'error': f'Campo {campo} debe ser string no vacio'}), 400
    
    num_empleado = data.get('numeroEmpleado')
    if not isinstance(num_empleado, str):
        num_empleado = str(num_empleado)
    if num_empleado.strip() == '':
        return jsonify({'error': 'Campo numeroEmpleado no puede estar vacio'}), 400
    
    try:
        horas = float(data.get('horasClase'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Campo horasClase debe ser un numero valido'}), 400
    
    nuevo_id = data.get('id')
    if nuevo_id is None:
        nuevo_id = max([p['id'] for p in profesores], default=0) + 1
    else:
        try:
            nuevo_id = int(nuevo_id)
        except (ValueError, TypeError):
            nuevo_id = max([p['id'] for p in profesores], default=0) + 1
    
    nuevo_profesor = {
        'id': nuevo_id,
        'numeroEmpleado': num_empleado.strip(),
        'nombres': data['nombres'].strip(),
        'apellidos': data['apellidos'].strip(),
        'horasClase': horas
    }
    profesores.append(nuevo_profesor)
    return jsonify(nuevo_profesor), 201

@app.route('/profesores/<int:id>', methods=['PUT'])
def update_profesor(id):
    profesor = next((p for p in profesores if p['id'] == id), None)
    if not profesor:
        return jsonify({'error': 'Profesor no encontrado'}), 404
    
    data = request.get_json()
    
    if 'numeroEmpleado' in data:
        num = data['numeroEmpleado']
        if num is None:
            return jsonify({'error': 'numeroEmpleado no puede ser nulo'}), 400
        if not isinstance(num, str):
            num = str(num)
        if num.strip() == '':
            return jsonify({'error': 'numeroEmpleado no puede estar vacio'}), 400
        profesor['numeroEmpleado'] = num.strip()
    
    if 'nombres' in data:
        if data['nombres'] is None or (isinstance(data['nombres'], str) and data['nombres'].strip() == ''):
            return jsonify({'error': 'nombres no puede ser vacio'}), 400
        if isinstance(data['nombres'], str):
            profesor['nombres'] = data['nombres'].strip()
    
    if 'apellidos' in data:
        if data['apellidos'] is None or (isinstance(data['apellidos'], str) and data['apellidos'].strip() == ''):
            return jsonify({'error': 'apellidos no puede ser vacio'}), 400
        if isinstance(data['apellidos'], str):
            profesor['apellidos'] = data['apellidos'].strip()
    
    if 'horasClase' in data:
        try:
            profesor['horasClase'] = float(data['horasClase'])
        except (ValueError, TypeError):
            return jsonify({'error': 'horasClase debe ser un numero valido'}), 400
    
    return jsonify(profesor), 200

@app.route('/profesores/<int:id>', methods=['DELETE'])
def delete_profesor(id):
    global profesores
    profesor = next((p for p in profesores if p['id'] == id), None)
    if not profesor:
        return jsonify({'error': 'Profesor no encontrado'}), 404
    profesores = [p for p in profesores if p['id'] != id]
    return jsonify({'mensaje': 'Profesor eliminado'}), 200

# Manejador para rutas no encontradas (404)
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Ruta no encontrada'}), 404

# Manejador para metodo no permitido (405)
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Metodo no permitido'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
