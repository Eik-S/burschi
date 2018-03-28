import { Component } from '@angular/core';
import * as d3 from 'd3';
import * as $ from 'jquery';

@Component({
  selector: 'd3',
  templateUrl: './d3.component.html',
  styleUrls: ['./d3.component.scss']
})
export class D3Component {
    width;
    height;
    context;
    canvas;
    simulation;
    graphData = {
        nodes: [],
        links: []
    };

    hoveredNode;
    dragging;

    colors = ["151,41,255","29,161,242"]
    scale = d3.scaleLinear().domain([2, 30]).range([6, 18]);

    ticked() {
        let margin = 10;
        this.graphData.nodes.forEach( node => {
            let x = node.x;
            let y = node.y;
            let r = node.r;
            if( x < 0 + r + margin){
                node.x = 0 + r + margin;
            } else if ( x > this.width - (r + margin)) {
                node.x = this.width - (r + margin);
            }
            if( y < 0 + r + margin){
                node.y = 0 + r + margin;
            } else if ( y > this.height - (r + margin)) {
                node.y = this.height - (r + margin);
            }
        });

        this.context.clearRect(0, 0, this.width, this.height);
        this.context.beginPath();
        this.graphData.links.filter( link => {
            if( link.opacity == 1) {
                return link;
            }
        }).forEach( link => this.drawLink(link));
        this.context.stroke();

        this.context.beginPath();
        this.graphData.links.filter( link => {
            if( link.opacity == 0.2) {
                return link;
            }
        }).forEach( link => this.drawLink(link));
        this.context.stroke();

        this.context.beginPath();
        this.graphData.nodes.forEach(node => {
               this.drawNode(node);
        });
        this.graphData.nodes.forEach(node => {
            if( node.labeled) {
                this.drawNodeLabel(node);
            }
        })
    }

    resizeCanvas() {
        this.canvas.width = 0;
        this.canvas.height = 0;
        this.width = $('.canvas').width();
        this.height = $('.canvas').height();
        this.canvas = document.querySelector(".d3-graph");
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        this.context = this.canvas.getContext("2d");
        this.simulation.stop()
        this.startSimulation().then( (simulation) => {
            this.context.beginPath();
            this.simulation = simulation;
        });
    }

    render() {
        this.width = $('.canvas').width();
        this.height = $('.canvas').height();
        this.canvas = document.querySelector(".d3-graph");
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        this.context = this.canvas.getContext("2d");
        this.graphData.nodes.forEach( node => {
            node.r = this.scale(this.getNeighbours(node)) * 1.6;;
            node.opacity = 1.0;
        });
        this.graphData.links.forEach( link => {
            link.opacity = 1.0;
        });
        console.log(this.graphData.links.length);
        console.log(this.graphData.links[103]);
        console.log(this.graphData.nodes.filter( node => {return node.id == 27}))
        this.addTimestamps();
        this.startSimulation().then( (simulation) => {
            this.simulation = simulation;
            d3.select(this.canvas)
                .call( d3.drag()
                    .container(this.canvas)
                    .subject( () => { return nodeHovered(this.canvas)})
                    .on("start", () => { return this.dragstarted() })
                    .on("drag", () => { return this.dragged()})
                    .on("end", () => { return this.dragended()}));
            d3.select(this.canvas)
                .on("mousemove", () => {
                    let node = nodeHovered(this.canvas);
                    if( node) {
                        node.labeled = true;
                    } else {
                        this.hoveredNode.labeled = false;
                    }
                    if( node && !this.hoveredNode ) {
                        this.highlightNeighbours(node, "both");
                        this.hoveredNode = node;
                    } else if ( !node && 
                                this.hoveredNode && 
                                !this.dragging ){
                        this.resetHighlightNeighbours();
                        this.hoveredNode = undefined;
                    }
                })
                .on("click", () => {
                    let node = nodeHovered(this.canvas);
                    if( node) {
                        this.openNodeLink(node);
                    }
                });

            function nodeHovered(canvas) {
                let mouse = d3.mouse(canvas);
                let x = mouse[0];
                let y = mouse[1];
                let node = simulation.find( x, y);
                return simulation.find( x, y, node.r);
            }

        });

    }

    showNodeLabel(node) {
        
    }


    addTimestamps() {
        this.graphData.nodes.forEach( node => {
            node.timestamp = Date.parse(node.retweet_created_at) / 1000;
        });
        this.graphData.nodes.sort( (a,b) => {
            return a.timestamp - b.timestamp;
        })
        let authorNode = this.graphData.nodes[0];
        let firstTime = authorNode.timestamp;
        let lastTime = this.graphData.nodes[this.graphData.nodes.length -1].timestamp;
        let multiplicator = (lastTime - firstTime) / (this.width - authorNode.r);
        this.graphData.nodes.forEach( node => {
            node.rel_timestamp = authorNode.r + ((node.timestamp - firstTime) / multiplicator);
        })
    }


    dragstarted() {
        this.dragging = true;
        if( !d3.event.active)
            this.simulation.alphaTarget(0.3).restart();
        d3.event.subject.fx = d3.event.subject.x;
        d3.event.subject.fy = d3.event.subject.y;
    }

    dragged() {
        d3.event.subject.fx = d3.event.x;
        d3.event.subject.fy = d3.event.y;
    }

    dragended() {
        this.dragging = false;
        if( !d3.event.active) 
            this.simulation.alphaTarget(0);
        d3.event.subject.fx = null;
        d3.event.subject.fy = null;
    }


    drawLink(d) {
        let angle = Math.atan2( d.target.y- d.source.y, d.target.x - d.source.x);
        let xPos = d.target.x - d.target.r * Math.cos(angle);
        let yPos = d.target.y - d.target.r * Math.sin(angle);
        this.context.moveTo(d.source.x, d.source.y);
        this.context.lineTo( xPos, yPos);
        this.context.strokeStyle = "rgba(140,140,140,"+d.opacity+")";
        this.context.lineWidth = 1;
        this.drawHead(xPos, yPos, angle)
    }

    drawHead(xPos, yPos, angle) {
        let headlen = 5;
        let headRightX = xPos - headlen * Math.cos(angle - Math.PI/6);
        let headRightY = yPos - headlen * Math.sin(angle - Math.PI/6); 
        this.context.lineTo( headRightX, headRightY);
        this.context.moveTo( xPos, yPos);
        let headLeftX = xPos - headlen * Math.cos(angle + Math.PI/6);
        let headLeftY = yPos - headlen * Math.sin(angle + Math.PI/6); 
        this.context.lineTo( headLeftX, headLeftY);

    }

    drawNode(d) {
        let lineWidth = d.r / 7;
        let radius = d.r - lineWidth;
        this.context.beginPath();
        this.context.moveTo( d.x + radius, d.y)
        this.context.arc(d.x, d.y, radius, 0, 2*Math.PI);
        this.context.lineWidth = lineWidth;
        this.context.fillStyle = "rgba("+this.colors[d.group]+","+d.opacity+")";
        this.context.strokeStyle = "rgba("+this.colors[d.group]+","+d.opacity+")";
        this.context.fill();
        this.context.stroke();
    }

    drawNodeLabel( node) {
        this.context.fillStyle = "white";
        let offset = 0;
        if(node.x < this.width / 2) {
            this.context.textAlign = "start";
            offset = node.r;
        } else {
            this.context.textAlign = "end";
            offset = -node.r;
        }
        this.context.font = "17px Roboto";
        if( node.group == 0) {
            this.context.fillText(node.name, node.x + offset, node.y);
        } else {
            this.context.fillText(node.base_link, node.x + offset, node.y);
        }
    }

    openNodeLink( node) {
        let link;
        if(node.group == 0) {
            link = node.web_link;
        } else {
            link = "http://" + node.base_link;
        }
        window.open(link, '_blank');
        window.focus();
    }

    startSimulation(): Promise<d3.forceSimulation> {
        return new Promise((resolve, reject) => {
            let simulation = d3.forceSimulation()
                .force("link", d3.forceLink().id(function(d) {
                    return d.id; 
                }))
                .force("charge", d3.forceManyBody().strength(function(d) {
                    return d.r * -20;
                }))
                .force("collide", d3.forceCollide().radius(function(d) {
                    return d.r * 1.5;
                }))
                .force("center", d3.forceCenter(this.width / 2, this.height / 2));

            simulation
                .nodes( this.graphData.nodes)
                .on( "tick", () => { return this.ticked()});

            simulation.force("link")
                .links(this.graphData.links);
            resolve(simulation);
        });

    }

    highlightNeighbours( node, direction) {
        let childLinks;
        let children;
        let parentLinks;
        let parents;


        //set graphs opacity to 0.2
        this.graphData.nodes.forEach( node => {
            node.opacity = 0.2;
        });
        this.graphData.links.forEach( link => {
            link.opacity = 0.2;
        });
        //make neighbour links visible and create lists of children/parents
        if( direction=="both" || direction=="next") { 
            childLinks = this.graphData.links.filter( link => {
                if( link.source == node) {
                    link.opacity = 1;
                    return link;
                }
            });
            children = childLinks.map( link => {
                return link.target;
            });
        }
        if( direction=="both" || direction=="previous") {
            parentLinks = this.graphData.links.filter( link => {
                if( link.target == node) {
                    link.opacity = 1;
                    return link;
                }
            });
            parents = parentLinks.map( link => {
                return link.source;
            });
        }

        node.opacity = 1;
        //make neighbour nodes visible
        if( direction=="both" || direction=="next") {
            this.graphData.nodes.forEach( node => {
                if( children.indexOf(node) >= 0){
                    node.opacity = 1;
                }
            });
        }
        if( direction=="both" || direction=="previous") {
            this.graphData.nodes.forEach( node => {
                if( parents.indexOf(node) >= 0) {
                    node.opacity = 1;
                }
            });
        }
        this.ticked();        
    }

    resetHighlightNeighbours() {
        this.graphData.nodes.forEach( node => {
            node.opacity = 1;
        });
        this.graphData.links.forEach( link => {
            link.opacity = 1;
        });
        this.ticked();
    }

    getNeighbours(d, direction=undefined): number {
        let matches = [];
        this.graphData.links.forEach( link => {
            if( !direction || direction == "in") {
                if(link.target == d.id) {
                    matches.push(link);
                }
            }
            if(!direction || direction == "out") {
                if(link.source == d.id) {
                    matches.push(link);
                }
            }
        })
        return matches.length;
    }

    
}
