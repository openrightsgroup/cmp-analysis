
Opencharities data processing

The opencharities_source_list.tsv was turned into a URL list for import by
using:

awk -F'\t' '{ print $3 }' < opencharities_source_list.tsv > import_list.txt

While the tests were running, the source list had geographical information
(County, Constituency, Council) added by using the postcode.py script.

postcode.py parses the address field looking for postcode formatted data, then
does a lookup against uk-postcodes.com's API.  Results are locally cached in a
file managed by the script.

Since county/council/constituency are unlikely to very much inside a postcode
sector, the information is cached at that level.

Finally, the merge_results.py script takes the geographical file and the test
results summary and merges them using the URL as the key.

The final files are:

opencharities_merged_results.tsv
opencharities_merged_results.ods

It's all very rough around the edges at the point.  The API's URL normalization
routine sometimes causes a mismatch between the source list URL and the API
results URL.  I'm sure there are many improvements that can be made!

Daniel.
