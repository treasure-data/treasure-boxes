package com.treasuredata.polestar;

import android.content.Context;
import android.widget.Toast;

import com.polestar.naosdk.api.external.NAOERRORCODE;
import com.polestar.naosdk.api.external.NAOGeofencingHandle;
import com.polestar.naosdk.api.external.NAOGeofencingListener;
import com.polestar.naosdk.api.external.NAOSensorsListener;
import com.polestar.naosdk.api.external.NAOSyncListener;
import com.polestar.naosdk.api.external.NaoAlert;

public class NaoGeofencingClient implements NAOGeofencingListener, NAOSensorsListener, NAOSyncListener {

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

    /**
     * NAOGeofencingListener
     */

    @Override
    public void onFireNaoAlert(NaoAlert alert) {
        notifyUser("Last alert received: " + alert.getName());
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
