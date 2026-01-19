const prefixes = {
    'p': 1e-12,
    'n': 1e-9,
    'u': 1e-6,
    'm': 1e-3,
    'k': 1e3,
    'M': 1e6,
    'G': 1e9
}

export const parseUnit = (value: string): number | null => {
    if (!value) return null

    const match = value.match(/^([\d.]+)\s*([pnumkMG]?)[a-zA-Z]*$/i)
    if (!match) return null

    const valStr = match[1]
    const prefix = match[2]

    if (valStr === undefined) return null

    const num = parseFloat(valStr)

    if (!prefix) return num

    const multiplier = prefixes[prefix as keyof typeof prefixes] || 1
    return num * multiplier
}

export const formatUnit = (value: number): string => {
    if (value >= 1e9) return (value / 1e9).toFixed(1) + 'G'
    if (value >= 1e6) return (value / 1e6).toFixed(1) + 'M'
    if (value >= 1e3) return (value / 1000).toFixed(1) + 'k'
    if (value >= 1) return value.toString()
    if (value >= 1e-3) return (value * 1e3).toFixed(1) + 'm'
    if (value >= 1e-6) return (value * 1e6).toFixed(1) + 'u'
    if (value >= 1e-9) return (value * 1e9).toFixed(1) + 'n'
    return (value * 1e12).toFixed(1) + 'p'
}
