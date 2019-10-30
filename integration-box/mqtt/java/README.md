# Treasure Data MQTT Broker: Java Example

The sample uses [Eclipse Paho Java Client](https://www.eclipse.org/paho/clients/java/) as an MQTT client.

## Preparation

Before connecting to the broker, retrieve server certificate and add it to your local keystore e.g., by using [escline/InstallCert](https://github.com/escline/InstallCert):

```sh
javac InstallCert.java

java InstallCert [host]:[port]

# Extract certificate from created jssecacerts keystore
keytool -exportcert -alias [host]-1 -keystore jssecacerts -storepass changeit -file [host].cer

# Import certificate into system keystore
keytool -importcert -alias [host] -keystore [path to system keystore] -storepass changeit -file [host].cer
```

## Usage

```sh
./gradlew run
```