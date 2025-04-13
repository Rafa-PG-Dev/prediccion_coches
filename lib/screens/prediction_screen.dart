import 'package:flutter/material.dart';

class PrediccionScreen extends StatefulWidget {
  @override
  _PrediccionScreenState createState() => _PrediccionScreenState();
}

class _PrediccionScreenState extends State<PrediccionScreen> {
  final TextEditingController _marcaController = TextEditingController();
  final TextEditingController _modeloController = TextEditingController();
  final TextEditingController _anioController = TextEditingController();
  final TextEditingController _kmController = TextEditingController();
  String _resultado = '';

  void predecirPrecio() {
    setState(() {
      _resultado = "Precio estimado: \$15,000"; // Esto será reemplazado por la IA más adelante.
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Predicción de Precios de Coches")),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(controller: _marcaController, decoration: InputDecoration(labelText: "Marca")),
            TextField(controller: _modeloController, decoration: InputDecoration(labelText: "Modelo")),
            TextField(controller: _anioController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: "Año")),
            TextField(controller: _kmController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: "Kilometraje")),
            SizedBox(height: 20),
            ElevatedButton(onPressed: predecirPrecio, child: Text("Predecir Precio")),
            SizedBox(height: 20),
            Text(_resultado, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }
}
