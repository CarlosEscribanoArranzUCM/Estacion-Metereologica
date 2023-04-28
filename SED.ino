#include "DHT.h"

#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

String inputString = "";      // Cadena para guardar el comando recibido
bool stringComplete = false;  // Bool que indica cuando el comando fue recibido 
			      // y podemos compararlo con los comandos válidos
int value;		      // Store value from photoresistor (0-1023)

const int DHTPin = 5;     // what digital pin we're connected to

DHT dht(DHTPin, DHTTYPE);

//Constants
const int ledCalor = 13;
const int motorFrio = 3;
const int pResistor = A0; // Photoresistor at Arduino analog pin A0
const int ledPin=10;      // Led pin at Arduino pin 10

void setup() {
  Serial.begin(9600);

  dht.begin();

  pinMode(ledCalor, OUTPUT);
  pinMode(motorFrio, OUTPUT);
  // initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

void loop() {

  if (stringComplete) {//El comando fue recibido, procedemos a compararlo
    
    if (inputString.equals("/temperature") ){//Si el comando es "temperature"
      float temperature = dht.readTemperature();
      if (isnan(temperature)) {
        Serial.println("Failed to read from DHT sensor!");
      }
      else{
        Serial.println(temperature);        
      }
    }
    else if (inputString.equals("/humidity") ){//Si el comando es "humidity"
      float humidity = dht.readHumidity();
      if (isnan(humidity)) {
        Serial.println("Failed to read from DHT sensor!");
      }
      else{
        Serial.println(humidity);
      }
    }
    else if (inputString.equals("/hot") ){//Si el comando es "hot"
      digitalWrite(ledCalor, LOW);
      digitalWrite(motorFrio, HIGH);
      Serial.println("Fan activated");
    }
    else if (inputString.equals("/cold") ){//Si el comando es "cold"
      digitalWrite(ledCalor, HIGH);
      digitalWrite(motorFrio, LOW);
      Serial.println("Stove activated");
    }
    else if (inputString.equals("/off") ){//Si el comando es "off"
      digitalWrite(ledCalor, LOW);
      digitalWrite(motorFrio, LOW);
      Serial.println("Shut down both electronic devices");
    }
    else if (inputString.equals("/light") ){//Si el comando es "light"
      value = analogRead(pResistor);
      Serial.println(value);
    }
    else if (inputString.equals("/light_came_on") ){//Si el comando es "ligh_came_on"
      digitalWrite(ledPin, HIGH);
      Serial.println("The light came ON!");
    }
    else if (inputString.equals("/light_came_off") ){//Si el comando es "light_came_off"
      digitalWrite(ledPin, LOW);
      Serial.println("The light came OFF!");
    }
    else{
      Serial.println("Command not recognized, try again");
    }
    inputString = "";//Limpiamos la cadena para poder recibir el siguiente comando
    stringComplete = false;//Bajamos la bandera para no volver a ingresar a la comparación hasta que recibamos un nuevo comando
  }
}

void serialEvent() {
  
  while (Serial.available()) {//Mientras tengamos caracteres disponibles en el buffer
    char inChar = (char)Serial.read();//Leemos el siguiente caracter
    if (inChar == '\n') {//Si el caracter recibido corresponde a un salto de línea
      stringComplete = true;//Levantamos la bandera 
    }
    else{//Si el caracter recibido no corresponde a un salto de línea
      inputString += inChar;//Agregamos el caracter a la cadena 
    }
  }
}
