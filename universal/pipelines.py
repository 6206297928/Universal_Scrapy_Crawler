import json


class UniversalPipeline:

    def open_spider(self, spider):

        self.file = open("output.json", "w")

        self.data = []


    def process_item(self, item, spider):

        self.data.append(dict(item))

        return item


    def close_spider(self, spider):

        json.dump(self.data, self.file, indent=2)

        self.file.close()

        print("\nSaved output.json")
