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
    
    # Validaciones
    campos_requeridos = ['nombres', 'apellidos', 'matricula']
    for campo in campos_requeridos:
        if campo not in data or not data[campo] or not isinstance(data[campo], str):
            return jsonify({'error': f'Campo {campo} es requerido y debe ser string'}), 400
    
    if 'promedio' not in data or not isinstance(data['promedio'], (int, float)):
        return jsonify({'error': 'Campo promedio es requerido y debe ser numérico'}), 400
    
    nuevo_id = max([a['id'] for a in alumnos], default=0) + 1
    nuevo_alumno = {
        'id': nuevo_id,
        'nombres': data['nombres'],
        'apellidos': data['apellidos'],
        'matricula': data['matricula'],
        'promedio': data['promedio']
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
        if not isinstance(data['nombres'], str):
            return jsonify({'error': 'nombres debe ser string'}), 400
        alumno['nombres'] = data['nombres']
    
    if 'apellidos' in data:
        if not isinstance(data['apellidos'], str):
            return jsonify({'error': 'apellidos debe ser string'}), 400
        alumno['apellidos'] = data['apellidos']
    
    if 'matricula' in data:
        if not isinstance(data['matricula'], str):
            return jsonify({'error': 'matricula debe ser string'}), 400
        alumno['matricula'] = data['matricula']
    
    if 'promedio' in data:
        if not isinstance(data['promedio'], (int, float)):
            return jsonify({'error': 'promedio debe ser numérico'}), 400
        alumno['promedio'] = data['promedio']
    
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
    
    campos_requeridos = ['numeroEmpleado', 'nombres', 'apellidos']
    for campo in campos_requeridos:
        if campo not in data or not data[campo] or not isinstance(data[campo], str):
            return jsonify({'error': f'Campo {campo} es requerido y debe ser string'}), 400
    
    if 'horasClase' not in data or not isinstance(data['horasClase'], (int, float)):
        return jsonify({'error': 'Campo horasClase es requerido y debe ser numérico'}), 400
    
    nuevo_id = max([p['id'] for p in profesores], default=0) + 1
    nuevo_profesor = {
        'id': nuevo_id,
        'numeroEmpleado': data['numeroEmpleado'],
        'nombres': data['nombres'],
        'apellidos': data['apellidos'],
        'horasClase': data['horasClase']
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
        if not isinstance(data['numeroEmpleado'], str):
            return jsonify({'error': 'numeroEmpleado debe ser string'}), 400
        profesor['numeroEmpleado'] = data['numeroEmpleado']
    
    if 'nombres' in data:
        if not isinstance(data['nombres'], str):
            return jsonify({'error': 'nombres debe ser string'}), 400
        profesor['nombres'] = data['nombres']
    
    if 'apellidos' in data:
        if not isinstance(data['apellidos'], str):
            return jsonify({'error': 'apellidos debe ser string'}), 400
        profesor['apellidos'] = data['apellidos']
    
    if 'horasClase' in data:
        if not isinstance(data['horasClase'], (int, float)):
            return jsonify({'error': 'horasClase debe ser numérico'}), 400
        profesor['horasClase'] = data['horasClase']
    
    return jsonify(profesor), 200

@app.route('/profesores/<int:id>', methods=['DELETE'])
def delete_profesor(id):
    global profesores
    profesor = next((p for p in profesores if p['id'] == id), None)
    if not profesor:
        return jsonify({'error': 'Profesor no encontrado'}), 404
    profesores = [p for p in profesores if p['id'] != id]
    return jsonify({'mensaje': 'Profesor eliminado'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
