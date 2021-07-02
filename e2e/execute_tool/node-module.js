const [_, _2, ...args] = process.argv

console.log('executed node module')

if (args.length) {
    console.log('CLI arguments:')
    args.forEach(arg => console.log(arg))
}