from treelib import Node, Tree
tree = Tree()
tree.create_node("Harry", "Harry")  # root node
tree.create_node("Jane", "Jane", parent="Harry")
tree.create_node("Bill", "Bill", parent="Harry")
tree.create_node("Diane", "Diane", parent="Jane")
tree.show()

#params: start_urls | links | link | absolute_url

# tree.create_node(start_urls)


# parent_link = response.meta.link

# for link in links:
#     absolute_url = absolute_url
#     link = link

#     data = [link, absolute_url]
#     if(link != null)
#         tree.create_node(link, link, parent_link, data)

#         requests(absolute_url, meta = link)
