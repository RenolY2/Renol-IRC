import urllib2
import traceback

from urllib import quote

from commands.miscLib.xml_to_dict import xml_to_dict

ID = "wolfram"
permission = 2


def execute(self, name, params, channel, userdata, rank):
    request = " ".join(params)
    request = request.strip()

    if len(request) > 1:
        try:
            result = self.WolframAlpha.submit(request)#.decode("utf-8", "replace")
            xmldict = xml_to_dict(result, encoding="utf-8")


            if "pod" not in xmldict["queryresult"]:
                self.sendMessage(channel, "Error: Wolfram did not return any results")
                return

            pod = xmldict["queryresult"]["pod"]
            print pod

            for item in pod:
                if item["@id"] == "Input":
                    continue

                if "subpod" in item and "plaintext" in item["subpod"]:
                    result = item["subpod"]["plaintext"]

                    if result is not None:
                        description = item["@title"]
                        result = result.strip("| ")
                        result = result.replace(" | ", ": ")
                        result = " | ".join(result.split("\n"))

                        self.sendMessage(channel, u"{0}: {1}".format(description, result))
                        break
            """
            #for item in pod:
            with pod[0] as item:
                description = item["@title"]#.decode("utf-8")
                #print item
                #print item["subpod"]
                if not isinstance(item["subpod"], list):
                    result = item["subpod"]["plaintext"]

                    if result != None:
                        #result = result.decode("utf-8", "replace")
                        result = result.strip("| ")
                        result = result.replace(" | ", ": ")
                        result = " | ".join(result.split("\n"))


                        self.sendMessage(channel, u"{0}: {1}".format(description, result))
                else:
                    entries = []
                    for subpod in item["subpod"]:
                        result = subpod["plaintext"]

                        if result != None:
                            #result = result.decode("utf-8", "replace")
                            result = result.strip("| ")
                            result = result.replace(" | ", ": ")
                            result = " | ".join(result.split("\n"))

                            entries.append(result)

                    self.sendMessage(channel, u"{0}: {1}".format(description, " | ".join(entries)))
            """

        except Exception as error:
            self.sendMessage(channel, "Error appeared: {0}".format(str(error)))
