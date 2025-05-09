import innertube

def print_results(search_data) -> str:
    """Print search results, then return the continuation token"""

    if "contents" in search_data:
        # This is the first batch of results
        item_section, continuation_item = search_data["contents"][
            "twoColumnSearchResultsRenderer"
        ]["primaryContents"]["sectionListRenderer"]["contents"]
    elif "onResponseReceivedCommands" in search_data:
        # This is a continuation
        item_section, continuation_item = search_data["onResponseReceivedCommands"][0][
            "appendContinuationItemsAction"
        ]["continuationItems"]
    else:
        raise Exception("Failed to parse search data")

    results = item_section["itemSectionRenderer"]["contents"]

    for result in results:
        result_type = next(iter(result))
        result_data = result[result_type]

        if result_type == "channelRenderer":
            print("Channel -", result_data["title"]["simpleText"])
        elif result_type == "playlistRenderer":
            print("Playlist -", result_data["title"]["simpleText"])
        elif result_type == "radioRenderer":
            print("Radio -", result_data["title"]["simpleText"])
        elif result_type == "reelShelfRenderer":
            print("Reel Shelf -", result_data["title"]["simpleText"])
        elif result_type == "shelfRenderer":
            print("Shelf -", result_data["title"]["simpleText"])
        elif result_type == "videoRenderer":
            print("Video -", result_data["title"]["runs"][0]["text"])
        else:
            print(f"{result_type} - ???")

    continuation_token = continuation_item["continuationItemRenderer"][
        "continuationEndpoint"
    ]["continuationCommand"]["token"]

    return continuation_token

# Construct a client
client = innertube.InnerTube("WEB")
# Get some data!
data = client.search(query="Liverpool Soccer")
# Power user? No problem, dispatch requests yourself
# data = client("browse", body={"browseId": "FEwhat_to_watch"})
# The core endpoints are implemented, so the above is equivalent to:
#data = client.browse("FEwhat_to_watch")
print_results(data)