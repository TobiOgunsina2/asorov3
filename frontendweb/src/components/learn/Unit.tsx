import React from 'react'
import Lesson from './Lesson'

const Unit = () => {
  return (
    <div className="w-full h-full pt-6 snap-start flex flex-col">
      <div className="w-fit h-fit text-right">
        <h2 className="text-xl font-semibold text-gray-500">Unit 1</h2>
        <h2 className="text-2xl font-bold text-black">title</h2>
      </div>
      {/* Lessons Container */}
      <div className="w-full h-full self-stretch relative">
        
        <div
            className={`absolute opacity-90 cursor-pointer transition-all duration-500 ease-out transform hover:scale-101 `}
        >
        </div>
      </div>
    </div>
  )
}

export default Unit