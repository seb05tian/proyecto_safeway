import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  final String baseUrl;

  ApiService(this.baseUrl);

  // Método para registrar un nuevo usuario
  Future<bool> register(String nombre, String correoElectronico, String contrasena) async {
    final response = await http.post(
      Uri.parse('$baseUrl/usuarios/create'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'nombre': nombre,
        'correo_electronico': correoElectronico,
        'contrasena': contrasena,
        'rol': 'cliente', // Se asigna un rol por defecto
      }),
    );

    return response.statusCode == 201;
  }

  // Método para iniciar sesión
  Future<String?> login(String emailOrName, String contrasena) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'email_or_name': emailOrName,
        'contrasena': contrasena,
      }),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final token = data['token'];
      // Guardar el token en shared preferences
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', token);
      return token;
    } else {
      return null; // O manejar el error de otra manera
    }
  }

  // Método para cerrar sesión
  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');
  }
}
