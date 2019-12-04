package com.treasuredata.polestar.naosdk;

import com.polestar.naosdk.api.external.NAOERRORCODE;
import com.polestar.naosdk.api.external.NAOGeofenceListener;
import com.polestar.naosdk.api.external.NAOGeofencingHandle;
import com.polestar.naosdk.api.external.NaoAlert;

public class NaoGeofencing extends AbstractClient<NAOGeofencingHandle> implements NAOGeofenceListener {

    @Override
    protected void createHandle() {
        setHandle(new NAOGeofencingHandle(getContext(), MyNaoService.class, getApiKey(), this, this));
    }

    /**
     * NAOGeofencingListener
     */

    @Override
    public void onFireNaoAlert(NaoAlert alert) {
        showNotification(alert.getName(), alert.getContent());
    }

    /**
     * NAOGeofenceListener
     */

    @Override
    public void onEnterGeofence(int regionId, String regionName) {
        showToast("Enter region " + regionId + "(" + regionName + ")");
    }

    @Override
    public void onExitGeofence(int regionId, String regionName) {
        showToast("Exit region " + regionId + "(" + regionName + ")");
    }

    /**
     * NAOErrorListener
     */

    @Override
    public void onError(NAOERRORCODE naoerrorcode, String msg) {
        showToast(msg);
    }

}
