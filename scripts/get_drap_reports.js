const { promises: fs } = require("fs")
const { basename, join } = require("path")

/** @type {(year: 2015|2018|2021|2024, month: 1|4|7|10) => string} */
const dirPath = (year,month) => {
  const m = month.toString().padStart(2,"0")
  return `data/drap-data/drap-${year}-${m}`
}
/** @type {(year: 2015|2018|2021|2024, month: 1|4|7|10, hour: number) => string} */
const path1 = (year,month,hour) => `SWX_DRAP20_C_SWPC_${year}${month.toString().padStart(2,"0")}01${hour}0000_GLOBAL.txt`
/** @type {(year: 2015|2018|2021|2024, month: 1|4|7|10) => string[]} */
const paths = (year,month) => {
  const hours = month === 1 ? [15,19,23] : [14,18,22]
  return hours.map(hour => `${dirPath(year,month)}/${path1(year,month,hour)}` )
}

const years = [2015,2018,2021,2024]
const months = [1,4,7,10]


async function main() {
  const pairs = years.flatMap(year => months.map(month => [year,month]))
  const allPaths = pairs.flatMap(([year,month]) => paths(year,month))
  for (const src of allPaths) {
    const dest = join("data/drap-data",basename(src))
    try {
      await fs.copyFile(src,dest)
    } catch (error) {
      console.error(error)
    }
  }
}

main()