import 'package:flutter/material.dart';
import '../models/car.dart';
import '../services/api_service.dart';
import 'result_screen.dart';
import 'dart:convert';

class CarFormScreen extends StatefulWidget {
  const CarFormScreen({super.key});

  @override
  CarFormScreenState createState() => CarFormScreenState();
}

// ¡Clase pública! No debe comenzar con guion bajo
class CarFormScreenState extends State<CarFormScreen> {
  final _formKey = GlobalKey<FormState>();

  String fuel = 'gasolina';
  String shift = 'manual';
  int year = 0;
  int kms = 0;
  int power = 0;
  int doors = 0;

  bool _isLoading = false;
  bool _dataLoaded = false;

  final List<String> fuels = ['gasolina', 'diésel', 'eléctrico', 'híbrido'];
  final List<String> shifts = ['manual', 'automático'];

  Map<String, List<String>> brandsAndModels = {};
  String? selectedBrand;
  String? selectedModel;

  @override
  void initState() {
    super.initState();
    _loadBrandsAndModels();
  }

  Future<void> _loadBrandsAndModels() async {
    try {
      String jsonString = await DefaultAssetBundle.of(context)
          .loadString('assets/coches_por_marca.json');
      final Map<String, dynamic> data = json.decode(jsonString);

      final Map<String, List<String>> parsedData = {};
      data.forEach((key, value) {
        parsedData[key] = List<String>.from(value);
      });

      setState(() {
        brandsAndModels = parsedData;
        _dataLoaded = true;
      });
    } catch (e) {
      debugPrint('Error cargando marcas y modelos: $e');
    }
  }

  String? validateNumber(String? value) {
    if (value == null || value.isEmpty) return 'Campo requerido';
    final number = int.tryParse(value);
    if (number == null) return 'Introduce un número válido';
    return null;
  }

  Future<void> _submitForm() async {
    if (!_formKey.currentState!.validate()) return;

    _formKey.currentState!.save();

    setState(() {
      _isLoading = true;
    });

    final car = Car(
      make: selectedBrand ?? '',
      model: selectedModel ?? '',
      fuel: fuel,
      shift: shift,
      year: year,
      kms: kms,
      power: power,
      doors: doors,
    );

    try {
      double predictedPrice = await ApiService.predictPrice(car);

      if (!mounted) return;

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResultScreen(predictedPrice: predictedPrice),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: ${e.toString()}')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!_dataLoaded) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('ValoraCar'),
        titleTextStyle: const TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
        centerTitle: true,
        backgroundColor: Colors.deepPurple,
      ),
      body: SingleChildScrollView(
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
                  buildDropdown(
                    'Marca',
                    brandsAndModels.keys.toList(),
                    selectedBrand,
                    (val) {
                      setState(() {
                        selectedBrand = val;
                        selectedModel = null;
                      });
                    },
                  ),
                  if (selectedBrand != null)
                    buildDropdown(
                      'Modelo',
                      brandsAndModels[selectedBrand] ?? [],
                      selectedModel,
                      (val) => setState(() => selectedModel = val),
                    ),
                  buildDropdown('Combustible', fuels, fuel, (val) {
                    setState(() => fuel = val!);
                  }),
                  buildDropdown('Transmisión', shifts, shift, (val) {
                    setState(() => shift = val!);
                  }),
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

  Widget buildDropdown(String label, List<String> items, String? value, Function(String?) onChanged) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: DropdownButtonFormField<String>(
        decoration: InputDecoration(
          labelText: label,
          border: const OutlineInputBorder(),
        ),
        value: value,
        items: items.map((val) {
          return DropdownMenuItem(value: val, child: Text(val));
        }).toList(),
        onChanged: onChanged,
        validator: (val) => val == null ? 'Campo requerido' : null,
      ),
    );
  }
}
