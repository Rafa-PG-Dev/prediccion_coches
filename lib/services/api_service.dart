// services/api_service.dart

import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/car.dart';
import '../utils/constants.dart';

class ApiService {
  static Future<double> predictPrice(Car car) async {
    final url = Uri.parse(API_BASE_URL);

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode(car.toJson()),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['predicted_price'] != null) {
          return data['predicted_price'].toDouble();
        } else {
          throw Exception('La respuesta no contiene el precio predicho');
        }
      } else {
        throw Exception('Error al obtener el precio. Código: ${response.statusCode}');
      }
    } catch (e) {
      print('Error al conectar con la API: $e');
      throw Exception('Error de conexión con la API: $e');
    }
  }
}
