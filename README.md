# burschi
Visually displayed data of german burschenschaften

## Frontend Description
The burschi frontend consists of an [angular.io](https://angular.io/) module.
The javascript library [d3js](https://d3js.org/) is used for the network visualisation.

### Data Aggregation
[burschis.json](/burschi-app/src/assets/burschis.json) is created by [main.py](/main.py) and contains a list of burschenschaft dictionaries with the following information:

```json
[
  {
    "name": "<name of the burschenschaft>",
    "web_link": "<url of the burschenschaft>",
    "external_links": [
      {
        "link":"<external url at this burschenschafts website>",
        "count": 9
      },
      {},
      {}
    ]
  },
  {},
  {}
]
```
`"count"`: number of times the link exists on the whole website

After creating a javascript list containing this data, the network graph data is created by:

1. Iterating through each dictionary and creating a **node** object for each burschenschaft and saving:

        let node = {
          'id':1, //unique id for each node
          'group':0,
          'name': 'foo',
          'web_link': 'http://foo-website.de',
          'external_links':[{...},{...}]
        }


2. Adding each node to a **nodes** dictionary, using the urls base as its key:

        let nodes = {
          'foo-website': {...},
          'bar-website': {...}
        }


3. Iterating through all **external_links** inside each dictionary and creating a **link** object for each of them:

        let link = {
          'source': 1, //the id value of the parent burschenschaft node
          'count': 3,
          'target': 9, // the id of this external node 
        }
    This link is added to a list of **links**


4. If the external node identified by its url base is not found in **nodes**, its created before the links `'target':9` key/value pair is added:

        let externalNode = {
          'id':9, //same unique id space as burschenschaft nodes
          'group':1,
          'web_link': 'http://foo-website.de',
          'base_link': 'www.wikipedia.de', //base link, unlike base, contains at least the websites tld
          'in_degree': 0 //used to identify number of burschenschaft nodes linking to this external one
        }
    This node is also added to the **nodes** dictionary with using the web_links base as a key.


5. The `'in_degree'` of the target node is incremented by 1. 

6. The Value of each key in **nodes={}** is added to the list **nodes=[]**

7. All nodes having an `'in_degree'` of just 1 are removed from this list. This is done to reduce the complexity of the resulting network graph.

8. All links connected to the removed nodes are also deleted.

9. The resulting **graphData** dictionary, containing the **nodes** list and **links** list is added to the [d3Component](/burschi-app/src/app/d3.component.ts).

### Data Visualisation

The [d3Component](/burschi-app/src/app/d3.component.ts) is rendering the nodes and links by drawing them to a **HTML5 Canvas**.

#### Simulation

The simulation creating the network-structure uses these forces:

* `.forceLink()`: Connecting each link to a node by its `'source:'` and `'target:'` values and connected nodes are attracting each other.
* `.forceManyBody()`: All nodes are repelling each other.
* `.forceCollide()`: Nodes are not repelling all the nodes in an area of their radius. This prevents nodes from overlapping each other
* `.forceCenter()`: All nodes are attracted to the center of the canvas.

For an in depth api reference visit [d3js at github](https://github.com/d3/d3/blob/master/API.md)
