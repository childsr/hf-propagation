#!/usr/bin/env node

const URL = "https://services.swpc.noaa.gov/text/drap_global_frequencies.txt"
const getCurrent = () => fetch(URL).then(res => res.text())
