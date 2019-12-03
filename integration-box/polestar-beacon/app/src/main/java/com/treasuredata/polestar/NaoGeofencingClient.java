package com.treasuredata.polestar;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.os.Build;
import android.widget.Toast;

import androidx.core.app.NotificationCompat;

import com.polestar.naosdk.api.external.NAOERRORCODE;
import com.polestar.naosdk.api.external.NAOGeofenceListener;
import com.polestar.naosdk.api.external.NAOGeofencingHandle;
import com.polestar.naosdk.api.external.NAOSensorsListener;
import com.polestar.naosdk.api.external.NAOSyncListener;
import com.polestar.naosdk.api.external.NaoAlert;

public class NaoGeofencingClient implements NAOGeofenceListener, NAOSensorsListener, NAOSyncListener {

    private Context context;
    private NAOGeofencingHandle handle;

    public NaoGeofencingClient(Context context, String naoServiceApiKey) {
        this.context = context;
        this.handle = new NAOGeofencingHandle(context, MyNaoService.class, naoServiceApiKey, this, this);
        handle.synchronizeData(this);
        handle.start();
    }

    public void notifyUser(String msg) {
        Toast.makeText(context, msg, Toast.LENGTH_LONG).show();
    }

    public void showNotification(String title, String msg){
        String CHANNEL_ID = "geofencing_channel_01";

        NotificationManager notificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);

        // Create the NotificationChannel, but only on API 26+ because
        // the NotificationChannel class is new and not in the support library
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, "geofencing", NotificationManager.IMPORTANCE_DEFAULT);
            channel.setDescription("notification based on geofencing");
            // Register the channel with the system; you can't change the importance
            // or other notification behaviors after this
            notificationManager.createNotificationChannel(channel);
        }

        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, CHANNEL_ID)
                    .setSmallIcon(R.drawable.googleg_standard_color_18)
                    .setContentTitle(title)
                    .setContentText(msg)
                    .setPriority(NotificationCompat.PRIORITY_DEFAULT)
                    .setContentIntent(null)
                    .setAutoCancel(true);

        notificationManager.notify(1, builder.build());
    }

    /**
     * NAOGeofencingListener
     */

    @Override
    public void onFireNaoAlert(NaoAlert alert) {
        showNotification("NAO", "Last alert received: " + alert.getName());
    }

    /**
     * NAOGeofenceListener
     */

    @Override
    public void onEnterGeofence(int regionId, String regionName) {
        notifyUser("Enter region " + regionId + "(" + regionName + ")");
    }

    @Override
    public void onExitGeofence(int regionId, String regionName) {
        notifyUser("Exit region " + regionId + "(" + regionName + ")");
    }

    /**
     * NAOErrorListener
     */

    @Override
    public void onError(NAOERRORCODE naoerrorcode, String msg) {
        notifyUser(msg);
    }

    /**
     * NAOSensorsListener
     */

    @Override
    public void requiresCompassCalibration() {
        notifyUser("Calibrate Compass");
    }

    @Override
    public void requiresWifiOn() {
        notifyUser("Turn on WiFi");
    }

    @Override
    public void requiresBLEOn() {
        notifyUser("Turn on Bluetooth");
    }

    @Override
    public void requiresLocationOn() {
        notifyUser("Turn on location");
    }

    /**
     * NAOSyncListener
     */

    @Override
    public void onSynchronizationSuccess() {
        notifyUser("Sync succeeded");
    }

    @Override
    public void onSynchronizationFailure(NAOERRORCODE naoerrorcode, String msg) {
        notifyUser("Sync failed (" + naoerrorcode + "): " + msg);
    }

}
