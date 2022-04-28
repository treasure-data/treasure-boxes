# LINE User ID integration to Treasure-data. 
[LINE](https://line.me/ja/) is in Asia what Facebook Messaging and Instagram are to US mobile users—a fast and easy way to communicate with friends and to discover new promotions about your favorite products and services. LINE is the number one mobile messaging platform in Japan and Taiwan and is also one of the largest Ads delivery platforms. 

## Important Notes
This sample script ([line_uid_integration.txt](https://github.com/treasure-data/td-customers-code/blob/master/Line_uid_integration/line_uid_integration.txt)) is integrating LINE User ID to Treasure Data by TD JS SDK.  This script is not included in the implementation of LINE login and LIFF init process, because LINE login and LIFF code strongly depends on customer requirement and needs. The sample script specifies how to get LINE User ID and LINE Display Name by LIFF after LINE Login and send the data to Treasure Data with 1st party coookie(td_ssc_id). 

## Prerequisite
You should check the following and implement LINE Login on your web apps before using this sample script. You need LINE business account to login LINE Developer Console, and create LINE Channel and add LIFF apps for developing. 

- [Create LINE business ID and official account.](https://developers.line.biz/ja/docs/line-developers-console/login-account/#account-relationships)
- [Create LINE Login channel and set up.](https://developers.line.biz/ja/docs/line-login/getting-started/#step-1-create-channel)
- [Adding LIFF Apps to Channels.](https://developers.line.biz/ja/docs/liff/registering-liff-apps/#registering-liff-app)
- [Developing the LIFF application.](https://developers.line.biz/ja/docs/liff/developing-liff-apps/)
- [Understand TD JS SDK script.](https://github.com/treasure-data/td-js-sdk)

Please check security guideline and document of LINE Developer Console for implementing LINE Login and how you will give a privacy policy information to get LINE User ID. The following is the sample of privacy policy information. 

- [Developer's Guideline](https://developers.line.biz/ja/docs/line-login/development-guidelines/)
- [Security Check List](https://developers.line.biz/ja/docs/line-login/security-checklist/)
- [Build a secure login process between the app and the server](https://developers.line.biz/ja/docs/line-login/secure-login-process/)

The sample of privacy policy information for English 
```
LINE User ID Integration
1. Information to be collected from LINE
   LINE USER ID and LINE USER NAME will be obtained.
   LINE Corporation's user identifier (This is an internal identifier given independently by LINE Corporation, and is not an email address or phone number.

2. How to disconnect from LINE
   You can cancel the link by logging out of your LINE Login. 
   
3. How do I stop receiving messages?
   If you do not want to be notified of messages, you can change your settings by going to "Talk Settings => Notification Off". (You will not receive notifications, but you can still receive messages.
   If you do not want to receive messages, please change the setting by clicking [Talk Settings => Block].
```

The sample of privacy policy information for English for Japanese
```
LINEアカウント連携について
1. LINEから連携される情報について
    LINE USER ID,LINE USER NAMEを取得いたします。
    LINE（株）のユーザー識別子（LINE（株）が独自に付与した内部識別子で、メールアドレス、電話番号ではありません。）

2. 連携を解除方法について
    LINEログインからログアウトいただくことで連携解除が可能です。

3. メッセージ受信の停止について
    メッセージ通知が不要の場合、【トーク設定⇒通知をオフ】で設定の変更可能です。※通知はありませんが、受信はできます
    メッセージが不要の場合、【トーク設定⇒ブロック】で設定の変更ください。
```

## Parameter Configuration for sample script. 
|Param|Description|
|--|--|
| var sscDomains = {'ssc_domain':'ssc_server'} | Your ssc domain and ssc server. Ex) 'treasuredata.co.jp':'ssc'|
| host: 'in.treasuredata.com'| TD API endpoint. Please change tokyo.in.treasuredata.com if your CDP is in Japan.| writeKey: 'td write key'| Your TD Write API key for authentication |
| database: 'td database name'| Your td database name including target table.|
| var table = 'table name'| Your td table name to store LINE User ID and 1st Party cookie.|