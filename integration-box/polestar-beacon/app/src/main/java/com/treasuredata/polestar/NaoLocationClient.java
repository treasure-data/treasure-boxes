package com.treasuredata.polestar;

import android.location.Location;

import com.polestar.naosdk.api.external.NAOERRORCODE;
import com.polestar.naosdk.api.external.NAOLocationHandle;
import com.polestar.naosdk.api.external.NAOLocationListener;
import com.polestar.naosdk.api.external.TNAOFIXSTATUS;

public class NaoLocationClient extends AbstractClient<NAOLocationHandle> implements NAOLocationListener {

    @Override
    protected NAOLocationHandle createHandle() {
        return new NAOLocationHandle(getContext(), MyNaoService.class, getNaoServiceApiKey(), this, this);
    }

    /**
     * NAOLocationListener
     */

    @Override
    public void onLocationChanged(Location location) {
        ((MainActivity) getContext()).onChange(location);
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

}
