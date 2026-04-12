from flask import Flask, request, jsonify

app = Flask(__name__)

# Arrays en memoria (aquí se guardan los datos)
alumnos = []
profesores = []

# Contadores para generar IDs automáticos
alumno_id_counter = 1
profesor_id_counter = 1

# ==================== VALIDACIONES ====================

def validar_alumno(data):
    """Valida que los datos del alumno sean correctos"""
    # Validar nombres
    if not data.get('nombres'):
        return False, "El campo 'nombres' es requerido"
    if not isinstance(data['nombres'], str):
        return False, "El campo 'nombres' debe ser texto"
    if len(data['nombres'].strip()) == 0:
        return False, "El campo 'nombres' no puede estar vacío"
    
    # Validar apellidos
    if not data.get('apellidos'):
        return False, "El campo 'apellidos' es requerido"
    if not isinstance(data['apellidos'], str):
        return False, "El campo 'apellidos' debe ser texto"
    if len(data['apellidos'].strip()) == 0:
        return False, "El campo 'apellidos' no puede estar vacío"
    
    # Validar matricula
    if not data.get('matricula'):
        return False, "El campo 'matricula' es requerido"
    if not isinstance(data['matricula'], str):
        return False, "El campo 'matricula' debe ser texto"
    if len(data['matricula'].strip()) == 0:
        return False, "El campo 'matricula' no puede estar vacío"
    
    # Validar promedio
    if 'promedio' not in data:
        return False, "El campo 'promedio' es requerido"
    if not isinstance(data['promedio'], (int, float)):
        return False, "El campo 'promedio' debe ser un número"
    if data['promedio'] < 0 or data['promedio'] > 10:
        return False, "El campo 'promedio' debe estar entre 0 y 10"
    
    return True, ""

def validar_profesor(data):
    """Valida que los datos del profesor sean correctos"""
    # Validar numeroEmpleado
    if not data.get('numeroEmpleado'):
        return False, "El campo 'numeroEmpleado' es requerido"
    if not isinstance(data['numeroEmpleado'], str):
        return False, "El campo 'numeroEmpleado' debe ser texto"
    if len(data['numeroEmpleado'].strip()) == 0:
        return False, "El campo 'numeroEmpleado' no puede estar vacío"
    
    # Validar nombres
    if not data.get('nombres'):
        return False, "El campo 'nombres' es requerido"
    if not isinstance(data['nombres'], str):
        return False, "El campo 'nombres' debe ser texto"
    if len(data['nombres'].strip()) == 0:
        return False, "El campo 'nombres' no puede estar vacío"
    
    # Validar apellidos
    if not data.get('apellidos'):
        return False, "El campo 'apellidos' es requerido"
    if not isinstance(data['apellidos'], str):
        return False, "El campo 'apellidos' debe ser texto"
    if len(data['apellidos'].strip()) == 0:
        return False, "El campo 'apellidos' no puede estar vacío"
    
    # Validar horasClase
    if 'horasClase' not in data:
        return False, "El campo 'horasClase' es requerido"
    if not isinstance(data['horasClase'], (int, float)):
        return False, "El campo 'horasClase' debe ser un número"
    if data['horasClase'] < 0:
        return False, "El campo 'horasClase' no puede ser negativo"
    
    return True, ""

# ==================== ENDPOINTS DE ALUMNOS ====================

@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    """GET /alumnos - Lista todos los alumnos"""
    return jsonify(alumnos), 200

@app.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    """GET /alumnos/{id} - Obtiene un alumno por su ID"""
    alumno = next((a for a in alumnos if a['id'] == id), None)
    if alumno:
        return jsonify(alumno), 200
    return jsonify({"error": "Alumno no encontrado"}), 404

@app.route('/alumnos', methods=['POST'])
def post_alumno():
    """POST /alumnos - Crea un nuevo alumno"""
    global alumno_id_counter
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Se esperaba un JSON válido"}), 400
    
    valido, msg = validar_alumno(data)
    if not valido:
        return jsonify({"error": msg}), 400
    
    alumno = {
        'id': alumno_id_counter,
        'nombres': data['nombres'].strip(),
        'apellidos': data['apellidos'].strip(),
        'matricula': data['matricula'].strip(),
        'promedio': float(data['promedio'])
    }
    alumnos.append(alumno)
    alumno_id_counter += 1
    
    return jsonify(alumno), 201

@app.route('/alumnos/<int:id>', methods=['PUT'])
def put_alumno(id):
    """PUT /alumnos/{id} - Actualiza un alumno existente"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Se esperaba un JSON válido"}), 400
    
    valido, msg = validar_alumno(data)
    if not valido:
        return jsonify({"error": msg}), 400
    
    for alumno in alumnos:
        if alumno['id'] == id:
            alumno['nombres'] = data['nombres'].strip()
            alumno['apellidos'] = data['apellidos'].strip()
            alumno['matricula'] = data['matricula'].strip()
            alumno['promedio'] = float(data['promedio'])
            return jsonify(alumno), 200
    
    return jsonify({"error": "Alumno no encontrado"}), 404

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    """DELETE /alumnos/{id} - Elimina un alumno"""
    global alumnos
    alumnos = [a for a in alumnos if a['id'] != id]
    return jsonify({}), 200

# ==================== ENDPOINTS DE PROFESORES ====================

@app.route('/profesores', methods=['GET'])
def get_profesores():
    """GET /profesores - Lista todos los profesores"""
    return jsonify(profesores), 200

@app.route('/profesores/<int:id>', methods=['GET'])
def get_profesor(id):
    """GET /profesores/{id} - Obtiene un profesor por su ID"""
    profesor = next((p for p in profesores if p['id'] == id), None)
    if profesor:
        return jsonify(profesor), 200
    return jsonify({"error": "Profesor no encontrado"}), 404

@app.route('/profesores', methods=['POST'])
def post_profesor():
    """POST /profesores - Crea un nuevo profesor"""
    global profesor_id_counter
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Se esperaba un JSON válido"}), 400
    
    valido, msg = validar_profesor(data)
    if not valido:
        return jsonify({"error": msg}), 400
    
    profesor = {
        'id': profesor_id_counter,
        'numeroEmpleado': data['numeroEmpleado'].strip(),
        'nombres': data['nombres'].strip(),
        'apellidos': data['apellidos'].strip(),
        'horasClase': float(data['horasClase'])
    }
    profesores.append(profesor)
    profesor_id_counter += 1
    
    return jsonify(profesor), 201

@app.route('/profesores/<int:id>', methods=['PUT'])
def put_profesor(id):
    """PUT /profesores/{id} - Actualiza un profesor existente"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Se esperaba un JSON válido"}), 400
    
    valido, msg = validar_profesor(data)
    if not valido:
        return jsonify({"error": msg}), 400
    
    for profesor in profesores:
        if profesor['id'] == id:
            profesor['numeroEmpleado'] = data['numeroEmpleado'].strip()
            profesor['nombres'] = data['nombres'].strip()
            profesor['apellidos'] = data['apellidos'].strip()
            profesor['horasClase'] = float(data['horasClase'])
            return jsonify(profesor), 200
    
    return jsonify({"error": "Profesor no encontrado"}), 404

@app.route('/profesores/<int:id>', methods=['DELETE'])
def delete_profesor(id):
    """DELETE /profesores/{id} - Elimina un profesor"""
    global profesores
    profesores = [p for p in profesores if p['id'] != id]
    return jsonify({}), 200

# ==================== INICIAR SERVIDOR ====================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
