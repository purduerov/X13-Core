export interface LogItem{
    timestamp: string
    process: string
    text: string,
    color?: string
}

export const LOG_NORMAL = '#f0ffff';
export const LOG_WARNING = '#FFC900';
export const LOG_ERROR = '#FF3600';
export const LOG_SUCCESS = '#7AFF33';

export default (proc: string, text: string, color = LOG_NORMAL) => {
    let i: LogItem = {
        timestamp: new Date().toISOString().substr(14, 5),
        process: proc,
        text: text,
        color: color
    }

    return i;
}
     