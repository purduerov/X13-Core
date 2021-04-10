export interface LogItem{
    timestamp: string
    process: string
    text: string
}

export default function(proc: string, text: string) {
    let i: LogItem = {
        timestamp: new Date().toISOString().substr(14, 5),
        process: proc,
        text: text
    }

    return i;
}
     