LDA topic modeling template
===

This workflow shows an example how to apply [LDA](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)-based [topic modeling](https://en.wikipedia.org/wiki/Topic_model) which often be used for document clustering.

## Input

This workflow takes a table of the following form:

| docid<br/>`long` | contents `string` |
|---:|:---|
|2238|A red oak tree a few miles down the road from Terry A. Andersons ...|
|2240|A veteran jockey who had planned to retire at the end of the year ...|
|2241|The bloodiest of four army uprisings in four years was also the ...|
| ... |...|...|

You can used `$ bin/load_data.sh` to prepare the above example table on Treasure data.

The input table of LDA training will be as follows:

| docid | features |
|-:|:-|
| 1936 | List [ "africa:3", "altar:2", "arrived:2", "bus:3", "carrying:2", "country:2", "crowd:2", "day:2", "five:2", "gate:2", "god:2", "hijackers:4", "hijacking:2", "hour:2", "ii:4", "including:2", "injured:2", "john:6", "king:8", "lesotho:5", "mass:3", "mozambique:2", "mswati:3", "only one:2", "paul:6", "people:4", "platform:2", "police:2", "pope:7", "popes:2", "queen:2", "rally:2", "red:2", "slipped:2", "soldiers:2", "south:2", "southern:2", "spear:3", "stadium:4", "stop:2", "stormed:2", "swaziland:3", "thursday:3", "told:3", "unscheduled:2", "vatican:2", "visit:2", "war:2", "warriors:2", "weather:2", "wife:2", "wives:2" ]
| 1555 | List [ "army:2", "baltic:2", "candidates:3", "coalition:2", "communist:5", "communists:6", "dapkus:2", "december:2", "decided:3", "democrats:2", "dominated:2", "election:4", "elections:2", "front:2", "gathered:2", "goal:3", "independence:5", "independents:2", "landsbergis:3", "landslide:2", "leader:2", "led:2", "lithuania:9", "lithuanian:3", "lithuanias:2", "main:2", "moscow:4", "movement:3", "parliament:5", "parties:2", "party:6", "popular:2", "probably:2", "races:2", "red:2", "reform:4", "reformed:2", "republics:3", "results:3", "rule:2", "sajudis:17", "seats:4", "secession:2", "six:2", "soviet:9", "sunday:3", "turnout:2", "union:5", "victory:2", "voters:2", "voting:2", "winners:2", "won:4" ]
| 2145 | List [ "angeles:2", "beach:2", "beaches:2", "brush:2", "center:2", "continues:2", "county:2", "crops:3", "day:2", "degrees:2", "desert:3", "district:3", "downtown:2", "dropped:2", "fruits:2", "grower:2", "heat:6", "heat wave:2", "hillbrecht:3", "hundreds:2", "inland:2", "los:2", "past:2", "people:2", "record:3", "reported:2", "restrictions:2", "san:4", "santa:2", "six:2", "temperatures:2", "thousands:2", "threatened:2", "time:2", "valley:2", "water:7", "weather:2", "wont:2" ]
| 36 | List [ "brought:2", "cambridge:3", "city:2", "costa:2", "cristiani:3", "dozens:2", "el:4", "flores:2", "harvard:4", "jose:2", "las:2", "letter:2", "letters:2", "military:4", "outside:2", "president:2", "protesters:3", "salvador:2", "salvadoran:2", "san:2", "sister:3", "son:2", "squash:2", "wolf:2" ]
| 977 | List [ "begin:3", "economic:2", "historic:2", "israel:7", "israeli:4", "israels:2", "kavanau:3", "military:2", "minister:2", "peace:3", "pierre:2", "prime:2", "report:4", "rinfret:6", "rinfrets:2", "sadat:6", "sadats:2", "secret:2", "service:2", "vance:3", "visit:3" ]
| 1832 | List [ "angelo:2", "bentsen:14", "center:2", "conservative:2", "county:2", "democratic:2", "democrats:3", "dont:2", "dukakis:5", "election:2", "financial:2", "fort:2", "health:2", "lloyd:2", "lubbock:2", "medical:2", "pitch:2", "private:2", "quayle:2", "records:2", "reporters:2", "republican:3", "running:2", "san:2", "seat:2", "senate:4", "senator:2", "support:2", "supporters:3", "television:2", "texas:4", "ticket:4", "time:2", "told:3", "traveled:3", "tyler:2", "vote:2", "votes:2", "win:2", "worth:4" ]
| 1301 | List [ "city:3", "mayor:3", "paolino:2" ] |
| .. | .. |

## Workflow

```sh
# push workflow to TD
$ td wf push lda_wf

# run workflow
$ td wf start lda_wf lda --session now
```
  
## Output

The output of workflow consists of the following three tables:

`lda_model` table stores model parameter of LDA. `lambda` 

| label | word | lambda |
|---:|---:|---:|
| 5 | eritrean | 7.959341132846021e-07 |
| 5 | altovise | 7.959536105772713e-07 |
| 5 | governmed | 7.959557137837692e-07 |
| .. | .. | .. |

`predicted_topics` table shows assigned topic(s) for each document. 
`proba1`/`proba2` represents probability be `topic1`/`topic2`, respectively. 
`topic1` is the topic id that a document is most likely to be described. `topic2` can be null when there is no second topic candidate.

| docid | topic1 | proba1 | topic2 | proba2 |
|---:|---:|---:|---:|---:|
| 5 | 6 | 0.1428571492433548 | | |
| 6 | 0 | 0.1478169709444046 | 6 | 0.1420305073261261 |
| 7 | 6 | 0.1428571492433548 | | |
| 8 | 6 | 0.1428571492433548 | | |

`topicwords` shows topic-describing words for each topic.

| topic | words |
|:-:|:--|
| 0 | [ "museum", "art", "short", "museums", "tomb", "black", "n___", "divorce", ... ] |
| 1 | [ "band", "recording", "poet", "album", "charles", "nea", "fulton", "rjr", ... ] |
| 2 | [ "family", "gallery", "friends", "the dog", "nixon", "art", "door", "monet", ... ] |
| 3 | [ "people", "government", "president", "officials", "police", "united", ... ] |
| 4 | [ "percent", "market", "million", "stock", "billion", "prices", "rose", ... ] |
| 5 | [ "billboard", "test", "fda", "transplant", "trailer", "patients", "surgery", ... ] |
| 6 | [ "maxwell", "shark", "randolph", "comedy", "opera", "dunn", "sang", "historic", ... ] |


## Conclusion

Treasure Workflow provides an easy way to apply document clustering using LDA. 
What you need to prepare is just an input table.

Note that you can find stopwords in various languages in [PostgreSQL repository](https://github.com/postgres/postgres/tree/master/src/backend/snowball/stopwords).
Better to replace [stopwords.csv](.resources/stopwords.csv) for non-English texts.

[Contact us](https://www.treasuredata.com/contact_us) if you interested in [our paid consulting service](https://docs.treasuredata.com/display/public/PD/Consultation).
