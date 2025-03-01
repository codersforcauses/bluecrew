export interface BingoData {
  bingo_rows: number[]
  bingo_cols: number[]
  bingo_diag: number[]
  full_bingo: boolean
}

export interface BingoType {
  type: 'row' | 'column' | 'diagonal' | 'full'
  index?: number
}
