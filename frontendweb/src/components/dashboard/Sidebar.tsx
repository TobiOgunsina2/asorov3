import React from 'react'
import ProgressCircle from './sidebar/Progress'


const Sidebar = () => {
  return (
    <div className="flex flex-col justify-between bg-ewe-500/60 hover:bg-ewe-500/65 glass-3d transform-gpu hover:rotateX-5 hover:rotateY-5  backdrop-blur-md shadow-lg border border-white/20 hover:scale-101 rounded-3xl space-y-2 text-white p-4 transition-all duration-400">
      <ProgressCircle color="ewe-700" strokeWidth={11} percentage={20} size={170} />
    </div>
  )
}

export default Sidebar