# Supported Markets Reference

## Exchange Format Guide

### US Markets (NYSE, NASDAQ)
- **Format**: Direct codes (e.g., 'AAPL')
- **Validation**: No suffix required

### China Markets
| Exchange | Format | Example |
|----------|--------|---------|
| Shanghai (SSE) | `.SS` suffix | `600519.SS` |
| Shenzhen (SZSE) | `.SZ` suffix | `002415.SZ` |

### International Markets
| Region | Suffix | Example |
|--------|--------|---------|
| Hong Kong | `.HK` | `0700.HK` |
| Japan | `.T` | `7203.T` |
| Germany | `.DE` | `SAP.DE` |
| France | `.PA` | `MC.PA` |
| UK | `.L` | `HSBA.L` |

## Validation Rules
1. All Chinese stocks require 6-digit codes
2. International stocks use company tickers with region suffix
3. Always verify with `validate_symbol()` before analysis

## Common Errors
- ❌ Missing suffix (e.g., `000001` instead of `000001.SS`)
- ❌ Incorrect digit count (Chinese stocks must be 6 digits)
- ❌ Mixed market formats (e.g., `AAPL.HK`)