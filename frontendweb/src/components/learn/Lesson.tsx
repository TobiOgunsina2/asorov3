import React from 'react'

const Lesson = () => {

    return(
    
    <div className="bg-gradient-to-br from-ewe-300/90 to-ewe-500/90 backdrop-blur-md h-full w-full rounded-3xl flex flex-row items-center justify-evenly hover:shadow-xl">
      <div className="bg-white h-30 w-30 rounded-3xl"></div>
      <div className="lesson-info rounded-2xl w-7/16 h-48 px-0.5 text-center flex flex-col items-center">
        <h1 className="lesson-title text-md text-white font-bold">Title</h1>
        <h4 className="lesson-description text-xs font-bold text-gray-300">Description</h4>
        <button
          
          className="bg-white rounded-lg py-1 text-sm font-bold mt-auto w-3/4 hover:text-gray-400"
        >
          Start Lesson
        </button>
      </div>
    </div>
    );

    {/*
    <div className="w-full h-full bg-gradient-to-br from-ewe-300 to-ewe-500 opacity-90 flex rounded-3xl items-center text-white justify-center">
      <div className="bg-ewe-500/70 h-3/4 w-3/4 rounded-xl"></div>
    </div>
  */}
}

export default Lesson