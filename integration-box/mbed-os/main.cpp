#include "mbed.h"
#include "https_request.h"

#define URL_SIZE 100
#define BUFF_SIZE 100

/* Amazon Server CA retrieved by:
 * $ openssl s_client -showcerts -connect in.treasuredata.com:443
 */
const char SSL_CA_PEM[] = "-----BEGIN CERTIFICATE-----\n"
  "MIIEdTCCA12gAwIBAgIJAKcOSkw0grd/MA0GCSqGSIb3DQEBCwUAMGgxCzAJBgNV\n"
  "BAYTAlVTMSUwIwYDVQQKExxTdGFyZmllbGQgVGVjaG5vbG9naWVzLCBJbmMuMTIw\n"
  "MAYDVQQLEylTdGFyZmllbGQgQ2xhc3MgMiBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0\n"
  "eTAeFw0wOTA5MDIwMDAwMDBaFw0zNDA2MjgxNzM5MTZaMIGYMQswCQYDVQQGEwJV\n"
  "UzEQMA4GA1UECBMHQXJpem9uYTETMBEGA1UEBxMKU2NvdHRzZGFsZTElMCMGA1UE\n"
  "ChMcU3RhcmZpZWxkIFRlY2hub2xvZ2llcywgSW5jLjE7MDkGA1UEAxMyU3RhcmZp\n"
  "ZWxkIFNlcnZpY2VzIFJvb3QgQ2VydGlmaWNhdGUgQXV0aG9yaXR5IC0gRzIwggEi\n"
  "MA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDVDDrEKvlO4vW+GZdfjohTsR8/\n"
  "y8+fIBNtKTrID30892t2OGPZNmCom15cAICyL1l/9of5JUOG52kbUpqQ4XHj2C0N\n"
  "Tm/2yEnZtvMaVq4rtnQU68/7JuMauh2WLmo7WJSJR1b/JaCTcFOD2oR0FMNnngRo\n"
  "Ot+OQFodSk7PQ5E751bWAHDLUu57fa4657wx+UX2wmDPE1kCK4DMNEffud6QZW0C\n"
  "zyyRpqbn3oUYSXxmTqM6bam17jQuug0DuDPfR+uxa40l2ZvOgdFFRjKWcIfeAg5J\n"
  "Q4W2bHO7ZOphQazJ1FTfhy/HIrImzJ9ZVGif/L4qL8RVHHVAYBeFAlU5i38FAgMB\n"
  "AAGjgfAwge0wDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMCAYYwHQYDVR0O\n"
  "BBYEFJxfAN+qAdcwKziIorhtSpzyEZGDMB8GA1UdIwQYMBaAFL9ft9HO3R+G9FtV\n"
  "rNzXEMIOqYjnME8GCCsGAQUFBwEBBEMwQTAcBggrBgEFBQcwAYYQaHR0cDovL28u\n"
  "c3MyLnVzLzAhBggrBgEFBQcwAoYVaHR0cDovL3guc3MyLnVzL3guY2VyMCYGA1Ud\n"
  "HwQfMB0wG6AZoBeGFWh0dHA6Ly9zLnNzMi51cy9yLmNybDARBgNVHSAECjAIMAYG\n"
  "BFUdIAAwDQYJKoZIhvcNAQELBQADggEBACMd44pXyn3pF3lM8R5V/cxTbj5HD9/G\n"
  "VfKyBDbtgB9TxF00KGu+x1X8Z+rLP3+QsjPNG1gQggL4+C/1E2DUBc7xgQjB3ad1\n"
  "l08YuW3e95ORCLp+QCztweq7dp4zBncdDQh/U90bZKuCJ/Fp1U1ervShw3WnWEQt\n"
  "8jxwmKy6abaVd38PMV4s/KCHOkdp8Hlf9BRUpJVeEXgSYCfOn8J3/yNTd126/+pZ\n"
  "59vPr5KW7ySaNRB6nJHGDn2Z9j8Z3/VyVOEVqQdZe4O/Ui5GjLIAZHYcSNPYeehu\n"
  "VsyuLAOQ1xk4meTKCRlb/weWsKh/NEnfVqn3sF/tM+2MR7cwA130A4w=\n"
  "-----END CERTIFICATE-----\n";

int main (void) {
  printf("\nTreasure Boxes (Integration): Mbed OS + Treasure Data\n");

  NetworkInterface *net = NetworkInterface::get_default_instance();
  if (net->connect() != NSAPI_ERROR_OK) {
    printf("Cannot connect to the network.\n");
    return 1;
  }
  printf("Connected to the network successfully.\n\n");

  printf("MAC: %s\n", net->get_mac_address());
  printf("IP: %s\n", net->get_ip_address());
  printf("Netmask: %s\n", net->get_netmask());
  printf("Gateway: %s\n", net->get_gateway());

  char url[URL_SIZE];
  sprintf(url, "https://in.treasuredata.com/postback/v3/event/%s/%s", MBED_CONF_APP_TD_DATABASE, MBED_CONF_APP_TD_TABLE);
  printf("\nSending POST request to: %s\n\n", url);

  mbed_stats_heap_t heapinfo; // device information object
  char body[BUFF_SIZE] = {0};
  while (1) {
    mbed_stats_heap_get(&heapinfo); // collect current heap information

    sprintf(body, "{\"current_size\":%ld,\"max_size\":%ld,\"total_size\":%ld,\"reserved_size\":%ld,\"alloc_cnt\":%ld,\"alloc_fail_cnt\":%ld}",
                  heapinfo.current_size,
                  heapinfo.max_size,
                  heapinfo.total_size,
                  heapinfo.reserved_size,
                  heapinfo.alloc_cnt,
                  heapinfo.alloc_fail_cnt);

    printf("Data: %s\n", body);

    HttpsRequest *req = new HttpsRequest(net, SSL_CA_PEM, HTTP_POST, url);
    req->set_header("Content-Type", "application/json");
    req->set_header("X-TD-Write-Key", MBED_CONF_APP_TD_APIKEY);

    HttpResponse *res = req->send(body, strlen(body));
    if (!res) {
      printf("HttpRequest failed with error code: %d.\n", req->get_error());
      return 1;
    }
    printf("Response code: %d\n", res->get_status_code());

    delete req;

    wait(10);
  }

  net->disconnect();
}
