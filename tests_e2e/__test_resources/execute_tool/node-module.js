const [_, _2, ...args] = process.argv

console.log('executed node module')

if (args.length) {
    console.log('CLI arguments:')
    args.forEach(arg => console.log(arg))
}

console.log('envvars:')
console.log('HEXAGON_EXECUTION_TOOL =', process.env.HEXAGON_EXECUTION_TOOL)
console.log('HEXAGON_EXECUTION_ENV =', process.env.HEXAGON_EXECUTION_ENV)
