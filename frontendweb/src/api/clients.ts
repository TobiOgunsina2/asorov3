import createClient from "openapi-fetch"
import type { paths } from "./generated"

const API_URL = process.env.BACKEND_API_URL


export const api = createClient<paths>({
  baseUrl: API_URL,
  /*headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },*/
})