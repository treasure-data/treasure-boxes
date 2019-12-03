package com.treasuredata.polestar;

import com.polestar.naosdk.api.external.NAOERRORCODE;
import com.polestar.naosdk.api.external.NAOGeofenceListener;
import com.polestar.naosdk.api.external.NAOGeofencingHandle;
import com.polestar.naosdk.api.external.NaoAlert;

public class NaoGeofencingClient extends AbstractClient<NAOGeofencingHandle> implements NAOGeofenceListener {

    @Override
    protected NAOGeofencingHandle createHandle() {
        return new NAOGeofencingHandle(getContext(), MyNaoService.class, getNaoServiceApiKey(), this, this);
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

}
