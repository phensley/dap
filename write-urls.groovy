
// Write all URLs in the frontier into a text file.

import com.sleepycat.je.DatabaseEntry;
import com.sleepycat.je.OperationStatus;
 
pendingUris = job.crawlController.frontier.pendingUris
 
rawOut.println "(this seems to be more of a ceiling) pendingUris.pendingUrisDB.count()=" + pendingUris.pendingUrisDB.count()
rawOut.println()
 
// Set the output path for the list of URLs from the frontier
File file = new File("/data/crawl/epa-frontier.txt")
FileWriter out = new FileWriter(file, true)

cursor = pendingUris.pendingUrisDB.openCursor(null, null);
key = new DatabaseEntry();
value = new DatabaseEntry();
count = 0;
 
while (cursor.getNext(key, value, null) == OperationStatus.SUCCESS) {
    if (value.getData().length == 0) {
        continue;
    }
    curi = pendingUris.crawlUriBinding.entryToObject(value);
    //rawOut.println curi
    out.println curi
    count++
}
cursor.close();
out.flush()
out.close()

rawOut.println()
rawOut.println count + " pending urls listed"

