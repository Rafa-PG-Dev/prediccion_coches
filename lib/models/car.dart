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

  Map<String, dynamic> toJson() {
    return {
      'make': make.toLowerCase(),
      'model': model.toLowerCase(),
      'fuel': fuel.toLowerCase(),
      'year': year,
      'kms': kms,
      'power': power,
      'doors': doors,
      'shift': shift.toLowerCase(),
    };
  }
}
