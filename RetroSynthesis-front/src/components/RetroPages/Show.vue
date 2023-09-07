<template>
  <div class="container">
    <h1>Show</h1>
    <div id="parent" :style="{height:flag===true?'auto':'100px'}">
      <!--    <div class="parent">-->
      <div class="control col-sm-3">
        <a id="config" class="fa fa-minus-square" role="button" v-show="direction_show" style="color: #17a2b8"
           @click="direction_close"></a>
        <a id="config" class="fa fa-plus-square" role="button" v-show="!direction_show" style="color: #17a2b8"
           @click="direction_open"></a>
        <h5 id="direction">Direction</h5>
        <div v-show="direction_show">
          <li><i class="fa fa-circle-o" style="color: #5d4ef3;font-size: 20px;"></i> target molecule</li>
          <li><i class="fa fa-circle-o" style="color: #32B796;font-size: 20px;"></i> blocking blocks</li>
          <li><i class="fa fa-circle-o" style="color: #5f97d2;font-size: 20px;"></i> predicted intermediates</li>
          <li><i class="fa fa-square" style="color: #BFBFBF;font-size: 20px;"></i> reaction enzyme</li>
          <li><i class="fa fa-long-arrow-right" style="color: #EE2C2C;font-size: 20px;"></i> best retrosynthesis route</li>
          <li><b>You can click the molecule to redirect to PubChem</b></li>
        </div>
      </div>
      <div id="cy" ref="cy" :style="{height:flag===true?'700px':'0'}"></div>
    </div>
  </div>
</template>

<script>
import cytoscape from 'cytoscape'
import bus from '../../assets/js/eventBus'

export default {
  name: 'cytoscape',
  components: {},
  data() {
    return {
      elementsData: null,
      cidsData: null,
      bestPath: null,
      targetMol: null,
      buildMol: null,
      r_map: null,
      direction_show: false,
      flag: false,
      nodes: [],
      edges: [],
    }
  },
  methods: {
    createCytoscape() {
      let cy = cytoscape({
        container: document.getElementById('cy'),
        boxSelectionEnabled: false,
        zoomingEnabled: true,
        wheelSensitivity: 0.1,
        autounselectify: true,
        zoom: 1,
        minZoom: 0.4,
        maxZoom: 2,

        style: [{
          selector: 'node',
          style: {
            // 'content': 'data(id)',
            'border-color': '#5f97d2',
            'border-width': 3.5,
            'border-opacity': 1,
            'text-valign': 'center',
            "background-fit": "contain",
          },
        },
          {
            selector: 'edge',
            style: {
              'width': 4.5,
              'line-color': '#6495ED',
              'target-arrow-color': '#6495ED',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier'
            }
          }, {
            selector: 'node[label="mol"]',
            style: {
              // 'content': 'data(cid)',
              "text-opacity": 1,
              "text-valign": "bottom",
              "text-halign": "center",
              "font-weight": "bold",
              "text-margin-y": 8,
              "text-background-color": "White",
              "text-background-opacity": 0.85,
              "background-color": "#FFF",
              'background-image': 'data(backgroundImage)',
              width: 100,
              height: 100,
            }
          }, {
            selector: 'node[label="rct"]',
            style: {
              'content': 'data(true_id)',
              shape: "rectangle",
              "text-valign": "center",
              "text-halign": "center",
              color: "#575757",
              "border-color": "#BFBFBF",
              "border-style": "solid",
              "border-width": 4,
              "background-color": "white",
              width: 45,
              height: 45,
            }
          }],

        elements: this.eleData(),
        layout: {
          name: 'breadthfirst',
          fit: true, // whether to fit the viewport to the graph
          directed: true, // whether the tree is directed downwards (or edges can point in any direction if false)
          padding: 30, // padding on fit
          circle: false, // put depths in concentric circles if true, put depths top down if false
          grid: false, // whether to create an even grid into which the DAG is placed (circle:false only)
          spacingFactor: 1.75, // positive spacing factor, larger => more space between nodes (N.B. n/a if causes overlap)
          boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
          avoidOverlap: true, // prevents node overlap, may overflow boundingBox if not enough space
          nodeDimensionsIncludeLabels: false, // Excludes the label when calculating node bounding boxes for the layout algorithm
          // roots: cy.elements("node['"+this.startMol+"']"), // the roots of the trees
          animate: false, // whether to transition the node positions
        }
      })
      this.modify(cy);
    },
    eleData() {
      /*
        设置节点和边元素数据
       */
      let eles = {
        nodes: [],
        edges: []
      }
      let cids = this.cidsData
      this.elementsData[0].forEach(item => {
        eles.nodes.push({
          data: {
            id: item,
            cid: cids[item],
            label: 'mol',
            backgroundImage: 'http://127.0.0.1:5001/retro/tmp/svg/' + item + '.svg'
          }
        })
      }),
        this.elementsData[1].forEach(item => {
          eles.nodes.push({
            data: {
              id: item,
              true_id: this.r_map[item],
              label: 'rct',
            }
          })
        }),
        this.elementsData[2].forEach(item => {
          let tmp
          tmp = item.split('>>')
          eles.edges.push({
            data: {
              id: item,
              source: tmp[0],
              target: tmp[1],
            }
          })
        })
      return eles
    },
    direction_open() {
      this.direction_show = true
    },
    direction_close() {
      this.direction_show = false
    },
    setData(data) {
      /*
        获取data并设置
       */
      this.elementsData = data[0]
      this.cidsData = data[1]
      this.bestPath = data[2]
      this.r_map = data[3]
      this.targetMol = data[4]
      this.buildMol = data[5]
      this.direction_show = true
      this.flag = true
    },
    modify(cy) {
      // 添加a链接
      let node_dom = cy.elements("node[label='mol']")
      node_dom.on('click', function (e) {
        window.open('https://pubchem.ncbi.nlm.nih.gov/compound/' + e.target.data().cid)
      })
      // 增加最佳路径的颜色
      let reactions = this.bestPath
      let react, edge_dom
      for (let i = 0; i < reactions.length; i++) {
        react = reactions[i]
        edge_dom = cy.elements("edge[id='" + react + "']")
        edge_dom.style('line-color', '#EE2C63')
        edge_dom.style('target-arrow-color', '#EE2C63')
      }
      // 给目标分子加边框颜色
      let target_dom = cy.elements("node[id='" + this.targetMol + "']")
      target_dom.style('border-color', '#5d4ef3')
      // 给build分子加边框颜色
      let blocks = this.buildMol
      let block, block_dom
      for (let i = 0; i < blocks.length; i++) {
        block = blocks[i]
        block_dom = cy.elements("node[id='" + block + "']")
        block_dom.style('border-color', '#32B796')
      }
    }
  },
  mounted() {
    // data.elements,data.cids,data.best_route
    bus.$on('sendShowData', data => {
      this.setData(data)
      this.createCytoscape()
      this.modify()
    })
  }
}

</script>

<style scoped>
body {
  font: 14px helvetica neue, helvetica, arial, sans-serif;
}

#parent {
  position: relative;
  width: auto;
  margin: auto;
  border: 1px solid #17a2b8;
  border-radius: 10px;
}

#cy {
  width: auto;
  position: relative;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  margin: auto;
}

.control {
  position: absolute;
  top: 25px;
  left: 50px;
  box-shadow: 1px 2px 3px #ccc;
  border: 1px solid #DCDCDC;
  font-size: 14px;
  z-index: 9;
  border-radius: 3px;
}

#config {
  position: absolute;
  z-index: 99;
  padding: 10px;
  left: 0px;
}

#direction {
  margin-top: 10px;
  text-align: center;
  font-size: small;
  font-weight: bold;
}
</style>

