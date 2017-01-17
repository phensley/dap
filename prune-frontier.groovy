
pattern = "^https?://domain.com/.*"
count = job.crawlController.frontier.deleteURIs(".*", pattern)
rawOut.println count + " uris deleted from frontier"

