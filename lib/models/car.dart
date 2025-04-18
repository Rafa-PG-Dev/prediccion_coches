class Car {
  String make;
  String model;
  String fuel;
  int year;
  int kms;
  int power;
  int doors;
  String shift;

  Car({
    this.make = '',
    this.model = '',
    this.fuel = '',
    this.year = 0,
    this.kms = 0,
    this.power = 0,
    this.doors = 0,
    this.shift = '',
  });

  String capitalize(String input) {
    if (input.isEmpty) return input;
    return input[0].toUpperCase() + input.substring(1).toLowerCase();
  }

  Map<String, dynamic> toJson() {
    return {
      'make': make.toUpperCase(),      
      'model': model,                  
      'fuel': capitalize(fuel),        
      'year': year,
      'kms': kms,
      'power': power,
      'doors': doors,
      'shift': capitalize(shift),      
    };
  }
}
