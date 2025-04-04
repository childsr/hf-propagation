const { readFileSync, readdirSync, writeFileSync } = require("fs")
const { join } = require("path")
const DATA_DIR = "data/iri-data"

function parse(data) {
  return data
    .trimEnd()
    .split("\n")
    .slice(34)
    .map(line => line.trim().split(/\s+/g))
    .map(line => [line[0],line[1],line[5]].map(parseFloat).map(x => x === -1 ? null : x))
    .map(([height,ne,Te]) => ({ height, ne: ne * 1e6, Te }))
}
function parseFile(name) {
  const inpath = join(DATA_DIR,name+".txt")
  const outpath = join(DATA_DIR,name+".json")
  const data = readFileSync(inpath,"utf8")
  const json = parse(data)
  writeFileSync(outpath,JSON.stringify(json),"utf8")
}

// const dir = readdirSync(DATA_DIR)
// const names = dir.map(f => f.slice(0,10))
// for (const name of names) {
//   parseFile(name)
// }
parseFile("iri1")