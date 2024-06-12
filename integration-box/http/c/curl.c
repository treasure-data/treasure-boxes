#include <curl/curl.h>
#include <stdlib.h>
#include <strings.h>

int main(int argc, char *argv[])
{
  CURLcode ret;
  CURL *hnd;
  struct curl_slist *slist1;

  if (argc != 6) {
      fprintf(stderr, "usage: %s <endpoint> <apikey> <database> <table>\n", argv[0]);
  }

  /* c360-ingest-api endpoint; ex. "c360-ingest-api.treasuredata.com" */
  char *endpoint = argv[1];
  /* Treasure Data apikey; ex. "1234/0123456789abcdef0123456789abcdef01234567 */
  char *apikey = argv[2];
  /* Treasure Data database name; pattern: [0-9a-z_]{3,128} */
  char *database = argv[3];
  /* Treasure Data table name; pattern: [0-9a-z_]{3,128} */
  char *table = argv[4];
  /* payload:
   *   {
   *     "events": [
   *       {"key": "value", ...},
   *       ...
   *     ]
   *   }
   */
  char *curlopt_postfields = argv[5];

  char curlopt_url[1024];
  {
      int r = snprintf(curlopt_url, sizeof(curlopt_url), "https://%s/%s/%s", endpoint, database, table);
      if (r <= 0 || 1000 < r) {
          fprintf(stderr, "failed to format curlopt_url\n");
          exit(1);
      }
  }

  char authrization[128];
  {
      int r = snprintf(authrization, sizeof(authrization), "Authorization: TD1 %s", apikey);
      if (r <= 0 || 100 < r) {
          fprintf(stderr, "failed to format Authorization\n");
          exit(1);
      }
  }

  slist1 = NULL;
  slist1 = curl_slist_append(slist1, "Content-Type: application/vnd.treasuredata.v1+json");
  slist1 = curl_slist_append(slist1, "Accept: application/vnd.treasuredata.v1+json");
  slist1 = curl_slist_append(slist1, authrization);

  hnd = curl_easy_init();
  curl_easy_setopt(hnd, CURLOPT_URL, curlopt_url);
  curl_easy_setopt(hnd, CURLOPT_NOPROGRESS, 1L);
  curl_easy_setopt(hnd, CURLOPT_POSTFIELDS, curlopt_postfields);
  curl_easy_setopt(hnd, CURLOPT_POSTFIELDSIZE_LARGE, (curl_off_t)strlen(curlopt_postfields));
  curl_easy_setopt(hnd, CURLOPT_USERAGENT, "curl/7.54.0");
  curl_easy_setopt(hnd, CURLOPT_HTTPHEADER, slist1);
  curl_easy_setopt(hnd, CURLOPT_MAXREDIRS, 50L);
  curl_easy_setopt(hnd, CURLOPT_HTTP_VERSION, (long)CURL_HTTP_VERSION_2TLS);
  curl_easy_setopt(hnd, CURLOPT_TCP_KEEPALIVE, 1L);

  /* Here is a list of options the curl code used that cannot get generated
     as source easily. You may select to either not use them or implement
     them yourself.

  CURLOPT_WRITEDATA set to a objectpointer
  CURLOPT_INTERLEAVEDATA set to a objectpointer
  CURLOPT_WRITEFUNCTION set to a functionpointer
  CURLOPT_READDATA set to a objectpointer
  CURLOPT_READFUNCTION set to a functionpointer
  CURLOPT_SEEKDATA set to a objectpointer
  CURLOPT_SEEKFUNCTION set to a functionpointer
  CURLOPT_ERRORBUFFER set to a objectpointer
  CURLOPT_STDERR set to a objectpointer
  CURLOPT_HEADERFUNCTION set to a functionpointer
  CURLOPT_HEADERDATA set to a objectpointer

  */

  ret = curl_easy_perform(hnd);

  curl_easy_cleanup(hnd);
  hnd = NULL;
  curl_slist_free_all(slist1);
  slist1 = NULL;

  return (int)ret;
}
/**** End of sample code ****/
