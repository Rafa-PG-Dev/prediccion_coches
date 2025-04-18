// screens/home_screen.dart

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../screens/car_form_screen.dart'; // Importa CarFormScreen en lugar de InputForm

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Predicción de Precio de Coches',
          style: GoogleFonts.poppins(fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        backgroundColor: Colors.deepPurple,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              'assets/images/car_logo.png', // Asegúrate de tener una imagen en assets
              height: 200,
              fit: BoxFit.contain,
            ),
            const SizedBox(height: 20),
            Text(
              '¡Bienvenido a la app de predicción de precios de coches!',
              style: GoogleFonts.poppins(
                fontSize: 20,
                fontWeight: FontWeight.w600,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 15),
            Text(
              'Introduce los datos de tu coche para predecir su precio de mercado.',
              style: GoogleFonts.poppins(fontSize: 16),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 40),
            ElevatedButton.icon(
              onPressed: () {
                // Navegar a CarFormScreen (Formulario)
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const CarFormScreen()), // Cambiar a CarFormScreen
                );
              },
              icon: const Icon(Icons.arrow_forward_outlined),
              label: const Text('Comenzar'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepPurple,
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
