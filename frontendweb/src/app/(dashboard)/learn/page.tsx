import React from 'react'
import Unit from '@/components/learn/Unit'
import { api } from '@/api/clients'

// Pages in the app are async, this allows for server side rendering for better SEO
const Page = async () => {

  const { data: units, error } = await api.GET('/api/v1/courses/units/')

  if (error) {
    // TypeScript knows the structure of 'error' based on your OpenAPI spec
    console.error('Failed to fetch units:', error);
    // Handle the error (e.g., show a notification, return early)
    return;
  }
    
  return (
    <>
      {units?.map((unit)=>{
        return <Unit key={unit.id} unit={unit}/>
      })}
    </>
  )
}

export default Page