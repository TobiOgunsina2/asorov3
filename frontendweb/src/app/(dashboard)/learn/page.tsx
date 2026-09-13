import React from 'react'
import Unit from '@/components/learn/Unit'
import { api } from '@/api/clients'

// Pages in the app are async, this allows for server side rendering for better SEO
const Page = async () => {

  const { data: units, error } = await api.GET('/api/v1/courses/units/')
    
  return (
    <div className='text-black'>
      {units?.map(()=>{
        return <Unit/>
      })}
    </div>
  )
}

export default Page