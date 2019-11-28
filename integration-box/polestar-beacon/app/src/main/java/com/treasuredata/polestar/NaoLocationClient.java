package com.treasuredata.polestar;

import android.content.Context;
import android.location.Location;
import android.widget.Toast;

import com.polestar.naosdk.api.external.NAOERRORCODE;
import com.polestar.naosdk.api.external.NAOLocationHandle;
import com.polestar.naosdk.api.external.NAOLocationListener;
import com.polestar.naosdk.api.external.NAOSensorsListener;
import com.polestar.naosdk.api.external.NAOSyncListener;
import com.polestar.naosdk.api.external.TNAOFIXSTATUS;

public class NaoLocationClient implements NAOLocationListener, NAOSensorsListener, NAOSyncListener {

    private Context context;
    private NAOLocationHandle handle;

    public NaoLocationClient(Context context, String naoServiceApiKey) {
        this.context = context;
        this.handle = new NAOLocationHandle(context, MyNaoService.class, naoServiceApiKey, this, this);
        handle.synchronizeData(this);
        handle.start();
    }

    public void notifyUser(String msg) {
        Toast.makeText(context, msg, Toast.LENGTH_LONG).show();
    }

    /**
     * NAOLocationListener
     */

    @Override
    public void onLocationChanged(Location location) {
        ((MainActivity) context).onChange(location);
    }

    @Override
    public void onLocationStatusChanged(TNAOFIXSTATUS tnaofixstatus) {
        notifyUser(tnaofixstatus.toString());
    }

    @Override
    public void onEnterSite(String s) {
        notifyUser(s);
    }

    @Override
    public void onExitSite(String s) {
        notifyUser(s);
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
