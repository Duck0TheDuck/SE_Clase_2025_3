const int sensorPin = A0;      // Pin del fototransistor
const int ledPin1 = 8;        // Foco 1
const int ledPin2 = 9;        // Foco 2
const int ledPin3 = 10;       // Foco 3

// Umbrales de oscuridad 
const int umbral1 = 700;      // 1 foco oscuro
const int umbral2 = 800;      // 2 focos 
const int umbral3 = 900;      // 3 focos 

// Variables para el filtrado
const int numLecturas = 5;    // Número de lecturas para la mediana
int lecturas[numLecturas];    // Array para almacenar lecturas
int indice = 0;               // Índice actual

void setup() {
  Serial.begin(9600);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
}

void loop() {
  // Lee el sensor y actualiza el array de lecturas
  lecturas[indice] = analogRead(sensorPin);
  indice = (indice + 1) % numLecturas;

  // Calcula la mediana de las últimas lecturas
  int mediana = calcularMediana(lecturas, numLecturas);

  // Control de focos según la mediana
  if (mediana >= umbral3) {
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, HIGH);
    digitalWrite(ledPin3, HIGH);
    Serial.println("Oscuridad ALTA - 3 focos encendidos");
  } 
  else if (mediana >= umbral2) {
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, HIGH);
    digitalWrite(ledPin3, LOW);
    Serial.println("Oscuridad MEDIA - 2 focos encendidos");
  } 
  else if (mediana >= umbral1) {
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin3, LOW);
    Serial.println("Oscuridad BAJA - 1 foco encendido");
  } 
  else {
    digitalWrite(ledPin1, LOW);
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin3, LOW);
    Serial.println("Luz suficiente - Todos los focos apagados");
  }

  // Muestra valores en el monitor serial
  Serial.print("Mediana: ");
  Serial.print(mediana);
  Serial.print(" | Valor crudo: ");
  Serial.println(analogRead(sensorPin));

  delay(500);  // Espera entre lecturas
}

// Función para calcular la mediana (ordena y toma el valor central)
int calcularMediana(int* array, int n) {
  // Copia el array para no modificar el original
  int copia[n];
  for (int i = 0; i < n; i++) copia[i] = array[i];
  
  // Ordena la copia (método burbuja simple)
  for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - i - 1; j++) {
      if (copia[j] > copia[j + 1]) {
        int temp = copia[j];
        copia[j] = copia[j + 1];
        copia[j + 1] = temp;
      }
    }
  }
  
  // Devuelve la mediana
  return copia[n / 2];
}

