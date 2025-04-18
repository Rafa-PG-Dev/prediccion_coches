import 'package:flutter/material.dart';
import '../models/car.dart';
import '../services/api_service.dart';
import 'result_screen.dart'; // Para navegar a la pantalla de resultados

class CarFormScreen extends StatefulWidget {
  const CarFormScreen({super.key});

  @override
  _CarFormScreenState createState() => _CarFormScreenState();
}

class _CarFormScreenState extends State<CarFormScreen> {
  final _formKey = GlobalKey<FormState>();
  String make = '';
  String model = '';
  String fuel = 'gasolina'; // Valor por defecto
  String shift = 'manual'; // Valor por defecto
  int year = 0;
  int kms = 0;
  int power = 0;
  int doors = 0;

  bool _isLoading = false;

  final List<String> fuels = ['gasolina', 'diésel', 'eléctrico', 'híbrido'];
  final List<String> shifts = ['manual', 'automático'];

  // Validación para campos numéricos
  String? validateNumber(String? value) {
    if (value == null || value.isEmpty) return 'Campo requerido';
    final number = int.tryParse(value);
    if (number == null) return 'Introduce un número válido';
    return null;
  }

  // Método para enviar los datos y obtener el precio estimado
  Future<void> _submitForm() async {
    if (!_formKey.currentState!.validate()) return;

    _formKey.currentState!.save();

    setState(() {
      _isLoading = true;
    });

    final car = Car(
      make: make,
      model: model,
      fuel: fuel,
      shift: shift,
      year: year,
      kms: kms,
      power: power,
      doors: doors,
    );

    try {
      // Obtener el precio estimado de la API
      double predictedPrice = await ApiService.predictPrice(car);

      if (!mounted) return;

      // Navegar a ResultScreen pasando el precio calculado
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResultScreen(predictedPrice: predictedPrice),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      // Mostrar mensaje de error
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: ${e.toString()}')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  // Método de construcción del formulario
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Formulario de Coche'),
        centerTitle: true,
        backgroundColor: Colors.deepPurple,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            const Text(
              'Introduce los datos del vehículo:',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 20),
            Form(
              key: _formKey,
              child: Column(
                children: [
                  buildTextField('Marca', (val) => make = val!),
                  buildTextField('Modelo', (val) => model = val!),
                  buildDropdown('Combustible', fuels, fuel, (val) => setState(() => fuel = val!)),
                  buildDropdown('Transmisión', shifts, shift, (val) => setState(() => shift = val!)),
                  buildNumberField('Año', (val) => year = int.parse(val!)),
                  buildNumberField('Kilómetros', (val) => kms = int.parse(val!)),
                  buildNumberField('Potencia (CV)', (val) => power = int.parse(val!)),
                  buildNumberField('Puertas', (val) => doors = int.parse(val!)),
                  const SizedBox(height: 20),
                  _isLoading
                      ? const CircularProgressIndicator()
                      : ElevatedButton.icon(
                          onPressed: _submitForm,
                          icon: const Icon(Icons.analytics_outlined),
                          label: const Text('Predecir Precio'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.deepPurple,
                            minimumSize: const Size(double.infinity, 50),
                            textStyle: const TextStyle(fontSize: 16),
                          ),
                        ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // Método para construir campos de texto (marca, modelo)
  Widget buildTextField(String label, Function(String?) onSaved) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: TextFormField(
        decoration: InputDecoration(
          labelText: label,
          border: const OutlineInputBorder(),
        ),
        validator: (value) => value == null || value.isEmpty ? 'Campo requerido' : null,
        onSaved: (value) => onSaved(value),
      ),
    );
  }

  // Método para construir campos numéricos (año, kilómetros, potencia, puertas)
  Widget buildNumberField(String label, Function(String?) onSaved) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: TextFormField(
        decoration: InputDecoration(
          labelText: label,
          border: const OutlineInputBorder(),
        ),
        keyboardType: TextInputType.number,
        validator: validateNumber,
        onSaved: (value) => onSaved(value),
      ),
    );
  }

  // Método para construir los dropdowns (combustible y transmisión)
  Widget buildDropdown(String label, List<String> items, String value, Function(String?) onChanged) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: DropdownButtonFormField<String>(
        decoration: InputDecoration(
          labelText: label,
          border: const OutlineInputBorder(),
        ),
        value: value,
        items: items.map((val) => DropdownMenuItem(value: val, child: Text(val))).toList(),
        onChanged: onChanged,
        validator: (val) => val == null ? 'Campo requerido' : null,
      ),
    );
  }
}
