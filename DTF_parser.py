import json


class EntryParser:
    def parse_entry(self, json_entry, comments = {}):
        result = {'id': json_entry['id']}
        result['title'] = json_entry['title']
        result['intro'] = json_entry['intro']
        for block in json_entry['blocks']:
            if block['type'] == 'list':
                result['list'] += self.__list_parser__(block)
            elif block['type'] == 'link':
                result += self.link_parser__(block)
        result['comments_id'] = comments
        return result

    def __list_parser__(self, text_parser):
        if type['type'] != 'list':
            return None
        result = []
        items = text_parser['data']['items']
        for item in items:
            result.append(item)
        return result

    def link_parser__(self, link_json):
        if type['type'] != 'link':
            return None
        keys = ['url', 'title', 'descrition'] 
        content = dict()
        data = link_json['data']
        for key in keys:
            if key in data:
                content[key] = data[key]
        return content


    

