
// Set the regexp pattern for the URLs you want to delete from the frontier
pattern = "^https?://www.usace.army.mil/About/History/.*'
count = job.crawlController.frontier.deleteURIs(".*", pattern)
rawOut.println count + " uris deleted from frontier"

