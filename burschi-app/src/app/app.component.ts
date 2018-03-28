import { Component, ViewChild } from '@angular/core';
import { Http, Response } from '@angular/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
    @ViewChild('d3Component') d3Component;
    title = 'app';
    data;
    constructor( private http:Http) {
        this.http.get('./assets/burschis.json')
                 .subscribe( response =>  {
                     this.data = response.json();
                     this.setGraphData();
                 });
    }

    setGraphData() {
        let graphData = {
            nodes: [],
            links: []
        };
        let nodes = {}
        let index = 0;
        this.data.forEach( (burschi) => {
            burschi['id'] = index;
            index +=1;
            burschi['group'] = 0;
            let baseUrl = this.getBase(burschi['web_link']);
            console.log(baseUrl);
            console.log(burschi['web_link']);
            nodes[baseUrl] = burschi;
        });
        this.data.forEach( (burschi) => {
            burschi['external_links'].forEach( link => {
                let linkBase = this.getBase(link['link']);
                let graphLink = {};
                graphLink['source'] = burschi['id'];
                graphLink['count'] = link['count'];
                if( !(linkBase in nodes) ){
                    let extNode = {};
                    extNode['web_link'] = link['link'];
                    extNode['id'] = index;
                    extNode['group'] = 1;
                    extNode['in_degree'] = 0;
                    extNode['base_link'] = this.getBaseLink(link['link']);
                    index += 1;
                    nodes[linkBase] = extNode;
                }
                graphLink['target'] = nodes[linkBase]['id'];
                let existingLink = graphData.links.filter( link => {
                    return (link['source'] == graphLink['source']
                        && link['target'] == graphLink['target']);
                })
                if( existingLink.length > 0) {
                    existingLink['count'] += graphLink['count'];
                } else {
                    if(nodes[linkBase]['group'] == 1) {
                        nodes[linkBase]['in_degree'] += 1;
                    }
                    graphData.links.push(graphLink);
                }
            })
        })

        for( let key in nodes) {
            graphData.nodes.push(nodes[key]);
        }

        let invalidNodeIds = new Set();
        graphData.nodes = graphData.nodes.filter( node => {
            if ( node['group'] == 0) {
                return node;
            } else if( node['in_degree'] >= 2) {
                return node;
            } else {
                invalidNodeIds.add(node['id']);
            }
        });
        graphData.links = graphData.links.filter( link => {
            if( !invalidNodeIds.has(link['target'])) {
                return link;
            }
        }) 
        console.log("Calculation of GraphData completed...");
        this.d3Component.graphData = graphData;
        this.d3Component.render();
    }

    getBase( url:string) {
        let baseUrl = url;
        let httpLoc = baseUrl.indexOf("http://");
        let httpsLoc = baseUrl.indexOf("https://");
        if( httpLoc >= 0) {
            baseUrl = baseUrl.slice(httpLoc + 7);
        } else if( httpsLoc >= 0) {
            baseUrl = baseUrl.slice(httpsLoc + 8);
        }
        let slashLoc = baseUrl.indexOf("/");
        if( slashLoc >= 0) {
            baseUrl = baseUrl.slice(0,slashLoc);
        }
        let lastDotLoc = baseUrl.lastIndexOf(".");
        if( lastDotLoc >= 0) {
            baseUrl = baseUrl.slice(0,lastDotLoc);
        }
        lastDotLoc = baseUrl.lastIndexOf(".");
        if( lastDotLoc >= 0) {
            baseUrl = baseUrl.slice(lastDotLoc + 1);
        }
        return baseUrl;
    }

    getBaseLink( url:string) {
        let baseUrl = url;
        let httpLoc = baseUrl.indexOf("http://");
        let httpsLoc = baseUrl.indexOf("https://");
        if( httpLoc >= 0) {
            baseUrl = baseUrl.slice(httpLoc + 7);
        } else if( httpsLoc >= 0) {
            baseUrl = baseUrl.slice(httpsLoc + 8);
        }
        let slashLoc = baseUrl.indexOf("/");
        if( slashLoc >= 0) {
            baseUrl = baseUrl.slice(0,slashLoc);
        }
        return baseUrl;
    }

}
