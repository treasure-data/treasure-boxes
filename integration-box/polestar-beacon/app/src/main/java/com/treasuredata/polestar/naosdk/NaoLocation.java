package com.treasuredata.polestar.naosdk;

import android.location.Location;

import com.polestar.naosdk.api.external.NAOERRORCODE;
import com.polestar.naosdk.api.external.NAOLocationHandle;
import com.polestar.naosdk.api.external.NAOLocationListener;
import com.polestar.naosdk.api.external.TNAOFIXSTATUS;
import com.treasuredata.polestar.MainActivity;

public class NaoLocation extends AbstractClient<NAOLocationHandle> implements NAOLocationListener {

    @Override
    protected void createHandle() {
        setHandle(new NAOLocationHandle(getContext(), MyNaoService.class, getApiKey(), this, this));
    }

    /**
     * NAOLocationListener
     */

    @Override
    public void onLocationChanged(Location location) {
        // notify current location to the main activity
        ((MainActivity) getContext()).onLocationChanged(location);
    }

    @Override
    public void onLocationStatusChanged(TNAOFIXSTATUS tnaofixstatus) {
        showToast(tnaofixstatus.toString());
    }

    @Override
    public void onEnterSite(String s) {
        showToast(s);
    }

    @Override
    public void onExitSite(String s) {
        showToast(s);
    }

    /**
     * NAOErrorListener
     */

    @Override
    public void onError(NAOERRORCODE naoerrorcode, String msg) {
        showToast(msg);
    }

}
