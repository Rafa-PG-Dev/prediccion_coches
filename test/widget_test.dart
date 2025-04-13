import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:prediccion_coches/main.dart';

void main() {
  testWidgets('Counter increments smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(MyApp());  // Elimina 'const' aquí

    // Verificar que nuestro contador comienza en 0
    expect(find.text('0'), findsOneWidget);
    expect(find.text('1'), findsNothing);

    // Tocar el ícono '+' y generar un nuevo frame.
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    // Verificar que nuestro contador ha incrementado.
    expect(find.text('0'), findsNothing);
    expect(find.text('1'), findsOneWidget);
  });
}
