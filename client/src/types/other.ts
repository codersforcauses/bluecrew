import { AxiosError } from 'axios'
export type ExtendedAxiosError = AxiosError & {
  config: { token_refreshed?: boolean; session_expired?: boolean }
}
