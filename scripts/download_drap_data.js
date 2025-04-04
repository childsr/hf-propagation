const { createWriteStream } = require("fs")
const { pipeline: _pipeline } = require("stream")
const { promisify } = require("util")

const pipeline = promisify(_pipeline)

/** @type {(year: 2015|2018|2021|2024, month: 1|4|7|10) => string} */
const downloadUrl = (year,month) => {
  const m = month.toString().padStart(2,"0")
  return `https://www.ngdc.noaa.gov/stp/drap/data/${year}/${m}/SWX_DRAP20_C_SWPC_${year}${m}01.tar.gz`
}
/** @type {(year: 2015|2018|2021|2024, month: 1|4|7|10) => string} */
const savePath = (year,month) => {
  const m = month.toString().padStart(2,"0")
  return `data/drap-data/drap-${year}-${m}.tar.gz`
}



const years = [2015,2018,2021,2024]
const months = [1,4,7,10]

/** @type {(year: 2015|2018|2021|2024, month: 1|4|7|10) => Promise<void>} */
async function get(year,month) {
  const url = downloadUrl(year,month)
  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`Failed to fetch ${url}: ${res.statusText}`);
  }
  const { body } = res
  if (!body) {
    throw new Error("failed to get data stream")
  }

  const fileStream = createWriteStream(savePath(year,month))

  return pipeline(body,fileStream)
}
async function main() {
  const pairs = years.flatMap(yr => months.map(mo => [yr,mo]))
  const n = pairs.length
  for (let i = 0; i < n; i++) {
    const [year,month] = pairs[i]
    console.log(`Downloading (${i+1}/${n}): '${downloadUrl(year,month)}' => '${savePath(year,month)}'`)
    await get(year,month)
    console.log("done")
  }
}

main()