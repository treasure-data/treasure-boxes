package com.treasuredata.polestar;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import com.treasuredata.android.TreasureData;

public class MainActivity extends AppCompatActivity {
    final private static String TD_WRITE_KEY = "1/234567890abcdefghijklmnopqrstuvwxyz";
    final private static String TD_ENCRYPTION_KEY = "1234567890";

    private TreasureData td;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initTreasureData();
    }

    private void initTreasureData() {
        // @see https://docs.treasuredata.com/articles/android-sdk
        TreasureData.initializeApiEndpoint("https://in.treasuredata.com");
        TreasureData.initializeEncryptionKey(TD_ENCRYPTION_KEY);
        TreasureData.disableLogging();
        TreasureData.initializeSharedInstance(this, TD_WRITE_KEY);

        TreasureData td = TreasureData.sharedInstance();

        td.setDefaultDatabase("polestar");
        td.enableAutoAppendUniqId();
        td.enableAutoAppendModelInformation();
        td.enableAutoAppendAppInformation();
        td.enableAutoAppendLocaleInformation();

        this.td = td;
    }
}
