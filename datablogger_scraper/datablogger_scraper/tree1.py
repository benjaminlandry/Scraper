from treelib import Node, Tree
tree = Tree()
parent1 = "Harry"
tree.create_node("Harry", "Harry")  # root node
tree.create_node("Jane", "Jane", parent="Harry")
tree.create_node("Bill", "Bill", parent="Harry")
tree.create_node("Diane", "Diane", parent="Jane")
tree.show()

def loop_links(self, links, parent_link):
    # set parent of a node e.g.(link) to the variable parent_link
    for link in links: ### HERE ###
        try:
            print('PARENT_LINK_A', parent_link)  ### HERE produces correct parent_link value

            data = [link, absolute_url]
            print("NODE_TREE", self.tree.create_node(link, link, parent=parent_link, data=data)) ### HERE does NOT produces correct parent_link value | issue is create_node function.

        time.sleep(1)


def start_requests(self):
        self.tree = Tree()
        parent_link = self.start_urls[0].replace("http://142.133.174.148:8888/", "")
        self.tree.create_node(parent_link, parent_link)
        yield scrapy.Request(self.start_urls[0], callback=self.parse, dont_filter=True)
        
    # Method for parsing items
    def parse(self, response):
        if(self.method_index == True):
            self.start_requests()
            self.method_index = False 
        
        parent_link = response.url
        parent_link = parent_link.replace("http://142.133.174.148:8888/", "")
        print(parent_link)

        # Fetch the html from the given url
        with urllib.request.urlopen(response.url) as response:
            current_page = response.read().decode('utf-8')
  
            links = regex_response.xpath('//div[@class="work_area_content"]/a/@href')
            loop_links(links, parent_link)




