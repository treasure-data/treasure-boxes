package com.treasuredata.polestar;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.os.Build;
import android.widget.Toast;

import androidx.core.app.NotificationCompat;

import com.polestar.naosdk.api.external.NAOERRORCODE;
import com.polestar.naosdk.api.external.NAOSensorsListener;
import com.polestar.naosdk.api.external.NAOServiceHandle;
import com.polestar.naosdk.api.external.NAOSyncListener;

public abstract class NaoAbstractClient<ServiceHandle extends NAOServiceHandle> implements NAOSensorsListener, NAOSyncListener {

    private Context context;
    private String apiKey;
    private ServiceHandle handle;

    public Context getContext() {
        return context;
    }

    public void setContext(Context context) {
        this.context = context;
    }

    public String getApiKey() {
        return apiKey;
    }

    public void setApiKey(String apiKey) {
        this.apiKey = apiKey;
    }

    protected abstract ServiceHandle createHandle();

    public void startService() {
        if (handle == null) {
            this.handle = createHandle();
        }
        handle.synchronizeData(this);
        handle.start();
    }

    protected void notifyUser(String msg) {
        Toast.makeText(context, msg, Toast.LENGTH_LONG).show();
    }

    protected void showNotification(String title, String msg){
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
