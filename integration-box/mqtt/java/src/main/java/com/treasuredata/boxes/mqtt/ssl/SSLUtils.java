package com.treasuredata.boxes.mqtt.ssl;

import org.eclipse.paho.client.mqttv3.MqttConnectOptions;

import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.security.GeneralSecurityException;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.cert.Certificate;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;

public class SSLUtils {

    public static PrivateKey loadPrivateKeyFromFile(final String filename, final String algorithm) {
        PrivateKey privateKey = null;

        File file = new File(filename);
        if (!file.exists()) {
            System.out.println("Private key file not found: " + filename);
            return null;
        }
        try (DataInputStream stream = new DataInputStream(new FileInputStream(file))) {
            privateKey = PrivateKeyReader.getPrivateKey(stream, algorithm);
        } catch (IOException | GeneralSecurityException e) {
            System.out.println("Failed to load private key from file " + filename);
        }

        return privateKey;
    }

    public static SSLContext loadSSLContext(final String clientCertFilename, final String privateKeyFilename) throws IOException, GeneralSecurityException {
        FileInputStream in = new FileInputStream(clientCertFilename);
        X509Certificate clientCert;
        try {
            clientCert = (X509Certificate) CertificateFactory.getInstance("X.509").generateCertificate(in);
            clientCert.checkValidity();
        } finally {
            in.close();
        }

        PrivateKey privateKey = loadPrivateKeyFromFile(privateKeyFilename, "RSA");

        KeyStore keyStore = KeyStore.getInstance(KeyStore.getDefaultType());
        keyStore.load(null, null);
        keyStore.setKeyEntry("private-key", privateKey, null, new Certificate[] {clientCert});

        KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory
                .getDefaultAlgorithm());
        kmf.init(keyStore, null);

        SSLContext context = SSLContext.getInstance("TLSv1.2");
        context.init(kmf.getKeyManagers(), null, null);

        return context;
    }

    public static MqttConnectOptions loadMqttConnectOptions(final String username, final String password, final String clientCertFilename, final String privateKeyFilename) throws IOException, GeneralSecurityException {
        MqttConnectOptions connOpts = new MqttConnectOptions();
        connOpts.setCleanSession(true);

        SSLContext context = loadSSLContext(clientCertFilename, privateKeyFilename);
        connOpts.setSocketFactory(context.getSocketFactory());
        connOpts.setUserName(username);
        connOpts.setPassword(password.toCharArray());

        return connOpts;
    }

}
