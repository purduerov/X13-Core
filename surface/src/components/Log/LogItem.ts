export interface LogItem{
    timestamp: string
    process: string
    text: string,
    color?: string
}

export default (proc: string, text: string, color = '#f0ffff') => {
    let i: LogItem = {
        timestamp: new Date().toISOString().substr(14, 5),
        process: proc,
        text: text,
        color: color
    }

    return i;
}
     