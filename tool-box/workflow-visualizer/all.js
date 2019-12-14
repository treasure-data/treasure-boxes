
function main() {
  fetch('tasks.json')
    .then(function(response) {
      return response.json();
    })
    .then(function(json) {
      new DigdagTaskDependencyRender(json['tasks']).render("#tasks")
    });
}

function DigdagTaskDependencyRender(tasks) {
  const self = this
  self.dagreRender = new dagreD3.render()
  self.tasks = tasks
  self.idToTask = {}
  self.parentIdToChildren = {}
  self.maxDuration = 0

  // Pre-process tasks
  tasks.forEach(function(task, index) {
    task.index = index

    const nameFragments = task.fullName.split(/[\+\^]/)
    task.name = nameFragments[nameFragments.length - 1]
    if (task.name == "sub") {
      task.name = "(generated)"
    }

    task.parallel = !!task.config._parallel

    task.children = []
    if (task.parentId) {
      self.idToTask[task.parentId].children.push(task)
    }

    if (task.startedAt) {
      task.duration = new Date(task.updatedAt) - new Date(task.startedAt)
      if (task.duration > self.maxDuration) {
        self.maxDuration = task.duration
      }
    } else {
      task.duration = 0
    }

    self.idToTask[task.id] = task
  })
}

DigdagTaskDependencyRender.prototype.render = function(selectExpr) {
  const self = this

  const root = d3.select(selectExpr)

  const dagTreeDiv = root.append("div")
  dagTreeDiv.attr("class", "digdag-dag-tree")

  const g = new dagreD3.graphlib.Graph()
    .setGraph({rankdir: "LR"})
    .setDefaultEdgeLabel(function() { return {} })

  self.tasks.forEach(function(task) {
    var durationClass = "duration-0"
    if (task.duration > 0) {
      durationClass = "duration-" + Math.ceil(task.duration / self.maxDuration * 10)
    }

    var html = `<div class="task">`;
    html += `<a class="status"></a>`
    html += `<span class="name">+${task.name}</span>`
    html += `<span class="duration ${durationClass}"></span>`
    html += `</div>`

    g.setNode(task.index, {
      labelType: "html",
      label: html,
      padding: 0,
      rx: 5,
      ry: 5,
      class: task.state,
    })

    //task.upstreams.forEach(function(upId) {
    //  g.setEdge(self.idToTask[upId].index, task.index)
    //})

    if (task.parentId) {
      g.setEdge(self.idToTask[task.parentId].index, task.index)
    }
  })

  // Render
  const dagDiv = dagTreeDiv.append("div")
  dagDiv.attr("class", "digdag-dag")

  const svg = dagDiv.append("svg")
  self.dagreRender(svg, g)

  // Adjust SVG image size
  svg.attr("height", Math.ceil(g.graph().height))
  svg.attr("width", Math.ceil(g.graph().width))
}

main();
